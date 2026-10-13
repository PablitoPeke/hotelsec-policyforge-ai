from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.security import _buckets
from app.db import AiUsage, User
from app.main import app
from app.services.usage_service import reserve_ai_request
from tests.test_product import payload


def user_ids(engine):
    with Session(engine) as db:
        return list(db.scalars(select(User.id)))


def reserve(engine, user_id):
    with Session(engine) as db:
        reserve_ai_request(db, db.get(User, user_id))


def test_global_quota_shared_between_users_and_persists_across_sessions(logged_client, isolated_database, monkeypatch):
    monkeypatch.setattr(get_settings(), "ai_global_daily_limit", 2)
    other = TestClient(app)
    assert other.post("/api/v1/auth/register", json={"name": "Other", "email": "other@example.org", "password": "Other-password-123"}).status_code == 201
    ids = user_ids(isolated_database)
    reserve(isolated_database, ids[0]); reserve(isolated_database, ids[1])
    _buckets.clear()
    with pytest.raises(HTTPException) as exception:
        reserve(isolated_database, ids[0])
    assert exception.value.status_code == 429 and int(exception.value.headers["Retry-After"]) > 0
    with Session(isolated_database) as db:
        assert db.scalar(select(AiUsage.used).where(AiUsage.owner_id.is_(None))) == 2


def test_user_quota_rejection_rolls_back_global_increment(logged_client, isolated_database, monkeypatch):
    monkeypatch.setattr(get_settings(), "ai_global_daily_limit", 5)
    monkeypatch.setattr(get_settings(), "ai_requests_per_hour", 1)
    uid = user_ids(isolated_database)[0]
    reserve(isolated_database, uid)
    with pytest.raises(HTTPException): reserve(isolated_database, uid)
    with Session(isolated_database) as db:
        assert [row.used for row in db.scalars(select(AiUsage))] == [1, 1]


def test_quota_reservation_is_atomic_under_concurrency(logged_client, isolated_database, monkeypatch):
    monkeypatch.setattr(get_settings(), "ai_global_daily_limit", 3)
    monkeypatch.setattr(get_settings(), "ai_requests_per_hour", 3)
    uid = user_ids(isolated_database)[0]
    def attempt(_):
        try:
            reserve(isolated_database, uid)
            return True
        except HTTPException as exception:
            assert exception.status_code == 429
            return False
    with ThreadPoolExecutor(max_workers=4) as pool:
        assert sum(pool.map(attempt, range(10))) == 3
    with Session(isolated_database) as db:
        assert [row.used for row in db.scalars(select(AiUsage))] == [3, 3]


def test_utc_day_and_hour_rollover(logged_client, isolated_database, monkeypatch):
    monkeypatch.setattr(get_settings(), "ai_global_daily_limit", 1)
    monkeypatch.setattr(get_settings(), "ai_requests_per_hour", 1)
    now = datetime(2026, 10, 13, 23, 59, tzinfo=timezone.utc)
    monkeypatch.setattr("app.services.usage_service.utcnow", lambda: now)
    uid = user_ids(isolated_database)[0]
    reserve(isolated_database, uid)
    now += timedelta(minutes=2)
    reserve(isolated_database, uid)
    with Session(isolated_database) as db:
        assert len(list(db.scalars(select(AiUsage)))) == 4


def test_kill_switch_prevents_paid_calls_but_allows_rules(logged_client, isolated_database, monkeypatch):
    monkeypatch.setattr(get_settings(), "openai_api_key", "fake-never-transmitted")
    monkeypatch.setattr(get_settings(), "ai_global_daily_limit", 0)
    def unexpected(*args, **kwargs): raise AssertionError("No provider calls allowed")
    monkeypatch.setattr("httpx.post", unexpected)
    result = logged_client.post("/api/v1/records", json={"assessment": payload(), "use_ai": True})
    assert result.status_code == 503
    assert logged_client.post("/api/v1/records", json={"assessment": payload(), "use_ai": False, "description": "No usamos MFA."}).status_code == 201
    with Session(isolated_database) as db:
        assert list(db.scalars(select(AiUsage))) == []


def test_invalid_input_and_unknown_company_do_not_consume_quota(logged_client, isolated_database, monkeypatch):
    monkeypatch.setattr(get_settings(), "openai_api_key", "fake-never-transmitted")
    data = payload(); data["hotel_profile"]["rooms_count"] = -1
    assert logged_client.post("/api/v1/records", json={"assessment": data, "use_ai": True}).status_code == 422
    assert logged_client.post("/api/v1/records", json={"assessment": payload(), "company_id": "missing", "use_ai": True}).status_code == 404
    assert logged_client.post("/api/v1/ai/analyze-description", json={}).status_code == 422
    with Session(isolated_database) as db:
        assert list(db.scalars(select(AiUsage))) == []


def test_delete_account_removes_personal_usage_but_keeps_global_ceiling(logged_client, isolated_database, monkeypatch):
    monkeypatch.setattr(get_settings(), "ai_global_daily_limit", 1)
    reserve(isolated_database, user_ids(isolated_database)[0])
    assert logged_client.request("DELETE", "/api/v1/auth/account", json={"password": "Demo-password-123"}).status_code == 204
    with Session(isolated_database) as db:
        remaining = list(db.scalars(select(AiUsage)))
        assert len(remaining) == 1 and remaining[0].owner_id is None and remaining[0].used == 1


def test_settings_errors_do_not_echo_secrets():
    marker = "do-not-print-api-secret"
    with pytest.raises(ValueError) as exception:
        Settings(_env_file=None, OPENAI_API_KEY=marker, SMTP_MODE="invalid")
    assert marker not in str(exception.value)
