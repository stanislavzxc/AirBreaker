from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from deps.ws import get_monitor_device_ws
from models.base_response import BaseResponse
from service import WifiScanningService

scanning_router = APIRouter(
    prefix="/scanning/ws",
    tags=["wifi scanning mode"]
)

scanning_service = WifiScanningService()

@scanning_router.websocket("/start")
async def scanning(ws: WebSocket, device: Annotated[str, Depends(get_monitor_device_ws)] ) -> None :
    await ws.accept()

    try:
        await scanning_service.start_scanning(device)

        async for network_model in scanning_service.stream_results():
            json_data = network_model.model_dump() 
            await ws.send_json(json_data)
            
    except WebSocketDisconnect:
        print("websocket was diconnect")
    finally:
        await scanning_service.stop_scanning()

@scanning_router.get("/stop")
async def stop_scanning() -> BaseResponse:
    await scanning_service.stop_scanning()
    return BaseResponse(
        success=True,
        message="ws scanning was stopped succesfully"
    )
    

