from exceptions import BadRequestError


def validate_json(data):
    if not isinstance(data, dict):
        raise BadRequestError("Request body must be a valid JSON object")


def validate_required_string(data, field, field_name=None, min_length=1):
    value = data.get(field)

    if value is None:
        raise BadRequestError(f"{field_name or field} is required")

    if not isinstance(value, str) or len(value.strip()) < min_length:
        raise BadRequestError(f"{field_name or field} must be a non-empty string")


def validate_optional_string(data, field, field_name=None):
    if field not in data or data[field] is None:
        return

    if not isinstance(data[field], str):
        raise BadRequestError(f"{field_name or field} must be a string")


def validate_email(data, field="email"):
    value = data.get(field)

    if value is None:
        raise BadRequestError(f"{field} is required")

    if not isinstance(value, str) or "@" not in value or "." not in value:
        raise BadRequestError("A valid email is required")


def validate_integer(data, field, required=True, min_value=None):
    if field not in data or data[field] is None:
        if required:
            raise BadRequestError(f"{field} is required")
        return

    value = data[field]

    if not isinstance(value, int):
        raise BadRequestError(f"{field} must be an integer")

    if min_value is not None and value < min_value:
        raise BadRequestError(f"{field} must be greater than or equal to {min_value}")


def validate_number(data, field, required=True, min_value=None):
    if field not in data or data[field] is None:
        if required:
            raise BadRequestError(f"{field} is required")
        return

    value = data[field]

    if not isinstance(value, (int, float)):
        raise BadRequestError(f"{field} must be a number")

    if min_value is not None and value < min_value:
        raise BadRequestError(f"{field} must be greater than or equal to {min_value}")


def validate_role(data, field="role"):
    if field not in data or data[field] is None:
        return

    if not isinstance(data[field], str) or data[field] not in ["admin", "client"]:
        raise BadRequestError("Role must be either 'admin' or 'client'")
