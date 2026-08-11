import logging
from contextlib import asynccontextmanager

import fastapi_swagger_dark as fsd
from fastapi import APIRouter, FastAPI

from routers import monitor_router, network_card_router, scanning_router
from service.monitor_mode_service import set_monitor_mode_service
from state import app_state
from utils.network import check_webcard_mode


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



app = FastAPI(lifespan=lifespan, docs_url=None)

swagger_router = APIRouter()
fsd.install(swagger_router)


app.include_router(swagger_router)
app.include_router(network_card_router)
app.include_router(monitor_router)
app.include_router(scanning_router)
@app.get('/')
def index():
    return "check /docs"
