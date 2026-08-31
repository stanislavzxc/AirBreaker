import logging
from contextlib import asynccontextmanager

import fastapi_swagger_dark as fsd
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from errors import CommandException, NetworkCardNotFoundError, ServiceException
from models.errors import CommandErrorResponse, ServiceErrorResponse
from routers import (
    current_network_router,
    handshake_router,
    monitor_router,
    network_card_router,
    pmkid_router,
    scanning_router,
)
from service import set_monitor_mode_service
from state import app_state
from utils.network import check_network_card_mode


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if app_state.current_card:
        try:
            current_mode = check_network_card_mode(app_state.current_card)
            if current_mode == "monitor":
                await set_monitor_mode_service()
                logging.info(
                    f"switch card {app_state.current_card} to managed type"
                )
        except Exception as e:
            logging.error(f"Error during shutdown cleanup: {e}")



app = FastAPI(lifespan=lifespan, docs_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

swagger_router = APIRouter()
fsd.install(swagger_router)


app.include_router(swagger_router)
app.include_router(network_card_router)
app.include_router(monitor_router)
app.include_router(scanning_router)
app.include_router(current_network_router)
app.include_router(handshake_router)
app.include_router(pmkid_router)

@app.get('/')
def index():
    return "check /docs"

@app.exception_handler(CommandException)
def linux_command_error(_, exc: CommandException) -> JSONResponse:
    result = CommandErrorResponse(
        detail=exc.detail,
        code=exc.code,
        failed_cmd=exc.failed_cmd,
        stderr=exc.stderr
    )
    return JSONResponse(status_code=exc.code, content=result.model_dump())
    

@app.exception_handler(ServiceException)
async def service_exception(_, exc: ServiceException) -> JSONResponse:
    result = ServiceErrorResponse(
        code=exc.code,
        detail=exc.detail
    )
    return JSONResponse(status_code=exc.code, content=result.model_dump())

@app.exception_handler(NetworkCardNotFoundError)
async def not_found_exception(_, exc: NetworkCardNotFoundError) -> JSONResponse:
    result = NetworkCardNotFoundError()
    return JSONResponse(status_code=exc.code, content=result.model_dump()) 

