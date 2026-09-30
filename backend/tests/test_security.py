from fastapi.testclient import TestClient
from sqlalchemy import select
from app.main import app
from app.db import LoginSession, User
from sqlalchemy.orm import Session


def test_authentication_and_csrf(logged_client):
    assert TestClient(app).get("/api/v1/auth/me").status_code == 401
    response = logged_client.get("/api/v1/auth/me")
    assert response.status_code == 200
    assert "password_hash" not in response.text
    no_csrf = TestClient(app)
    no_csrf.cookies.update(logged_client.cookies)
    assert no_csrf.post("/api/v1/auth/logout").status_code == 403
    assert logged_client.get("/api/v1/auth/admin/users").status_code == 403
    assert logged_client.post("/api/v1/auth/logout").status_code == 204
    assert logged_client.get("/api/v1/auth/me").status_code == 401


def test_hashes_and_role_cannot_be_forged(logged_client, isolated_database):
    with Session(isolated_database) as db:
        user = db.scalar(select(User))
        assert user.password_hash.startswith("$argon2id$")
        assert "Demo-password" not in user.password_hash
        session = db.scalar(select(LoginSession))
        assert session.token_hash != logged_client.cookies.get("hotelsec_session")
    response = logged_client.post("/api/v1/auth/register", json={"name": "Attacker", "email": "other@example.org", "password": "Demo-password-123", "role": "admin"})
    assert response.status_code == 422


def test_login_origin_rate_limit_and_revoke(logged_client):
    evil = logged_client.post("/api/v1/auth/logout", headers={"Origin": "https://evil.example"})
    assert evil.status_code == 403
    for _ in range(9):
        logged_client.post("/api/v1/auth/login", json={"email": "pablo@example.org", "password": "Wrong-password-123"})
    assert logged_client.post("/api/v1/auth/login", json={"email": "pablo@example.org", "password": "Wrong-password-123"}).status_code == 429


def test_account_erasure(logged_client, isolated_database):
    assert logged_client.request("DELETE", "/api/v1/auth/account", json={"password": "Wrong-password-123"}).status_code == 403
    assert logged_client.request("DELETE", "/api/v1/auth/account", json={"password": "Demo-password-123"}).status_code == 204
    assert logged_client.get("/api/v1/auth/me").status_code == 401
    with Session(isolated_database) as db:
        assert db.scalar(select(User)) is None
        assert db.scalar(select(LoginSession)) is None
