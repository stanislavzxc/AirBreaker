from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from models import BaseResponse
from deps.ws import get_monitor_device_ws

handshake_router = APIRouter(prefix="/handshake", tags=["handshake"])

@handshake_router.websocket("/ws/catch")
async def catch_handshake(ws: WebSocket, attack_type: str, device: str = Depends(get_monitor_device_ws)) -> None:
    await ws.accept()
    try:
        pass
    except WebSocketDisconnect:
        print("websocket was disconnected")

@handshake_router.post("/ws/stop", response_model=BaseResponse)
def stop_catching(ws: WebSocket):
    return BaseResponse(
        succes=True,
        message="catching handshake was stopped"
    )        

@handshake_router.get("/get", summary="get specific handshake by name of network")
def get_specific_handshake(name: str):
    pass

@handshake_router.get("/get/all", summary = "get all catched handshakes")
def get_all_handshakes():
    pass
