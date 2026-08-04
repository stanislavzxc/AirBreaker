from pydantic import BaseModel

class MonitorModeRequest(BaseModel):
    device: str

class MonitorModeResponse(BaseModel):
    success: bool
    current_mode: str
