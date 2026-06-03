from tests.helpers import create_admin_token, random_email


def test_admin_can_list_users(client):
    token = create_admin_token(client)

    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_admin_can_create_user(client):
    token = create_admin_token(client)
    email = random_email("newuser")

    response = client.post(
        "/users/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "New User",
            "email": email,
            "password": "123456",
            "role": "client"
        }
    )

    assert response.status_code == 201
    assert response.json["user_id"]


def test_admin_can_update_user(client):
    admin_token = create_admin_token(client)
    email = random_email("updateuser")

    response = client.post(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "name": "Update User",
            "email": email,
            "password": "123456",
            "role": "client"
        }
    )

    user_id = response.json["user_id"]

    update_response = client.put(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "role": "admin"
        }
    )

    assert update_response.status_code == 200


def test_admin_can_delete_user(client):
    token = create_admin_token(client)
    email = random_email("deleteuser")

    response = client.post(
        "/users/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Delete User",
            "email": email,
            "password": "123456",
            "role": "client"
        }
    )

    user_id = response.json["user_id"]

    delete_response = client.delete(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert delete_response.status_code == 200
