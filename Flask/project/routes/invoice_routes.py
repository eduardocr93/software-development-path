from flask import (Blueprint,request,jsonify)
from flask_jwt_extended import (jwt_required,get_jwt_identity)
from services.invoice_service import (InvoiceService)
from decorators.role_required import (admin_required)


invoice_bp = Blueprint("invoices",__name__)

@invoice_bp.route("/checkout",methods=["POST"])
@jwt_required()
def checkout():

    user_id = int(get_jwt_identity())

    request_data = request.get_json(silent=True)

    response, status = (InvoiceService.checkout(user_id,request_data))

    return jsonify(response), status

@invoice_bp.route("/",methods=["GET"])
@jwt_required()
def get_invoices():

    user_id = int(get_jwt_identity())

    response, status = (InvoiceService.get_user_invoices(user_id))

    return jsonify(response), status

@invoice_bp.route("/<int:invoice_id>", methods=["GET"])
@jwt_required()
def get_invoice(invoice_id):

    user_id = int(get_jwt_identity())

    response, status = (
        InvoiceService.get_invoice(
            invoice_id,
            user_id
        )
    )

    return jsonify(response), status


@invoice_bp.route("/<int:invoice_id>/refund",methods=["POST"])
@admin_required()
def refund_invoice(invoice_id):

    response, status = (InvoiceService.refund_invoice(invoice_id))

    return jsonify(response), status