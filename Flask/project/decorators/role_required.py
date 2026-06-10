from functools import wraps

from exceptions import ForbiddenError
from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt
)


def admin_required():

    def wrapper(fn):

        @wraps(fn)
        def decorator(*args, **kwargs):

            verify_jwt_in_request()

            claims = get_jwt()

            if claims["role"] != "admin":
                raise ForbiddenError("Admin access required")

            return fn(*args, **kwargs)

        return decorator

    return wrapper