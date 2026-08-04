from fastapi import APIRouter
from service.monitor_mode_service import set_monitor_mode_service
from schemas.monitor import MonitorModeRequest

monitor_router = APIRouter(prefix="/api")

@monitor_router.post("/monitor_mode")
async def set_monitor_mode(device: MonitorModeRequest):
    result = await set_monitor_mode_service(device)
    return {result}