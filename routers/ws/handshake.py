from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from deps.ws import get_monitor_device_ws
from models import BaseResponse, WifiNetworkModel
from service import HandshakeService

handshake_router = APIRouter(prefix="/handshake", tags=["handshake"])

handshake_service = HandshakeService()


@handshake_router.websocket("/ws/start")
async def catching_handshake(ws: WebSocket, attack_type: str, device: Annotated[str, Depends(get_monitor_device_ws)]) -> None:
    await ws.accept()
    try:
        await handshake_service.start_catching(device, attack_type)
        async for network_model in handshake_service.stream_results():
            json_data = network_model.model_dump()
            await ws.send_json(json_data)

    except WebSocketDisconnect:
        print("websocket was disconnected")
    finally:
        await handshake_service.stop_catching()

@handshake_router.post("/ws/stop", response_model=BaseResponse)
async def stop_catching():
    await handshake_service.stop_catching()
    return BaseResponse(
        success=True,
        message="catching handshake was stopped"
    )        

@handshake_router.get("/get", summary="get specific handshake by name of network")
def get_specific_handshake(name: str):
    pass

@handshake_router.get("/get/all", summary = "get all catched handshakes")
def get_all_handshakes():
    pass
