from tests.helpers import create_admin_token, create_user_token, create_product


def test_create_product(client):
    token = create_admin_token(client)
    response = create_product(client, token, name="Dog Food Test")

    assert response.status_code == 201


def test_create_product_requires_admin(client):
    token = create_user_token(client)

    response = client.post(
        "/products/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "User Product",
            "description": "No admin",
            "price": 1000,
            "stock": 5,
            "category": "Food"
        }
    )

    assert response.status_code == 403


def test_create_product_invalid_price(client):
    token = create_admin_token(client)

    response = client.post(
        "/products/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Bad Price Product",
            "description": "Invalid price",
            "price": -100,
            "stock": 5,
            "category": "Food"
        }
    )

    assert response.status_code == 400


def test_create_product_invalid_stock(client):
    token = create_admin_token(client)

    response = client.post(
        "/products/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Bad Stock Product",
            "description": "Invalid stock",
            "price": 1000,
            "stock": -5,
            "category": "Food"
        }
    )

    assert response.status_code == 400


def test_get_products(client):
    response = client.get("/products/")

    assert response.status_code == 200


def test_get_product_not_found(client):
    response = client.get("/products/999999")

    assert response.status_code == 404


def test_update_product(client):
    token = create_admin_token(client)
    create_product(client, token, name="Product Update", price=1000, stock=5)

    products = client.get("/products/")
    product_id = products.json[-1]["id"]

    response = client.put(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"price": 2000}
    )

    assert response.status_code == 200


def test_update_product_invalid_price(client):
    token = create_admin_token(client)
    create_product(client, token, name="Invalid Update", price=1000, stock=5)

    products = client.get("/products/")
    product_id = products.json[-1]["id"]

    response = client.put(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"price": -100}
    )

    assert response.status_code == 400


def test_delete_product(client):
    token = create_admin_token(client)
    create_product(client, token, name="Delete Product", price=1000, stock=10)

    products = client.get("/products/")
    product_id = products.json[-1]["id"]

    response = client.delete(
        f"/products/{product_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_update_nonexistent_product(client):
    token = create_admin_token(client)

    response = client.put(
        "/products/999999",
        headers={"Authorization": f"Bearer {token}"},
        json={"price": 9999}
    )

    assert response.status_code == 404


def test_delete_nonexistent_product(client):
    token = create_admin_token(client)

    response = client.delete(
        "/products/999999",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
