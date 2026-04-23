from flask import Blueprint, request, jsonify
from services.rental_service import create_rental, list_rentals, complete_rental

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

@rental_bp.route('/rentals/<int:rental_id>/complete', methods=['PUT'])
def complete_rental_route(rental_id):
    complete_rental(rental_id)
    return jsonify({"message": "rental completed"}), 200
