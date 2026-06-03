from uuid import uuid4

from app import app
from config.database import db
from models.user import User


def random_email(prefix="user"):
    return f"{prefix}-{uuid4().hex}@test.com"


def register_user(client, role="client"):
    email = random_email(role)

    payload = {
        "name": "Test User",
        "email": email,
        "password": "123456"
    }

    client.post(
        "/auth/register",
        json=payload
    )

    return email


def login_user(client, email):
    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "123456"
        }
    )

    return response.json["access_token"]


def create_user_token(client):
    email = register_user(client, role="client")
    return login_user(client, email)


def create_admin_token(client):
    email = register_user(client, role="client")

    with app.app_context():
        user = User.query.filter_by(email=email).first()
        user.role = "admin"
        db.session.commit()

    return login_user(client, email)


def create_product(client, token, **kwargs):
    body = {
        "name": kwargs.get("name", "Test Product"),
        "description": kwargs.get("description", "Test product"),
        "price": kwargs.get("price", 1000),
        "stock": kwargs.get("stock", 10),
        "category": kwargs.get("category", "Food")
    }

    response = client.post(
        "/products/",
        headers={"Authorization": f"Bearer {token}"},
        json=body
    )

    return response


def create_cart(client, token):
    return client.post(
        "/carts/",
        headers={"Authorization": f"Bearer {token}"}
    )


def add_item_to_cart(client, token, product_id, quantity=1):
    return client.post(
        "/carts/items",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "product_id": product_id,
            "quantity": quantity
        }
    )
