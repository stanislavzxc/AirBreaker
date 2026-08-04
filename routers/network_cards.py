from fastapi import APIRouter
from service.network_cards_service import GetWifiChipsets

network_router = APIRouter(prefix="/api")

@network_router.get('/GetNetworkCards')
async def GetNetworkCards():
    devices = await GetWifiChipsets()
    return {"status": 200, "devices": devices }