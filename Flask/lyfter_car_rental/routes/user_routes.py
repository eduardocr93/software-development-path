from flask import Blueprint, request, jsonify
from services.user_service import create_user, list_users

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user_route():
    data = request.json
    user_id = create_user(data)
    return jsonify({"id": user_id}), 201

@user_bp.route('/users', methods=['GET'])
def list_users_route():
    filters = request.args
    users = list_users(filters)
    return jsonify(users)

@user_bp.route('/users/<int:user_id>/status', methods=['PUT'])
def update_user_status_route(user_id):
    data = request.json
    from services.user_service import update_user_status
    update_user_status(user_id, data['status'])
    return jsonify({"message": "status updated"}), 200
