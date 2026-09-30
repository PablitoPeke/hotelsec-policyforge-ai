import os
import subprocess
import sys
from pathlib import Path
import pytest
from sqlalchemy import select, inspect, create_engine
from app.core.config import Settings, get_settings
from app.db import User
from sqlalchemy.orm import Session


def test_production_rejects_insecure_configuration():
    with pytest.raises(ValueError, match='Production requires HTTPS'):
        Settings(_env_file=None, APP_ENV='production', APP_URL='http://example.org', COOKIE_SECURE=False)
    secure = Settings(_env_file=None, APP_ENV='production', APP_URL='https://hotel.example.org',
        COOKIE_SECURE=True, CORS_ORIGINS='https://hotel.example.org', DATABASE_URL='postgresql+psycopg://user:private@db/hotel')
    assert secure.cookie_secure


def test_admin_only_authorized_and_password_spaces_preserved(logged_client, isolated_database):
    assert logged_client.get('/api/v1/auth/admin/users').status_code == 403
    with Session(isolated_database) as db:
        user = db.scalar(select(User))
        user.role = 'admin'
        db.commit()
    assert logged_client.get('/api/v1/auth/admin/users').status_code == 200
    client = logged_client
    registered = client.post('/api/v1/auth/register', json={'name': 'Space Password', 'email': 'space@example.org', 'password': '  Valid-password-123  '})
    assert registered.status_code == 201
    assert client.post('/api/v1/auth/login', json={'email': 'space@example.org', 'password': 'Valid-password-123'}).status_code == 401
    assert client.post('/api/v1/auth/login', json={'email': 'space@example.org', 'password': '  Valid-password-123  '}).status_code == 200


def test_ai_opt_out_does_not_send_text(logged_client, monkeypatch):
    from tests.test_product import payload
    monkeypatch.setattr(get_settings(), 'openai_api_key', 'fake-not-a-secret')
    def unexpected(*args, **kwargs):
        raise AssertionError('No consent: must not call provider')
    monkeypatch.setattr('httpx.post', unexpected)
    response = logged_client.post('/api/v1/records', json={'assessment': payload(), 'description': 'No usamos MFA.', 'use_ai': False})
    assert response.status_code == 201
    assert response.json()['description_by_ai'] is False


def test_migrations_from_empty_database_and_idempotence(tmp_path):
    root = Path(__file__).resolve().parents[1]
    url = f'sqlite:///{(tmp_path / "migrations.sqlite3").as_posix()}'
    env = {**os.environ, 'DATABASE_URL': url, 'APP_ENV': 'development'}
    for _ in range(2):
        result = subprocess.run([sys.executable, '-m', 'alembic', '-c', str(root / 'alembic.ini'), 'upgrade', 'head'], cwd=root, env=env, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
    engine = create_engine(url)
    assert set(inspect(engine).get_table_names()) >= {'users', 'login_sessions', 'companies', 'saved_assessments', 'audit_events', 'alembic_version'}
    engine.dispose()
