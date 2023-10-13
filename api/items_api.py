from fastapi import FastAPI
from typing import Union
from db import get_transaction
from data.items import Item

from fastapi import HTTPException, Depends


def get_item_routes():
    """Add routes for the /items subpath"""

    app = FastAPI()

    @app.get("/")
    async def read_item(tx=Depends(get_transaction)):
        items = await tx.fetch(
            "SELECT * FROM items",
        )
        print("Found items", items)
        return {"items": items, "status": "ok"}

    @app.get("/{item_id}")
    async def read_item(
        item_id: int, q: Union[str, None] = None, tx=Depends(get_transaction)
    ):
        item = await tx.fetchrow("SELECT * FROM items WHERE id=$1", item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        print("Found item", item)
        return {"item": item, "status": "ok", "q": q}

    @app.put("/{item_id}")
    async def update_item(item_id: int, item: Item, tx=Depends(get_transaction)):
        item = await tx.fetchrow(
            "UPDATE items SET name=$2, price=$3 WHERE id=$1 RETURNING *",
            item_id,
            item.name,
            item.price,
        )
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        print("Updated item", item)
        return {"status": "ok", "item": item}

    @app.post("/")
    async def update_item(item: Item, tx=Depends(get_transaction)):
        item = await tx.fetchrow(
            "INSERT INTO items (name, price) VALUES ($1, $2) RETURNING *",
            item.name,
            item.price,
        )
        print("Inserted item", item)
        return {"status": "ok", "item": item}

    @app.delete("/{item_id}")
    async def delete_item(item_id: int, tx=Depends(get_transaction)):
        item = await tx.fetchrow(
            "DELETE FROM items WHERE id=$1 RETURNING *",
            item_id,
        )
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        print("Deleted item", item)
        return {"status": "ok", "deleted": item}

    return app
