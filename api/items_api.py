from typing import Union

from fastapi import APIRouter
from fastapi import HTTPException

from data.items import Item
from db import ReqTx


def get_item_routes():
    """Add routes for the /items subpath"""

    router = APIRouter(prefix="/items")

    @router.get("/")
    async def read_item(tx: ReqTx):
        items = await tx.fetch(
            "SELECT * FROM items",
        )
        print("Found items", items)
        return {"items": items, "status": "ok"}

    @router.get("/foo")
    def get_foo():
        item1 = Item(name="athing", price=233.23, is_offer=True)
        item2 = Item(**{"name": "another", "price": 432})
        item3 = Item.model_validate({"name": "validated", "price": 53.24})
        return {"items": [item1, item2, item3]}

    @router.get("/{item_id}")
    async def read_item(
        tx: ReqTx,
        item_id: int,
        q: Union[str, None] = None,
    ):
        item = await tx.fetchrow("SELECT * FROM items WHERE id=$1", item_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        print("Found item", item)
        return {"item": item, "status": "ok", "q": q}

    @router.put("/{item_id}")
    async def update_item(tx: ReqTx, item_id: int, item: Item):
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

    @router.post("/")
    async def update_item(tx: ReqTx, item: Item):
        """Insert a new item"""
        item = await tx.fetchrow(
            "INSERT INTO items (name, price) VALUES ($1, $2) RETURNING *",
            item.name,
            item.price,
        )
        print("Inserted item", item)
        return {"status": "ok", "item": item}

    @router.delete("/{item_id}")
    async def delete_item(tx: ReqTx, item_id: int):
        item = await tx.fetchrow(
            "DELETE FROM items WHERE id=$1 RETURNING *",
            item_id,
        )
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        print("Deleted item", item)
        return {"status": "ok", "deleted": item}

    return router
