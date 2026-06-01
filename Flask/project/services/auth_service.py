from models.user import User
from config.database import db
from exceptions import BadRequestError, ConflictError, UnauthorizedError
from services.validation import (
    validate_email,
    validate_json,
    validate_required_string,
    validate_role
)

from flask_jwt_extended import (
    create_access_token
)


class AuthService:

    @staticmethod
    def register_user(data):

        validate_json(data)
        validate_required_string(data, "name")
        validate_email(data)
        validate_required_string(data, "password")
        validate_role(data)

        existing_user = User.query.filter_by(
            email=data["email"]
        ).first()

        if existing_user:
            raise ConflictError("Email already exists")

        user = User(
            name=data["name"],
            email=data["email"],
            role=data.get("role", "client")
        )

        user.set_password(
            data["password"]
        )

        db.session.add(user)
        db.session.commit()

        return {
            "message": "User created successfully"
        }, 201

    @staticmethod
    def login_user(data):

        validate_json(data)
        validate_email(data)
        validate_required_string(data, "password")

        user = User.query.filter_by(
            email=data["email"]
        ).first()

        if not user:
            raise UnauthorizedError("Invalid credentials")

        if not user.check_password(
            data["password"]
        ):
            raise UnauthorizedError("Invalid credentials")

        token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "role": user.role
            }
        )

        return {
            "access_token": token
        }, 200