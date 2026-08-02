from fastapi import APIRouter
from service.NetworkCardsService import GetWifiChipsets

NetworkRouter = APIRouter(prefix="/api")

@NetworkRouter.get('/GetNetworkCards')
async def GetNetworkCards():
    devices = await GetWifiChipsets()
    return {"status": 200, "devices": devices }