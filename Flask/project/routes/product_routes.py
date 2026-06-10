from flask import (
    Blueprint,
    request,
    jsonify
)

from services.product_service import (
    ProductService
)
from services.validation import validate_json

from decorators.role_required import (
    admin_required
)

product_bp = Blueprint(
    "products",
    __name__
)

@product_bp.route(
    "/",
    methods=["GET"]
)
def get_products():

    response, status = (
        ProductService.get_all_products()
    )

    return jsonify(response), status

@product_bp.route(
    "/<int:product_id>",
    methods=["GET"]
)
def get_product(product_id):

    response, status = (
        ProductService.get_product_by_id(
            product_id
        )
    )

    return jsonify(response), status

@product_bp.route(
    "/",
    methods=["POST"]
)
@admin_required()
def create_product():

    request_data = request.get_json(silent=True)
    validate_json(request_data)

    response, status = (
        ProductService.create_product(
            request_data
        )
    )

    return jsonify(response), status

@product_bp.route(
    "/<int:product_id>",
    methods=["PUT"]
)
@admin_required()
def update_product(product_id):

    request_data = request.get_json(silent=True)
    validate_json(request_data)

    response, status = (
        ProductService.update_product(
            product_id,
            request_data
        )
    )

    return jsonify(response), status

@product_bp.route(
    "/<int:product_id>",
    methods=["DELETE"]
)
@admin_required()
def delete_product(product_id):

    response, status = (
        ProductService.delete_product(
            product_id
        )
    )

    return jsonify(response), status