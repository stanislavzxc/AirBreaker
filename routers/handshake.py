from fastapi import APIRouter, WebSocket, WebSocketDisconnect

handshake_router = APIRouter(prefix="/handshake", tags=["network"])

@handshake_router.websocket("/ws/catch")
def catch_handshake(websocket: WebSocket) -> None:
    pass

@handshake_router.get("/get_all", summary = "get all catched handshakes")
def get_all_handshakes():
    pass
