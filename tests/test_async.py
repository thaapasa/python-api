import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from main import app


@pytest_asyncio.fixture
async def client():
    async with LifespanManager(app) as manager:
        print("App is", manager.app)
        async with AsyncClient(
            app=manager.app, base_url="http://127.0.0.1:8000"
        ) as client:
            print("Client is ready")
            yield client


@pytest.mark.asyncio
async def test_add_item(client):
    response = await client.get("/items/2")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
