from pydantic import BaseModel


class AppException(Exception):
    def __init__(self, code: int, detail: str):
        self.code = code
        self.detail = detail

        super().__init__(self.detail)
