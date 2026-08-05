from fastapi import FastAPI

from contextlib import asynccontextmanager
import logging

from state import app_state 

from utils.network_manager import network_manager_awake
from utils.check_monitor_mode import check_monitor_mode

from routers.network_cards import network_card_router
from routers.monitor_mode import monitor_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if app_state.current_card:
        try:
            current_mode = check_monitor_mode(app_state.current_card)
            if current_mode == "monitor":
                await network_manager_awake(app_state.current_card)
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