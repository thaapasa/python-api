from contextlib import asynccontextmanager
from typing import AsyncIterator, TypedDict

import asyncpg
from fastapi import FastAPI

from server.api.items_api import get_item_routes
from server.db import create_db_pool


class AppContext(TypedDict):
    db_pool: asyncpg.Pool


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[AppContext]:
    async with create_db_pool() as db_pool:
        yield {"db_pool": db_pool}


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World", "sub": {"dada": 1010}, "missing": None}


app.include_router(get_item_routes())
