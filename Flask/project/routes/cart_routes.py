from flask import (
    Blueprint,
    jsonify,
    request
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from services.cart_service import (
    CartService
)

cart_bp = Blueprint(
    "carts",
    __name__
)


@cart_bp.route(
    "/",
    methods=["POST"]
)
@jwt_required()
def create_cart():

    user_id = int(
        get_jwt_identity()
    )

    response, status = (
        CartService.create_cart(
            user_id
        )
    )

    return jsonify(response), status

@cart_bp.route(
    "/my-cart",
    methods=["GET"]
)
@jwt_required()
def get_cart():

    user_id = int(
        get_jwt_identity()
    )

    response, status = (
        CartService.get_active_cart(
            user_id
        )
    )

    return jsonify(response), status

@cart_bp.route(
    "/items",
    methods=["POST"]
)
@jwt_required()
def add_item():

    user_id = int(
        get_jwt_identity()
    )

    request_data = request.get_json(silent=True)

    response, status = (
        CartService.add_item(
            user_id,
            request_data
        )
    )

    return jsonify(response), status

@cart_bp.route(
    "/items/<int:item_id>",
    methods=["PUT"]
)
@jwt_required()
def update_item(item_id):

    request_data = request.get_json(silent=True)

    response, status = (
        CartService.update_item(
            item_id,
            request_data
        )
    )

    return jsonify(response), status

@cart_bp.route(
    "/items/<int:item_id>",
    methods=["DELETE"]
)
@jwt_required()
def delete_item(item_id):

    response, status = (
        CartService.delete_item(
            item_id
        )
    )

    return jsonify(response), status