def test_preflight_allows_configured_frontend_origin(client):
    response = client.options(
        "/products/",
        headers={
            "Origin": "http://127.0.0.1:8765",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Authorization, Content-Type",
        },
    )

    assert response.status_code == 200
    assert response.headers["Access-Control-Allow-Origin"] == "http://127.0.0.1:8765"
    assert "Authorization" in response.headers["Access-Control-Allow-Headers"]


def test_preflight_rejects_unconfigured_frontend_origin(client):
    response = client.options(
        "/products/",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert "Access-Control-Allow-Origin" not in response.headers
