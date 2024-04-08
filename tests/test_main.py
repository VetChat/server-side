from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root_happy_path():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_cors_allowed_origin():
    response = client.get("/", headers={"Origin": "http://localhost:5173"})
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_cors_disallowed_origin():
    response = client.get("/", headers={"Origin": "http://disallowed.com"})
    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers
