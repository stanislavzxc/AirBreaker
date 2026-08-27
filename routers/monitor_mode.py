from fastapi import APIRouter, Depends

from models.monitor import MonitorModeResponse
from service.monitor_mode_service import set_monitor_mode_service
from utils.network import check_network_card_mode
from utils.network.network_card import check_network_card
monitor_router = APIRouter(tags=["Wi-Fi Monitor Mode"])

@monitor_router.post("/monitor_mode", response_model = MonitorModeResponse, summary="on/off monitor mode on current card")
async def set_monitor_mode():
    result = await set_monitor_mode_service()
    return result

@monitor_router.get("/is_monitor_mode")
def is_monitor_mode(device : str = Depends(check_network_card)) -> bool:
    mode = check_network_card_mode(device) 
    return mode == "monitor"