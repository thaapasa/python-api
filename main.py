from config import DATABASE_URL
from db import init_pool, close_pool

from fastapi import FastAPI
from api.items_api import get_item_routes


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_pool()


@app.on_event("shutdown")
async def shutdown_event():
    await close_pool()


@app.get("/")
def read_root():
    return {"Hello": "World", "sub": {"dada": 1010}, "missing": None}


app.mount("/items", get_item_routes())
