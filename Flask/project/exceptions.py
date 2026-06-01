class ApiError(Exception):
    def __init__(self, message, status_code=400, details=None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)

    def to_dict(self):
        payload = {
            "status": "error",
            "message": self.message
        }

        if self.details is not None:
            payload["details"] = self.details

        return payload


class BadRequestError(ApiError):
    def __init__(self, message="Bad request"):
        super().__init__(message, 400)


class UnauthorizedError(ApiError):
    def __init__(self, message="Unauthorized"):
        super().__init__(message, 401)


class ForbiddenError(ApiError):
    def __init__(self, message="Forbidden"):
        super().__init__(message, 403)


class NotFoundError(ApiError):
    def __init__(self, message="Not found"):
        super().__init__(message, 404)


class ConflictError(ApiError):
    def __init__(self, message="Conflict"):
        super().__init__(message, 409)
