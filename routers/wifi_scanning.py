from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from schemas.scanning import WifiNetworkModel
from service.wifi_scanning_service import WifiScanningService

scanning_router = APIRouter(
    prefix="/ws",
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

