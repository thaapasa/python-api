from contextlib import asynccontextmanager

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from main import app
import pytest_asyncio


@pytest_asyncio.fixture
async def app_for_tests():
    async with LifespanManager(app) as manager:
        print("We're in!")
        yield manager.app


@pytest_asyncio.fixture
async def client():
    async with LifespanManager(app) as manager:
        print("App is", manager.app)
        print("App state is", manager.app.state)
        async with AsyncClient(
            app=manager.app, base_url="http://127.0.0.1:8000"
        ) as client:
            print("Client is ready")
            yield client


@pytest.mark.anyio
async def test_add_item(client):
    response = await client.get("/items/2")
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}
