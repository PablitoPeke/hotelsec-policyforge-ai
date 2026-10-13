import json
import os
from pathlib import Path
import subprocess
import sys

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session

from app.db import AuditEvent, LoginSession, User
from app.main import app
from tests.test_product import payload


PASSWORD = "Demo-password-123"


def another_session():
    client = TestClient(app)
    result = client.post("/api/v1/auth/login", json={"email": "pablo@example.org", "password": PASSWORD})
    assert result.status_code == 200
    client.headers["X-CSRF-Token"] = result.json()["csrf_token"]
    return client


def test_profile_edit_is_persistent_and_keeps_assessment(logged_client, isolated_database):
    record = logged_client.post("/api/v1/records", json={"assessment": payload()}).json()
    result = logged_client.patch("/api/v1/auth/profile", json={
        "name": "  Pablo Cortes  ", "organization_name": "  Hotel Lanzarote  ", "job_title": "Director",
    })
    assert result.status_code == 200
    assert result.json()["name"] == "Pablo Cortes"
    assert result.json()["organization_name"] == "Hotel Lanzarote"
    assert result.json()["email_verified"] is False
    assert logged_client.get("/api/v1/auth/me").json()["user"] == result.json()
    assert logged_client.get(f"/api/v1/records/{record['id']}").json()["input"] == record["input"]
    with Session(isolated_database) as db:
        assert db.scalar(select(User)).job_title == "Director"
        assert db.scalar(select(AuditEvent).where(AuditEvent.event == "profile.updated"))


@pytest.mark.parametrize("data", [{}, {"name": " "}, {"name": None}, {"name": "x" * 121},
                                  {"job_title": None}, {"role": "admin"}, {"id": "other"},
                                  {"email": "new@example.org"}, {"organization_name": 123}])
def test_profile_rejects_invalid_or_privileged_fields(logged_client, data):
    assert logged_client.patch("/api/v1/auth/profile", json=data).status_code == 422
    assert logged_client.get("/api/v1/auth/me").json()["user"]["role"] == "hotel"


def test_profile_authentication_origin_and_csrf(logged_client):
    assert TestClient(app).patch("/api/v1/auth/profile", json={"name": "Changed"}).status_code == 401
    assert logged_client.patch("/api/v1/auth/profile", json={"name": "Changed"}, headers={"X-CSRF-Token": ""}).status_code == 403
    assert logged_client.patch("/api/v1/auth/profile", json={"name": "Changed"}, headers={"Origin": "https://evil.example"}).status_code == 403
    assert logged_client.get("/api/v1/auth/me").json()["user"]["name"] == "Pablo Demo"


def test_password_change_rotates_session_and_revokes_all_previous(logged_client):
    other = another_session()
    previous_cookie = logged_client.cookies.get("hotelsec_session")
    previous_csrf = logged_client.headers["X-CSRF-Token"]
    result = logged_client.post("/api/v1/auth/password", json={"current_password": PASSWORD, "new_password": "Replacement-password-456"})
    assert result.status_code == 200
    assert logged_client.cookies.get("hotelsec_session") != previous_cookie
    assert result.json()["csrf_token"] != previous_csrf
    assert other.get("/api/v1/auth/me").status_code == 401
    assert logged_client.patch("/api/v1/auth/profile", json={"name": "Test"}).status_code == 403
    logged_client.headers["X-CSRF-Token"] = result.json()["csrf_token"]
    assert logged_client.patch("/api/v1/auth/profile", json={"name": "Test"}).status_code == 200
    assert TestClient(app).post("/api/v1/auth/login", json={"email": "pablo@example.org", "password": PASSWORD}).status_code == 401
    assert TestClient(app).post("/api/v1/auth/login", json={"email": "pablo@example.org", "password": "Replacement-password-456"}).status_code == 200


@pytest.mark.parametrize("data,status", [
    ({"current_password": "Incorrect-password", "new_password": "Replacement-password-456"}, 403),
    ({"current_password": PASSWORD, "new_password": PASSWORD}, 422),
    ({"current_password": PASSWORD, "new_password": "secret123"}, 422),
    ({"current_password": PASSWORD, "new_password": "x" * 129}, 422),
])
def test_password_change_rejects_invalid_credentials_without_echoing_them(logged_client, data, status):
    result = logged_client.post("/api/v1/auth/password", json=data)
    assert result.status_code == status
    assert data["current_password"] not in result.text
    assert data["new_password"] not in result.text
    assert logged_client.get("/api/v1/auth/me").status_code == 200


def test_sessions_expose_only_public_identifiers_and_are_owner_scoped(logged_client, isolated_database):
    other = another_session()
    sessions = logged_client.get("/api/v1/auth/sessions").json()
    assert len(sessions) == 2 and sum(item["current"] for item in sessions) == 1
    with Session(isolated_database) as db:
        for row in db.scalars(select(LoginSession)):
            assert row.token_hash not in json.dumps(sessions)
            assert row.csrf_token not in json.dumps(sessions)
    intruder = TestClient(app)
    registered = intruder.post("/api/v1/auth/register", json={"name": "Other", "email": "other@example.org", "password": "Other-password-123"})
    intruder.headers["X-CSRF-Token"] = registered.json()["csrf_token"]
    target = next(item["id"] for item in sessions if not item["current"])
    assert intruder.delete("/api/v1/auth/sessions/" + target).status_code == 404
    assert logged_client.delete("/api/v1/auth/sessions/" + target).status_code == 204
    assert other.get("/api/v1/auth/me").status_code == 401
    assert logged_client.get("/api/v1/auth/me").status_code == 200


def test_revoke_other_sessions_requires_password_and_keeps_current(logged_client):
    other = another_session()
    assert logged_client.post("/api/v1/auth/sessions/revoke-others", json={"current_password": "incorrect"}).status_code == 403
    assert other.get("/api/v1/auth/me").status_code == 200
    assert logged_client.post("/api/v1/auth/sessions/revoke-others", json={"current_password": PASSWORD}).status_code == 204
    assert other.get("/api/v1/auth/me").status_code == 401
    assert logged_client.get("/api/v1/auth/me").status_code == 200


def test_export_owns_all_rows_and_excludes_authentication_secrets(logged_client):
    owned = logged_client.post("/api/v1/records", json={"assessment": payload()}).json()
    outsider = TestClient(app)
    registered = outsider.post("/api/v1/auth/register", json={"name": "Private Other", "email": "other@example.org", "password": "Other-password-123"})
    outsider.headers["X-CSRF-Token"] = registered.json()["csrf_token"]
    data = payload()
    data["hotel_profile"]["business_name"] = "Other Hotel Must Not Be Exported"
    foreign = outsider.post("/api/v1/records", json={"assessment": data}).json()
    assert logged_client.post("/api/v1/auth/export", json={"current_password": "incorrect"}).status_code == 403
    response = logged_client.post("/api/v1/auth/export", json={"current_password": PASSWORD})
    assert response.status_code == 200 and response.headers["cache-control"] == "no-store"
    assert response.json()["profile"]["email"] == "pablo@example.org"
    assert [item["id"] for item in response.json()["assessments"]] == [owned["id"]]
    for secret in ("password_hash", "csrf_token", "token_hash", PASSWORD, foreign["id"], "Other Hotel Must Not Be Exported"):
        assert secret not in response.text


def test_sensitive_operations_are_rate_limited(logged_client):
    for _ in range(10):
        assert logged_client.post("/api/v1/auth/export", json={"current_password": "incorrect"}).status_code == 403
    assert logged_client.post("/api/v1/auth/export", json={"current_password": PASSWORD}).status_code == 429


def test_migration_preserves_existing_user_and_session(tmp_path):
    backend = Path(__file__).resolve().parents[1]
    url = f"sqlite:///{(tmp_path / 'legacy.sqlite3').as_posix()}"
    env = {**os.environ, "DATABASE_URL": url, "APP_ENV": "development"}
    command = [sys.executable, "-m", "alembic", "-c", str(backend / "alembic.ini"), "upgrade"]
    assert subprocess.run(command + ["0001"], cwd=backend, env=env, capture_output=True).returncode == 0
    engine = create_engine(url)
    with engine.begin() as connection:
        connection.execute(text("INSERT INTO users VALUES ('u1', 'Legacy User', 'legacy@example.org', 'legacy-test-hash', 'hotel', CURRENT_TIMESTAMP)"))
        connection.execute(text("INSERT INTO login_sessions VALUES ('hash1', 'u1', 'csrf1', '2099-01-01 00:00:00')"))
    result = subprocess.run(command + ["head"], cwd=backend, env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    with engine.connect() as connection:
        user = connection.execute(text("SELECT * FROM users")).mappings().one()
        session = connection.execute(text("SELECT * FROM login_sessions")).mappings().one()
    assert user["password_hash"] == "legacy-test-hash" and user["email"] == "legacy@example.org"
    assert user["organization_name"] == "" and user["email_verified_at"] is None
    assert session["token_hash"] == "hash1" and session["csrf_token"] == "csrf1"
    assert len(session["public_id"]) == 36 and session["created_at"] is None
    # A rollback to the previous API can still insert sessions without the new fields.
    with engine.begin() as connection:
        connection.execute(text("INSERT INTO login_sessions (token_hash, user_id, csrf_token, expires_at) VALUES ('hash2', 'u1', 'csrf2', '2099-01-01 00:00:00')"))
        assert connection.execute(text("SELECT public_id FROM login_sessions WHERE token_hash = 'hash2'")).scalar()
    engine.dispose()
