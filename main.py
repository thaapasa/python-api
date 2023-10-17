from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.items_api import get_item_routes
from db import setup_app_db_pool


@asynccontextmanager
async def bootstrap(_app: FastAPI):
    async with setup_app_db_pool(_app):
        yield


app = FastAPI(lifespan=bootstrap)


@app.get("/")
def read_root():
    return {"Hello": "World", "sub": {"dada": 1010}, "missing": None}


app.include_router(get_item_routes())
