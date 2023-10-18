import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from server.main import app

# For async tests, see: https://fastapi.tiangolo.com/advanced/async-tests/
# Note that AsyncClient does not initialize the app state (lifespan events
# are not run).
# See the note in: https://www.python-httpx.org/async/
# Therefore we also need the LifespanManager to run the lifespan
# initialization.
# See: https://github.com/florimondmanca/asgi-lifespan#usage


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
