from flask import Blueprint, request, jsonify
from services.rental_service import create_rental, list_rentals, update_rental_status

rental_bp = Blueprint('rental_bp', __name__)

@rental_bp.route('/rentals', methods=['POST'])
def create_rental_route():
    data = request.json
    rental_id = create_rental(data)
    return jsonify({"id": rental_id}), 201

@rental_bp.route('/rentals', methods=['GET'])
def list_rentals_route():
    filters = request.args
    rentals = list_rentals(filters)
    return jsonify(rentals)

@rental_bp.route('/rentals/<int:rental_id>/status', methods=['PUT'])
def update_rental_status_route(rental_id):
    data = request.json
    status = data.get('status')
    if not status:
        return jsonify({"error": "Campo 'status' requerido"}), 400
    result = update_rental_status(rental_id, status)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result), 200


