from contextlib import asynccontextmanager
from typing import Annotated

import asyncpg
from fastapi import FastAPI, Depends
from starlette.requests import Request

from config import DATABASE_URL


@asynccontextmanager
async def setup_app_db_pool(_app: FastAPI):
    async with asyncpg.create_pool(DATABASE_URL) as pool:
        _app.state.db_pool = pool
        yield
        _app.state.db_pool = None


def get_request_db_pool(request: Request) -> asyncpg.Pool:
    return request.app.state.db_pool


GetRequestDbPool = Annotated[asyncpg.Pool, Depends(get_request_db_pool)]


async def wrap_request_in_transaction(pool: GetRequestDbPool) -> asyncpg.Connection:
    async with pool.acquire() as conn:
        async with conn.transaction():
            yield conn


ReqTx = Annotated[asyncpg.Connection, Depends(wrap_request_in_transaction)]
