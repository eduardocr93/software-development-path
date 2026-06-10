from config.database import db
from exceptions import BadRequestError, NotFoundError
from sqlalchemy.orm import joinedload
from services.validation import (
    validate_integer
)

from models.cart import Cart
from models.cart_item import CartItem
from models.product import Product


class CartService:

    @staticmethod
    def create_cart(user_id):

        cart = Cart(
            user_id=user_id
        )

        db.session.add(cart)
        db.session.commit()

        return {
            "message": "Cart created successfully",
            "cart_id": cart.id
        }, 201
    
    @staticmethod
    def get_active_cart(user_id):

        cart = Cart.query.options(
            joinedload(Cart.items).joinedload(CartItem.product)
        ).filter_by(
            user_id=user_id,
            status="ACTIVE"
        ).first()

        if not cart:
            return {
                "message": "No active cart found"
            }, 404

        items = []

        total = 0

        for item in cart.items:

            subtotal = (
                item.product.price *
                item.quantity
            )

            total += subtotal

            items.append({
                "item_id": item.id,
                "product_id": item.product.id,
                "product_name": item.product.name,
                "price": item.product.price,
                "quantity": item.quantity,
                "subtotal": subtotal
            })

        return {
            "cart_id": cart.id,
            "status": cart.status,
            "items": items,
            "total": total
        }, 200
    
    @staticmethod
    def add_item(user_id, data):

        validate_integer(data, "product_id", min_value=1)
        validate_integer(data, "quantity", min_value=1)

        cart = Cart.query.filter_by(
            user_id=user_id,
            status="ACTIVE"
        ).first()

        if not cart:
            raise NotFoundError("No active cart found")

        product = db.session.get(
            Product,
            data["product_id"]
        )

        if not product:
            raise NotFoundError("Product not found")

        existing_item = CartItem.query.filter_by(
            cart_id=cart.id,
            product_id=product.id
        ).first()

        if existing_item:

            existing_item.quantity += data["quantity"]

        else:

            item = CartItem(
                cart_id=cart.id,
                product_id=product.id,
                quantity=data["quantity"]
            )

            db.session.add(item)

        db.session.commit()

        return {
            "message": "Product added to cart"
        }, 201

    @staticmethod
    def update_item(user_id, item_id, data):

        item = CartItem.query.join(Cart).filter(
            CartItem.id == item_id,
            Cart.user_id == user_id,
            Cart.status == "ACTIVE"
        ).first()

        if not item:
            raise NotFoundError("Item not found")

        validate_integer(data, "quantity", min_value=1)

        item.quantity = data["quantity"]

        db.session.commit()

        return {
            "message": "Item updated"
        }, 200

    @staticmethod
    def delete_item(user_id, item_id):

        item = CartItem.query.join(Cart).filter(
            CartItem.id == item_id,
            Cart.user_id == user_id,
            Cart.status == "ACTIVE"
        ).first()

        if not item:
            raise NotFoundError("Item not found")

        db.session.delete(item)
        db.session.commit()

        return {
            "message": "Item removed"
        }, 200    