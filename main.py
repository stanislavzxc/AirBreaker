from fastapi import FastAPI
from routers.NetworkCards import NetworkRouter

app = FastAPI()

app.include_router(NetworkRouter)

