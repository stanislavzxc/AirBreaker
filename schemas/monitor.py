from pydantic import BaseModel

class MonitorModeRequest(BaseModel):
    device: str

class MonitorModeResponse(BaseModel):
    succes: bool
    current_mode: str
