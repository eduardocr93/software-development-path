from flask import request, Response
from functools import wraps

from jwt_manager import JWT_Manager

jwt_manager = JWT_Manager()


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get("Authorization")

        if token is None:

            return Response(status=401)

        token = token.replace("Bearer ", "")

        decoded = jwt_manager.decode(token)

        if decoded is None:

            return Response(status=401)

        request.user = decoded

        return f(*args, **kwargs)

    return decorated


def admin_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get("Authorization")

        if token is None:

            return Response(status=401)

        token = token.replace("Bearer ", "")

        decoded = jwt_manager.decode(token)

        if decoded is None:

            return Response(status=401)

        if decoded["role"] != "admin":

            return Response(status=403)

        request.user = decoded

        return f(*args, **kwargs)

    return decorated