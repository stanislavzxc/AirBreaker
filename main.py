from fastapi import FastAPI

from contextlib import asynccontextmanager
import logging

from state import app_state 

from service.monitor_mode_service import set_monitor_mode_service
from utils.check_webcard_mode import check_webcard_mode

from routers.network_cards import network_card_router
from routers.monitor_mode import monitor_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if app_state.current_card:
        try:
            current_mode = check_webcard_mode(app_state.current_card)
            if current_mode == "monitor":
                await set_monitor_mode_service()
                logging.info(
                    f"switch card {app_state.current_card} to managed type"
                )
        except Exception as e:
            logging.error(f"Error during shutdown cleanup: {e}")



app = FastAPI(lifespan=lifespan)

app.include_router(network_card_router)
app.include_router(monitor_router)

@app.get('/')
def index():
    return "check /docs"