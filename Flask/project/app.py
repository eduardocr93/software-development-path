import os

import click
from flask import Flask, jsonify, request
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
from routes.user_routes import user_bp

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


@app.after_request
def add_cors_headers(response):
    origin = request.headers.get("Origin")
    if origin in app.config["FRONTEND_ORIGINS"]:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Vary"] = "Origin"
        response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


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
    app.logger.exception("Unhandled API exception")
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

app.register_blueprint(
    user_bp,
    url_prefix="/users"
)


@app.cli.command("promote-admin")
@click.argument("email")
def promote_admin(email):
    with app.app_context():
        user = User.query.filter_by(email=email.strip()).first()
        if user is None:
            raise click.ClickException(
                f"No existe una cuenta registrada con el correo {email.strip()}."
            )

        if user.role == "admin":
            click.echo("La cuenta ya tiene rol de administrador.")
            return

        user.role = "admin"
        db.session.commit()

    click.echo("Rol de administrador asignado. Vuelve a iniciar sesión para actualizar el token.")


if __name__ == "__main__":
    app.run(debug=True)