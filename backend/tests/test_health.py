from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check_returns_api_status():
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "HotelSec PolicyForge AI"


def test_root_endpoint_returns_public_api_metadata():
    response = client.get("/")

    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "HotelSec PolicyForge AI"
    assert body["docs"] == "/docs"
    assert body["health"] == "/api/v1/health"
