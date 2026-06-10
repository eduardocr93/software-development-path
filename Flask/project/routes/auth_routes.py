from flask import (
    Blueprint,
    request,
    jsonify
)

from services.auth_service import (
    AuthService
)
from services.validation import validate_json
from decorators.role_required import admin_required

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route(
    "/register",
    methods=["POST"]
)
def register():

    request_data = request.get_json(silent=True)
    validate_json(request_data)

    response, status = (
        AuthService.register_user(
            request_data
        )
    )

    return jsonify(response), status


@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    request_data = request.get_json(silent=True)
    validate_json(request_data)

    response, status = (
        AuthService.login_user(
            request_data
        )
    )

    return jsonify(response), status

@auth_bp.route(
    "/admin-test",
    methods=["GET"]
)
@admin_required()
def admin_test():

    return jsonify({
        "message": "Welcome admin"
    })