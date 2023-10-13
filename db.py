import asyncpg

from config import DATABASE_URL

pool: asyncpg.Pool = None


async def get_transaction() -> asyncpg.Connection:
    async with pool.acquire() as connection:
        async with connection.transaction():
            yield connection


async def init_pool():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)


async def close_pool():
    global pool
    await pool.close()
