from fastapi import APIRouter

from schemas import BaseResponse, WifiNetworkModel
from state import app_state

current_network_router = APIRouter(prefix="/network", tags=["network"])

@current_network_router.get('/get_current_network', response_model=BaseResponse)
def get_current_network():
    current_network : WifiNetworkModel = app_state.current_network
    return BaseResponse(
        success=True,
        message=current_network.model_dump_json()
    )

@current_network_router.post('/set_current_network', response_model=BaseResponse)
def set_current_network(request_data: WifiNetworkModel):
    app_state.current_network = request_data
    return BaseResponse(
        success=True,
        message=request_data.model_dump_json()
    )
