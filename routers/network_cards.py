from typing import Annotated

from fastapi import APIRouter, Body

from models.base_response import BaseResponse
from models.networkcards import NetworkCardsResponse
from state import app_state
from utils.network import get_wifi_chipsets

network_card_router = APIRouter(prefix="/network_cards", tags=["network_cards"])


@network_card_router.get("/get/all")
async def get_network_cards() -> NetworkCardsResponse:
    devices = await get_wifi_chipsets()
    return NetworkCardsResponse(status=200, devices=devices)


@network_card_router.get("/get/current")
def get_current_card() -> BaseResponse:
    device = app_state.current_card
    if not device:
        return BaseResponse(success=False, message="No card selected yet")
    return BaseResponse(success=True, message=device)


@network_card_router.post("/set/current")
def set_current_card(device: Annotated[str, Body(embed=True)]) -> BaseResponse:
    app_state.current_card = device
    return BaseResponse(success=True, message=f"card {device} was selected")
