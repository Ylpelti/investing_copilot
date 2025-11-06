class AppError(Exception):
    status_code: int = 400
    message: str = "Application error"

    def __init__(self, status_code: int | None = None, message: str | None = None):
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        super().__init__(self.message)

#User Errors
class UsernameDuplicateError(AppError):
    status_code = 400
    message = "Username already exist"

class EmailDuplicateError(AppError):
    status_code = 400
    message = "Email already registered"

class NotFound(AppError):
    status_code = 404
    message = "Resource not found"

class Forbidden(AppError):
    status_code = 403
    message = "Unsufficient permission"

class BadRequest(AppError):
    status_code = 400
    message = "Bad request"
    

