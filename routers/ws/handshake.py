from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from models import BaseResponse

handshake_router = APIRouter(prefix="/handshake", tags=["network"])

@handshake_router.websocket("/ws/catch")
def catch_handshake(ws: WebSocket, type: str) -> None:
    ws.accept()
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
