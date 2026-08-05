from pydantic import BaseModel

class Device(BaseModel):
    interface: str
    state: str
    driver: str

class NetworkCardsResponse(BaseModel):
    status: int
    devices: list[Device]
