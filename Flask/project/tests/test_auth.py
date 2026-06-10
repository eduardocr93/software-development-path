from tests.helpers import random_email, create_user_token, create_admin_token


def test_register_user(client):
    email = random_email("register")

    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "password": "123456"
        }
    )

    assert response.status_code == 201


def test_register_duplicate_email(client):
    email = random_email("duplicate")

    response1 = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "password": "123456"
        }
    )

    response2 = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "password": "123456"
        }
    )

    assert response1.status_code == 201
    assert response2.status_code == 409


def test_register_invalid_email(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "invalid-email",
            "password": "123456"
        }
    )

    assert response.status_code == 400


def test_register_invalid_role(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": random_email("role"),
            "password": "123456",
            "role": "superuser"
        }
    )

    assert response.status_code == 400


def test_login_success(client):
    token = create_user_token(client)

    assert token


def test_login_invalid_password(client):
    email = random_email("login")
    client.post(
        "/auth/register",
        json={
            "name": "Login User",
            "email": email,
            "password": "123456"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "wrong_password"
        }
    )

    assert response.status_code == 401


def test_login_wrong_email(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "noexist@test.com",
            "password": "123456"
        }
    )

    assert response.status_code == 401


def test_login_missing_password(client):
    email = random_email("nopassword")
    client.post(
        "/auth/register",
        json={
            "name": "Login User",
            "email": email,
            "password": "123456"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": email
        }
    )

    assert response.status_code == 400


def test_admin_route_requires_admin(client):
    token = create_user_token(client)

    response = client.get(
        "/auth/admin-test",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403


def test_admin_route_allows_admin(client):
    token = create_admin_token(client)

    response = client.get(
        "/auth/admin-test",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
