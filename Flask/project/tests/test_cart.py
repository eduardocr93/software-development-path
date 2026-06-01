from tests.helpers import create_user_token, create_admin_token, create_product, create_cart, add_item_to_cart


def test_create_cart(client):
    token = create_user_token(client)

    response = create_cart(client, token)

    assert response.status_code == 201


def test_add_item_to_cart(client):
    user_token = create_user_token(client)
    create_cart(client, user_token)

    admin_token = create_admin_token(client)
    create_product(client, admin_token, name="Cart Product", price=5000, stock=20)

    products = client.get("/products/")
    product_id = products.json[-1]["id"]

    response = add_item_to_cart(client, user_token, product_id, quantity=2)

    assert response.status_code == 201


def test_get_my_cart(client):
    token = create_user_token(client)
    create_cart(client, token)

    response = client.get(
        "/carts/my-cart",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_update_cart_item(client):
    user_token = create_user_token(client)
    create_cart(client, user_token)

    admin_token = create_admin_token(client)
    create_product(client, admin_token, name="Update Product", price=5000, stock=20)

    products = client.get("/products/")
    product_id = products.json[-1]["id"]

    add_item_to_cart(client, user_token, product_id, quantity=2)

    cart_response = client.get(
        "/carts/my-cart",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    item_id = cart_response.json["items"][0]["item_id"]

    response = client.put(
        f"/carts/items/{item_id}",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"quantity": 5}
    )

    assert response.status_code == 200


def test_delete_cart_item(client):
    user_token = create_user_token(client)
    create_cart(client, user_token)

    admin_token = create_admin_token(client)
    create_product(client, admin_token, name="Delete Product", price=5000, stock=20)

    products = client.get("/products/")
    product_id = products.json[-1]["id"]

    add_item_to_cart(client, user_token, product_id, quantity=2)

    cart_response = client.get(
        "/carts/my-cart",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    item_id = cart_response.json["items"][0]["item_id"]

    response = client.delete(
        f"/carts/items/{item_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 200


def test_add_item_invalid_product(client):
    token = create_user_token(client)
    create_cart(client, token)

    response = add_item_to_cart(client, token, 999999, quantity=1)

    assert response.status_code in (400, 404)


def test_add_item_invalid_quantity(client):
    user_token = create_user_token(client)
    create_cart(client, user_token)

    admin_token = create_admin_token(client)
    create_product(client, admin_token, name="Invalid Quantity Product", price=5000, stock=20)

    products = client.get("/products/")
    product_id = products.json[-1]["id"]

    response = add_item_to_cart(client, user_token, product_id, quantity=-1)

    assert response.status_code == 400


def test_update_item_invalid_quantity(client):
    user_token = create_user_token(client)
    create_cart(client, user_token)

    admin_token = create_admin_token(client)
    create_product(client, admin_token, name="Update Invalid Quantity", price=5000, stock=20)

    products = client.get("/products/")
    product_id = products.json[-1]["id"]

    add_item_to_cart(client, user_token, product_id, quantity=1)

    cart_response = client.get(
        "/carts/my-cart",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    item_id = cart_response.json["items"][0]["item_id"]

    response = client.put(
        f"/carts/items/{item_id}",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"quantity": -5}
    )

    assert response.status_code == 400


def test_remove_nonexistent_item(client):
    token = create_user_token(client)

    response = client.delete(
        "/carts/items/999999",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code in (400, 404)
