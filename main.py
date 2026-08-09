import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

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



app = FastAPI(
    lifespan=lifespan,
    docs_url=None
)

app.include_router(network_card_router)
app.include_router(monitor_router)
app.include_router(scanning_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/')
def index():
    return "check /docs"

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html_github():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        swagger_css_url="/static/swagger_ui_dark.css"
    )