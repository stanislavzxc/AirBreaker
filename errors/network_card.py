from .app import AppException

class NetworkCardNotFoundError(AppException):
    def __init__(self, detail: str = "Network card not selected"):
        super().__init__(code=404, detail=detail)