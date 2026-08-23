from pydantic import BaseModel


class BaseResponse(BaseModel):
    success: bool = True
    message: str
