from fastapi import APIRouter
from service.monitor_mode_service import set_monitor_mode_service
from schemas.monitor import MonitorModeRequest,MonitorModeResponse

monitor_router = APIRouter(prefix="/api", tags=["Wi-Fi Monitor Mode"])

@monitor_router.post("/monitor_mode", response_model = MonitorModeResponse)
async def set_monitor_mode(request_data: MonitorModeRequest):
    result = await set_monitor_mode_service(request_data.device)
    return result