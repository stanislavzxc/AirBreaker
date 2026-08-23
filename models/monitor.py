from pydantic import BaseModel


class MonitorModeResponse(BaseModel):
    success: bool
    current_mode: str
