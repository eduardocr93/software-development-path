from flask import Blueprint, request, jsonify
from services.car_service import create_car, list_cars, update_car_status

car_bp = Blueprint('car_bp', __name__)

@car_bp.route('/cars', methods=['POST'])
def create_car_route():
    data = request.json
    car_id = create_car(data)
    return jsonify({"id": car_id}), 201

@car_bp.route('/cars', methods=['GET'])
def list_cars_route():
    filters = request.args
    cars = list_cars(filters)
    return jsonify(cars)

@car_bp.route('/cars/<int:car_id>/status', methods=['PUT'])
def update_car_status_route(car_id):
    data = request.json
    update_car_status(car_id, data['status'])
    return jsonify({"message": "Status updated"}), 200
