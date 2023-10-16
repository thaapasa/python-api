from fastapi.testclient import TestClient
from main import app


def test_add_item():
    with TestClient(app) as client:
        resp1 = client.get("/items/2")
        assert resp1.status_code == 200
        resp = client.post("/items", json={"name": "Test item", "price": 65.90})
        assert resp.status_code == 200


def test_get_root():
    with TestClient(app) as client:
        resp = client.get("/")
        assert resp.status_code == 200
