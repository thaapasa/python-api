import pytest
import asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from data.items import Item
from main import app
from api.items_api import get_item_routes
from db import init_pool, close_pool


@pytest.fixture(scope="module")
async def setup_pool():
    await init_pool()
    yield None
    await close_pool()


@pytest.fixture
def async_client(setup_pool):
    return AsyncClient(app=get_item_routes(), base_url="http://127.0.0.1:8000/items")


@pytest.fixture
def client(setup_pool):
    return TestClient(app)


@pytest.mark.anyio
async def test_add_item():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/items/2")
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}
