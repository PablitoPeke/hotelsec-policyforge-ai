import json
import stat
import os

from fastapi.testclient import TestClient
import httpx
import pytest
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db import User, SavedAssessment
from app.main import app
from scripts.setup_production import create_configuration, validate_domain
from scripts.verify_deployment import validate_origin, verify


@pytest.mark.parametrize('domain', ['178.105.149.202', 'https://hotel.es', 'hotel.es/path',
                                     'hotel.example.org', 'host..es', '-host.es', 'host\nes'])
def test_production_configuration_rejects_invalid_domain(domain):
    with pytest.raises(ValueError):
        validate_domain(domain)


def test_production_configuration_does_not_overwrite_secrets(tmp_path):
    target = tmp_path / '.env.production'
    assert validate_domain(' Demo.Hotel.es. ') == 'demo.hotel.es'
    assert create_configuration('demo.hotel.es', target)
    content = target.read_text()
    settings = dict(line.split('=', 1) for line in content.splitlines())
    assert settings['DOMAIN'] == 'demo.hotel.es'
    assert len(bytes.fromhex(settings['POSTGRES_PASSWORD'])) == 32
    assert settings['OPENAI_API_KEY'] == ''
    assert not create_configuration('other.hotel.es', target)
    assert target.read_text() == content
    if os.name != 'nt':
        assert stat.S_IMODE(target.stat().st_mode) == 0o600


@pytest.mark.parametrize('origin', ['http://hotel.es', 'https://user:secret@hotel.es',
                                    'https://hotel.es/api', 'https://hotel.es?key=secret',
                                    'ftp://hotel.es', 'https://hotel.es:invalid', 'https://hotel.es#fragment'])
def test_deployment_check_rejects_unsafe_origins(origin):
    with pytest.raises(ValueError):
        validate_origin(origin)


@pytest.mark.parametrize('origin', ['http://localhost:8085', 'http://127.0.0.1:8085', 'https://hotel.es/'])
def test_deployment_check_accepts_valid_origins(origin):
    assert validate_origin(origin) == origin.rstrip('/')


@pytest.mark.parametrize('with_ai', [False, True])
def test_deployment_check_cleans_accounts_even_when_ai_falls_back(isolated_database, monkeypatch, with_ai):
    monkeypatch.setattr(get_settings(), 'cors_origins_raw', 'http://localhost:8085')
    with TestClient(app) as first, TestClient(app) as second:
        report = verify(first, second, 'http://localhost:8085', with_ai)
    assert report['passed'] is (not with_ai)
    assert report['cleanup'] == ['account_deleted', 'account_deleted']
    assert 'csrf_logout_history_and_persisted_progress' in report['checks'] or with_ai
    if with_ai:
        assert 'fallback' in report['failure']
    with Session(isolated_database) as db:
        assert db.scalar(select(func.count()).select_from(User)) == 0
        assert db.scalar(select(func.count()).select_from(SavedAssessment)) == 0
    evidence = json.dumps(report)
    assert 'csrf_token' not in evidence and '@example.org' not in evidence and 'password' not in evidence


def test_deployment_check_cleans_accounts_after_http_failure(isolated_database, monkeypatch):
    monkeypatch.setattr(get_settings(), 'cors_origins_raw', 'http://localhost:8085')
    with TestClient(app) as first, TestClient(app) as second:
        original = first.post
        def fail_record(url, **kwargs):
            if url.endswith('/records'):
                return httpx.Response(503, json={'secret': 'DO-NOT-EXPORT'})
            return original(url, **kwargs)
        monkeypatch.setattr(first, 'post', fail_record)
        report = verify(first, second, 'http://localhost:8085')
    assert report['passed'] is False
    assert report['cleanup'] == ['account_deleted', 'account_deleted']
    assert 'DO-NOT-EXPORT' not in json.dumps(report)


def test_deployment_check_accepts_all_ai_stages_only_when_successful(isolated_database, monkeypatch):
    monkeypatch.setattr(get_settings(), 'cors_origins_raw', 'http://localhost:8085')
    monkeypatch.setattr(get_settings(), 'openai_api_key', 'fake-for-tests-only')
    calls = []
    def respond(url, **kwargs):
        packet = kwargs['json']
        calls.append(packet['instructions'])
        data = json.loads(packet['input'])
        if 'Extrae SOLO' in packet['instructions']:
            text = json.dumps({'hotel_profile': {}, 'security_controls': {'uses_mfa': True}})
        elif 'Adapta estas' in packet['instructions']:
            text = json.dumps({'policies': [{key: item[key] for key in ('objective', 'scope', 'controls')}
                                             for item in data['pack']['policies']]})
        else:
            text = 'Resumen simulado para la prueba automatizada.'
        return httpx.Response(200, json={'output': [{'content': [{'type': 'output_text', 'text': text}]}]},
                              request=httpx.Request('POST', url))
    monkeypatch.setattr(httpx, 'post', respond)
    with TestClient(app) as first, TestClient(app) as second:
        report = verify(first, second, 'http://localhost:8085', with_ai=True)
    assert report['passed'] is True
    assert 'live_ai_extraction_policies_and_summary' in report['checks']
    assert report['cleanup'] == ['account_deleted', 'account_deleted']
    assert len(calls) == 3


def test_deployment_check_reports_missing_cleanup(isolated_database, monkeypatch):
    monkeypatch.setattr(get_settings(), 'cors_origins_raw', 'http://localhost:8085')
    with TestClient(app) as first, TestClient(app) as second:
        original = second.request
        def fail_delete(method, url, **kwargs):
            if method == 'DELETE' and url.endswith('/auth/account'):
                return httpx.Response(503)
            return original(method, url, **kwargs)
        monkeypatch.setattr(second, 'request', fail_delete)
        report = verify(first, second, 'http://localhost:8085')
    assert report['passed'] is False
    assert 'account_cleanup_failed' in report['cleanup']
