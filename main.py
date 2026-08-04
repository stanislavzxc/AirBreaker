from fastapi import FastAPI
from routers.network_cards import network_router
from routers.monitor_mode import monitor_router

app = FastAPI()

app.include_router(network_router)
app.include_router(monitor_router)
