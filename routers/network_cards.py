from fastapi import APIRouter, Body

from state import app_state

from schemas.base_response import BaseResponse
from schemas.networkcards import NetworkCardsResponse
from service.network_cards_service import get_wifi_chipsets

network_card_router = APIRouter(prefix="/api")


@network_card_router.get(
    "/get_all_network_cards", response_model=NetworkCardsResponse
)
async def get_network_cards() -> NetworkCardsResponse:
    devices = await get_wifi_chipsets()
    return NetworkCardsResponse(status=200, devices=devices)


@network_card_router.get(
    "/get_current_network_card", response_model=BaseResponse
)
def get_current_card() -> BaseResponse:
    device = app_state.current_card
    if not device:
        return BaseResponse(success=False, message="No card selected yet")
    return BaseResponse(success=True, message=device)


@network_card_router.post(
    "/set_current_network_card", response_model=BaseResponse
)
def set_current_card(device: str = Body(embed=True)) -> BaseResponse:
    app_state.current_card = device
    return BaseResponse(success=True, message=f"card {device} was selected")
