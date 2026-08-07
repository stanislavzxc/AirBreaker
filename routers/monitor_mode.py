from fastapi import APIRouter

from schemas.monitor import MonitorModeResponse
from service.monitor_mode_service import set_monitor_mode_service

monitor_router = APIRouter(prefix="/api", tags=["Wi-Fi Monitor Mode"])

@monitor_router.post("/monitor_mode", response_model = MonitorModeResponse)
async def set_monitor_mode():
    result = await set_monitor_mode_service()
    return result
