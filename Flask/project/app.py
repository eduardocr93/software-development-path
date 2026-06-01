import os

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException

from config.database import db
from config.settings import Config
from exceptions import ApiError
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.cart_routes import cart_bp
from routes.invoice_routes import invoice_bp

# Models
from models.user import User
from models.product import Product
from models.cart import Cart
from models.cart_item import CartItem
from models.invoice import Invoice
from models.invoice_item import InvoiceItem

app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)

db.init_app(app)
migrate = Migrate(app, db)

@app.errorhandler(ApiError)
def handle_api_error(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HTTPException)
def handle_http_exception(error):
    return jsonify({
        "status": "error",
        "message": error.description
    }), error.code


@app.errorhandler(Exception)
def handle_exception(error):
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500

app.register_blueprint(
    auth_bp,
    url_prefix="/auth"
)

app.register_blueprint(
    product_bp,
    url_prefix="/products"
)

app.register_blueprint(
    cart_bp,
    url_prefix="/carts"
)

app.register_blueprint(
    invoice_bp,
    url_prefix="/invoices"
)

if __name__ == "__main__":
    app.run(debug=True)