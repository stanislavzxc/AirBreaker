from fastapi import APIRouter
from schemas.scanning import WifiNetworkModel 
scanning_router = APIRouter(
    prefix="/ws",
    taps=["wifi scannign mode"]
)

@scanning_router.websocket(
    "/wifi_scanning",
    response_model = WifiNetworkModel
)
async def scanning() -> WifiNetworkModel:
    pass
