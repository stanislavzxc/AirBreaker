from fastapi import APIRouter, WebSocket

from deps.ws import monitor_device
from service import PmkidService

pmkid_router = APIRouter(prefix="/Attack: PMKID")

pmkid_service = PmkidService()

@pmkid_router.websocket("/scanning/ws")
async def pmkid_capture(ws: WebSocket):
    ws.accept()
    pass
@pmkid_router.post("/scanning/stop")

async def pmkid_capture_stop():
    pass
