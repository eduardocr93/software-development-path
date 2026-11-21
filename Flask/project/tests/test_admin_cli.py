from app import app
from models.user import User
from tests.helpers import create_product, login_user, register_user


def test_promote_admin_command_grants_admin_product_access(client):
    email = register_user(client)

    result = app.test_cli_runner().invoke(
        args=["promote-admin", email]
    )

    assert result.exit_code == 0
    assert "Vuelve a iniciar sesión" in result.output

    token = login_user(client, email)
    response = create_product(client, token, name="Admin CLI Product")

    assert response.status_code == 201

    with app.app_context():
        assert User.query.filter_by(email=email).one().role == "admin"


def test_promote_admin_command_rejects_unknown_email():
    result = app.test_cli_runner().invoke(
        args=["promote-admin", "missing@example.com"]
    )

    assert result.exit_code != 0
    assert "No existe una cuenta registrada" in result.output
