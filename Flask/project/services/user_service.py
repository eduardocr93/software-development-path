from models.user import User
from config.database import db
from exceptions import BadRequestError, ConflictError, NotFoundError
from services.validation import validate_email, validate_required_string, validate_role, validate_optional_string


class UserService:

    @staticmethod
    def get_all_users():

        users = User.query.all()

        response = [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "created_at": user.created_at
            }
            for user in users
        ]

        return response, 200

    @staticmethod
    def get_user_by_id(user_id):

        user = db.session.get(
            User,
            user_id
        )

        if not user:
            raise NotFoundError("User not found")

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at
        }, 200

    @staticmethod
    def create_user(data):

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

        user.set_password(data["password"])

        db.session.add(user)
        db.session.commit()

        return {
            "message": "User created successfully",
            "user_id": user.id
        }, 201

    @staticmethod
    def update_user(user_id, data):

        if not data:
            raise BadRequestError("No update data provided")

        user = db.session.get(
            User,
            user_id
        )

        if not user:
            raise NotFoundError("User not found")

        if "name" in data:
            validate_required_string(data, "name")
            user.name = data["name"]

        if "email" in data:
            validate_email(data)
            existing_user = User.query.filter_by(
                email=data["email"]
            ).first()
            if existing_user and existing_user.id != user.id:
                raise ConflictError("Email already exists")
            user.email = data["email"]

        if "password" in data:
            validate_required_string(data, "password")
            user.set_password(data["password"])

        if "role" in data:
            validate_role(data)
            user.role = data["role"]

        db.session.commit()

        return {
            "message": "User updated successfully"
        }, 200

    @staticmethod
    def delete_user(user_id):

        user = db.session.get(
            User,
            user_id
        )

        if not user:
            raise NotFoundError("User not found")

        db.session.delete(user)
        db.session.commit()

        return {
            "message": "User deleted successfully"
        }, 200
