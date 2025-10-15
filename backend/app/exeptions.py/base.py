from typing import Optional, Any, List, Dict

class AppException(Exception):
    def __init__(self,  status_code: int , error_code: str, message: str, details: Optional[Any] = None, meta: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details
        self.meta = meta

class NotFound(AppException):
    def __init__(self, message: str = "Resource not found", **kvargs):
        super().__init__(status_code=404, error_code="not_found", message=message, **kvargs)

class Unauthorized(AppException):
    def __init__(self, message: str = "Unauthorized", **kvargs):
        super().__init__(status_code=401, error_code="unauthorized", message=message, **kvargs)

class PermissionDenied(AppException):
    def __init__(self, message: str = "Permission denied", **kvargs):
        super().__init__(status_code=403, error_code="permission_denied", message=message, **kvargs)
