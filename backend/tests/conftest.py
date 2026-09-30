import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.main import app
from app.db import Base, get_db
from app.core.config import get_settings
from app.core.security import _buckets


@pytest.fixture(autouse=True)
def isolated_database(tmp_path, monkeypatch, request):
    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}", connect_args={"check_same_thread": False})
    @event.listens_for(engine, "connect")
    def foreign_keys(connection, _):
        connection.execute("PRAGMA foreign_keys=ON")
    Base.metadata.create_all(engine)
    def db_override():
        with Session(engine, expire_on_commit=False) as db:
            yield db
    app.dependency_overrides[get_db] = db_override
    monkeypatch.setattr(get_settings(), "openai_api_key", None)
    monkeypatch.setattr(get_settings(), "cookie_secure", False)
    _buckets.clear()
    legacy_client = getattr(request.module, "client", None)
    if legacy_client is not None:
        legacy_client.cookies.clear()
        result = legacy_client.post("/api/v1/auth/register", json={"name": "Prueba", "email": "prueba@example.org", "password": "Test-password-123"})
        assert result.status_code == 201, result.text
        legacy_client.headers["X-CSRF-Token"] = result.json()["csrf_token"]
    yield engine
    app.dependency_overrides.clear()
    engine.dispose()


@pytest.fixture
def logged_client(isolated_database):
    with TestClient(app) as client:
        response = client.post("/api/v1/auth/register", json={"name": "Pablo Demo", "email": "pablo@example.org", "password": "Demo-password-123"})
        assert response.status_code == 201, response.text
        client.headers["X-CSRF-Token"] = response.json()["csrf_token"]
        yield client
