from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket

from deps.ws import get_monitor_device_ws
from models import BaseResponse
from service import PmkidService

pmkid_router = APIRouter(prefix="/Attack: PMKID")

pmkid_service = PmkidService()

@pmkid_router.websocket("/scanning/ws")
async def pmkid_capture(ws: WebSocket, device : Annotated[str, Depends(get_monitor_device_ws)])-> None:
    ws.accept()
    await pmkid_service.start_capture(device)
    async for network_model in pmkid_service.stream_results():
        json_data = network_model.model_dump()
        ws.send_json(json_data) 

@pmkid_router.post("/scanning/stop", response_model=BaseResponse)
async def pmkid_capture_stop():
    await pmkid_service.stop_capture()
    return BaseResponse(
        success=True,
        message="pmkid capture was stopped"
    )
    

