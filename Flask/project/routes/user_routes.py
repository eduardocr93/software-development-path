from flask import Blueprint, request, jsonify

from decorators.role_required import admin_required
from services.user_service import UserService
from services.validation import validate_json

user_bp = Blueprint(
    "users",
    __name__
)


@user_bp.route(
    "/",
    methods=["GET"]
)
@admin_required()
def get_users():

    response, status = (
        UserService.get_all_users()
    )

    return jsonify(response), status


@user_bp.route(
    "/<int:user_id>",
    methods=["GET"]
)
@admin_required()
def get_user(user_id):

    response, status = (
        UserService.get_user_by_id(
            user_id
        )
    )

    return jsonify(response), status


@user_bp.route(
    "/",
    methods=["POST"]
)
@admin_required()
def create_user():

    request_data = request.get_json(silent=True)
    validate_json(request_data)

    response, status = (
        UserService.create_user(
            request_data
        )
    )

    return jsonify(response), status


@user_bp.route(
    "/<int:user_id>",
    methods=["PUT"]
)
@admin_required()
def update_user(user_id):

    request_data = request.get_json(silent=True)
    validate_json(request_data)

    response, status = (
        UserService.update_user(
            user_id,
            request_data
        )
    )

    return jsonify(response), status


@user_bp.route(
    "/<int:user_id>",
    methods=["DELETE"]
)
@admin_required()
def delete_user(user_id):

    response, status = (
        UserService.delete_user(
            user_id
        )
    )

    return jsonify(response), status
