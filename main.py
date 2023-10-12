import asyncpg

from typing import Union
from config import DATABASE_URL

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session


async def create_db_pool():
    return await asyncpg.create_pool(DATABASE_URL)


db_pool = create_db_pool()
app = FastAPI()


def get_db():
    db = db_pool.acquire()
    yield db
    db.release()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.post("/items")
async def update_item(item: Item):
    # Take a connection from the pool.
    async with db_pool.acquire() as connection:
        # Open a transaction.
        async with connection.transaction():
            item = await connection.execute(
                "INSERT INTO items (name, price) VALUES ($1, $2) RETURNING *",
                item.name,
                item.price,
            ).fetchone()
            print("Inserted item", item)
            return {"status": "ok"}
