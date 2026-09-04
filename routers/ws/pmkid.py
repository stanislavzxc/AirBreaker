from fastapi import APIRouter, WebSocket, Depends

from deps.ws import monitor_device
from service import PmkidService
from models import PmkidCaptured, BaseResponse
from typing import Annotated
pmkid_router = APIRouter(prefix="/Attack: PMKID")

pmkid_service = PmkidService()

@pmkid_router.websocket("/scanning/ws")
async def pmkid_capture(ws: WebSocket, device : Annotated[str, Depends(monitor_device)] ):
    ws.accept()
    await pmkid_service.start_capture(device)
    async for network_model in pmkid_service.stream_results():
        json_data = network_model.model_dump()
        ws.send_json(json_data) 

@pmkid_router.post("/scanning/stop")
async def pmkid_capture_stop():
    await pmkid_service.stop_capture()
    return BaseResponse(
        success=True,
        message="pmkid capture was stopped"
    )
    

