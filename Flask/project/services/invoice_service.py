from config.database import db
from config.cache import cache
from exceptions import BadRequestError, ForbiddenError, NotFoundError
from sqlalchemy.orm import joinedload
from uuid import uuid4
from services.validation import (
    validate_required_string
)

from models.cart import Cart
from models.cart_item import CartItem
from models.invoice import Invoice
from models.invoice_item import InvoiceItem
from models.product import Product


class InvoiceService:

    @staticmethod
    def checkout(user_id, data):

        validate_required_string(data, "billing_address")
        validate_required_string(data, "payment_method")

        cart = Cart.query.options(
            joinedload(Cart.items).joinedload(CartItem.product)
        ).filter_by(
            user_id=user_id,
            status="ACTIVE"
        ).first()

        if not cart:
            raise NotFoundError("No active cart found")

        if len(cart.items) == 0:
            raise BadRequestError("Cart is empty")

        total = 0

        for item in cart.items:

            if item.quantity > item.product.stock:
                raise BadRequestError(
                    f"Not enough stock for {item.product.name}"
                )

            total += (
                item.quantity *
                item.product.price
            )

        invoice = Invoice(
            invoice_number = (f"INV-{uuid4().hex[:12].upper()}"),
            user_id=user_id,
            billing_address=data["billing_address"],
            payment_method=data["payment_method"],
            total=total
        )

        db.session.add(invoice)
        db.session.flush()

        invalidated_products = set()

        for item in cart.items:

            invoice_item = InvoiceItem(
                invoice_id=invoice.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.product.price,
                subtotal=(
                    item.quantity *
                    item.product.price
                )
            )

            db.session.add(invoice_item)

            item.product.stock -= item.quantity
            invalidated_products.add(item.product_id)

        cache.delete("products_all")
        for product_id in invalidated_products:
            cache.delete(f"product_{product_id}")

        cart.status = "COMPLETED"

        db.session.commit()

        return {
            "message": "Purchase completed",
            "invoice_id": invoice.id,
            "invoice_number": invoice.invoice_number
        }, 201
    
    @staticmethod
    def get_user_invoices(user_id):

        invoices = Invoice.query.filter_by(
            user_id=user_id
        ).all()

        result = []

        for invoice in invoices:

            result.append({
                "id": invoice.id,
                "invoice_number": invoice.invoice_number,
                "total": invoice.total,
                "status": invoice.status,
                "created_at": invoice.created_at
            })

        return result, 200
    
    @staticmethod
    def get_invoice(
        invoice_id,
        user_id
    ):

        invoice = Invoice.query.options(
            joinedload(Invoice.items).joinedload(InvoiceItem.product)
        ).filter_by(
            id=invoice_id
        ).first()

        if not invoice:
            raise NotFoundError("Invoice not found")
        
        if invoice.user_id != user_id:
            raise ForbiddenError("Unauthorized")

        items = []

        for item in invoice.items:

            items.append({
                "product_id": item.product_id,
                "product_name": item.product.name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "subtotal": item.subtotal
            })

        return {
            "id": invoice.id,
            "invoice_number": invoice.invoice_number,
            "billing_address": invoice.billing_address,
            "payment_method": invoice.payment_method,
            "status": invoice.status,
            "total": invoice.total,
            "items": items
        }, 200
    
    @staticmethod
    def refund_invoice(invoice_id):

        invoice = Invoice.query.options(
            joinedload(Invoice.items)
        ).filter_by(
            id=invoice_id
        ).first()

        if not invoice:
            raise NotFoundError("Invoice not found")

        if invoice.status == "REFUNDED":
            raise BadRequestError("Invoice already refunded")

        invalidated_products = set()

        for item in invoice.items:

            product = db.session.get(
                Product,
                item.product_id
            )

            product.stock += item.quantity
            invalidated_products.add(item.product_id)

        cache.delete("products_all")
        for product_id in invalidated_products:
            cache.delete(f"product_{product_id}")

        invoice.status = "REFUNDED"

        db.session.commit()

        return {
            "message": "Refund completed"
        }, 200
    
