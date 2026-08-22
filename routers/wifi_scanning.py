from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from schemas.base_response import BaseResponse
from service.wifi_scanning_service import WifiScanningService

scanning_router = APIRouter(
    prefix="/network/ws",
    tags=["wifi scannign mode"]
)

scanning_service = WifiScanningService()

@scanning_router.websocket("/wifi_scanning")
async def scanning(websocket: WebSocket) -> None :
    await websocket.accept()

    try:
        await scanning_service.start_scanning()

        async for  network_model in scanning_service.stream_results():
            json_data = network_model.model_dump() 
            await websocket.send_json(json_data)
            
    except WebSocketDisconnect:
        print("websocket was diconnect")
    finally:
        await scanning_service.stop_scanning()

@scanning_router.get("/wifi_scanning_stop")
async def stop_scanning() -> BaseResponse:
    await scanning_service.stop_scanning()
    return BaseResponse(
        success=True,
        message="ws scanning was stopped succesfully"
    )
    

