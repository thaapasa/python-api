import asyncpg

from typing import Union
from config import DATABASE_URL

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session


pool = None
app = FastAPI()


@app.on_event("startup")
async def startup_event():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)


@app.on_event("shutdown")
async def shutdown_event():
    global pool
    await pool.close()


def get_db():
    db = pool.acquire()
    yield db
    db.release()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World", "sub": {"dada": 1010}, "missing": None}


@app.get("/items")
async def read_item():
    # Take a connection from the pool.
    async with pool.acquire() as connection:
        # Open a transaction.
        async with connection.transaction():
            items = await connection.fetch(
                "SELECT * FROM items",
            )
            print("Found items", items)
            return {"items": items, "status": "ok"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    # Take a connection from the pool.
    async with pool.acquire() as connection:
        # Open a transaction.
        async with connection.transaction():
            item = await connection.fetchrow("SELECT * FROM items WHERE id=$1", item_id)
            if item is None:
                raise HTTPException(status_code=404, detail="Item not found")
            print("Found item", item)
            return {"item": item, "status": "ok", "q": q}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    # Take a connection from the pool.
    async with pool.acquire() as connection:
        # Open a transaction.
        async with connection.transaction():
            item = await connection.fetchrow(
                "UPDATE items SET name=$2, price=$3 WHERE id=$1 RETURNING *",
                item_id,
                item.name,
                item.price,
            )
            if item is None:
                raise HTTPException(status_code=404, detail="Item not found")
            print("Updated item", item)
            return {"status": "ok", "item": item}


@app.post("/items")
async def update_item(item: Item):
    # Take a connection from the pool.
    async with pool.acquire() as connection:
        # Open a transaction.
        async with connection.transaction():
            item = await connection.fetchrow(
                "INSERT INTO items (name, price) VALUES ($1, $2) RETURNING *",
                item.name,
                item.price,
            )
            print("Inserted item", item)
            return {"status": "ok", "item": item}


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    # Take a connection from the pool.
    async with pool.acquire() as connection:
        # Open a transaction.
        async with connection.transaction():
            item = await connection.fetchrow(
                "DELETE FROM items WHERE id=$1 RETURNING *",
                item_id,
            )
            if item is None:
                raise HTTPException(status_code=404, detail="Item not found")
            print("Deleted item", item)
            return {"status": "ok", "deleted": item}
