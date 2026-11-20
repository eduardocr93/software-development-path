from tests.helpers import create_user_token, create_admin_token, create_product, create_cart, add_item_to_cart
from app import app
from config.database import db
from models.invoice import Invoice
from models.user import User
from tests.helpers import register_user


def setup_checkout(client, user_token):
    create_cart(client, user_token)
    admin_token = create_admin_token(client)
    create_product(client, admin_token, name="Checkout Product", price=10000, stock=50)

    products = client.get("/products/")
    product_id = products.json[-1]["id"]

    add_item_to_cart(client, user_token, product_id, quantity=2)
    return product_id


def test_admin_can_list_all_invoices(client):
    admin_token = create_admin_token(client)
    customer_email = register_user(client)

    with app.app_context():
        customer = User.query.filter_by(email=customer_email).one()
        invoice = Invoice(
            invoice_number="INV-ADMIN-001",
            user_id=customer.id,
            billing_address="San José",
            payment_method="SINPE",
            total=12500,
            status="PAID",
        )
        db.session.add(invoice)
        db.session.commit()

    response = client.get(
        "/invoices/admin",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    assert response.json[0]["invoice_number"] == "INV-ADMIN-001"
    assert response.json[0]["customer_name"] == "Test User"
    assert response.json[0]["total"] == 12500


def test_client_cannot_list_all_invoices(client):
    token = create_user_token(client)

    response = client.get(
        "/invoices/admin",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403


def test_checkout(client):
    user_token = create_user_token(client)
    setup_checkout(client, user_token)

    response = client.post(
        "/invoices/checkout",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "billing_address": "Heredia",
            "payment_method": "SINPE"
        }
    )

    assert response.status_code == 201


def test_get_user_invoices(client):
    token = create_user_token(client)

    response = client.get(
        "/invoices/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_checkout_without_cart(client):
    token = create_user_token(client)

    response = client.post(
        "/invoices/checkout",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "billing_address": "Heredia",
            "payment_method": "SINPE"
        }
    )

    assert response.status_code == 404


def test_checkout_empty_cart(client):
    token = create_user_token(client)
    create_cart(client, token)

    response = client.post(
        "/invoices/checkout",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "billing_address": "Heredia",
            "payment_method": "SINPE"
        }
    )

    assert response.status_code == 400


def test_checkout_missing_billing_address(client):
    token = create_user_token(client)
    setup_checkout(client, token)

    response = client.post(
        "/invoices/checkout",
        headers={"Authorization": f"Bearer {token}"},
        json={"payment_method": "SINPE"}
    )

    assert response.status_code == 400


def test_checkout_missing_payment_method(client):
    token = create_user_token(client)
    setup_checkout(client, token)

    response = client.post(
        "/invoices/checkout",
        headers={"Authorization": f"Bearer {token}"},
        json={"billing_address": "Heredia"}
    )

    assert response.status_code == 400


def test_invoice_not_found(client):
    token = create_user_token(client)

    response = client.get(
        "/invoices/999999",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404


def test_refund_nonexistent_invoice(client):
    token = create_admin_token(client)

    response = client.post(
        "/invoices/999999/refund",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404


def test_refund_requires_admin(client):
    user_token = create_user_token(client)

    response = client.post(
        "/invoices/999999/refund",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 403


def test_get_invoice_unauthorized(client):
    user_token = create_user_token(client)
    other_token = create_user_token(client)

    setup_checkout(client, user_token)

    client.post(
        "/invoices/checkout",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "billing_address": "Heredia",
            "payment_method": "SINPE"
        }
    )

    invoice_response = client.get(
        "/invoices/",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    invoice_id = invoice_response.json[0]["id"] if invoice_response.json else None

    assert invoice_id is not None

    response = client.get(
        f"/invoices/{invoice_id}",
        headers={"Authorization": f"Bearer {other_token}"}
    )

    assert response.status_code == 403


def test_refund_invoice(client):
    user_token = create_user_token(client)
    setup_checkout(client, user_token)

    client.post(
        "/invoices/checkout",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "billing_address": "Heredia",
            "payment_method": "SINPE"
        }
    )

    invoice_list = client.get(
        "/invoices/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    invoice_id = invoice_list.json[0]["id"]

    admin_token = create_admin_token(client)
    response = client.post(
        f"/invoices/{invoice_id}/refund",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
