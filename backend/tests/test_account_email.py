from datetime import timedelta
from hashlib import sha256
import ssl
from urllib.parse import parse_qs, urlsplit

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.db import AccountToken, User, utcnow
from app.main import app
from app.services import account_email


@pytest.fixture
def mail(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "smtp_host", "mail.example.org")
    monkeypatch.setattr(settings, "smtp_from", "account@example.org")
    messages = []
    monkeypatch.setattr(account_email, "send_message", lambda recipient, subject, body: messages.append((recipient, subject, body)))
    return messages


def token_from(message):
    link = next(line for line in message[2].splitlines() if "/#account_token=" in line)
    return parse_qs(urlsplit(link).fragment)["account_token"][0]


def test_email_routes_disabled_without_provider(logged_client, monkeypatch):
    monkeypatch.setattr(get_settings(), "smtp_host", "")
    assert logged_client.get("/api/v1/auth/capabilities").json()["email_delivery_configured"] is False
    assert logged_client.post("/api/v1/auth/email/verify").status_code == 503
    assert logged_client.post("/api/v1/auth/email/change", json={"current_password": "Demo-password-123", "new_email": "new@example.org"}).status_code == 503
    for email in ("pablo@example.org", "missing@example.org"):
        assert logged_client.post("/api/v1/auth/password/reset/request", json={"email": email}).status_code == 503


def test_email_verification_hash_expiry_single_use_and_trusted_link(logged_client, isolated_database, mail):
    assert logged_client.post("/api/v1/auth/email/verify", headers={"Host": "evil.example"}).status_code == 202
    token = token_from(mail[0])
    assert get_settings().frontend_url in mail[0][2] and "evil.example" not in mail[0][2]
    with Session(isolated_database) as db:
        row = db.scalar(select(AccountToken))
        assert row.token_hash == sha256(token.encode()).hexdigest() and token != row.token_hash
    client = TestClient(app)
    result = client.post("/api/v1/auth/account-token/confirm", json={"token": token})
    assert result.status_code == 200 and result.json()["kind"] == "email_verified"
    assert logged_client.get("/api/v1/auth/me").json()["user"]["email_verified"] is True
    assert client.post("/api/v1/auth/account-token/confirm", json={"token": token}).status_code == 400


@pytest.mark.parametrize("new_first", [False, True])
def test_email_change_requires_password_and_both_mailboxes(logged_client, mail, new_first):
    data = {"current_password": "wrong", "new_email": "NEW@example.org"}
    assert logged_client.post("/api/v1/auth/email/change", json=data).status_code == 403
    assert mail == []
    data["current_password"] = "Demo-password-123"
    assert logged_client.post("/api/v1/auth/email/change", json=data).status_code == 202
    assert [item[0] for item in mail] == ["pablo@example.org", "new@example.org"]
    tokens = [token_from(item) for item in mail]
    if new_first:
        tokens.reverse()
    client = TestClient(app)
    first = client.post("/api/v1/auth/account-token/confirm", json={"token": tokens[0]})
    assert first.status_code == 200 and first.json()["kind"] == "email_change_pending"
    assert logged_client.get("/api/v1/auth/me").json()["user"]["email"] == "pablo@example.org"
    assert client.post("/api/v1/auth/account-token/confirm", json={"token": tokens[0]}).status_code == 400
    second = client.post("/api/v1/auth/account-token/confirm", json={"token": tokens[1]})
    assert second.status_code == 200 and second.json()["kind"] == "email_changed"
    assert logged_client.get("/api/v1/auth/me").status_code == 401
    assert client.post("/api/v1/auth/login", json={"email": "pablo@example.org", "password": "Demo-password-123"}).status_code == 401
    login = client.post("/api/v1/auth/login", json={"email": "new@example.org", "password": "Demo-password-123"})
    assert login.status_code == 200 and login.json()["user"]["email_verified"] is True


def test_email_collision_during_confirmation_is_controlled(logged_client, mail):
    assert logged_client.post("/api/v1/auth/email/change", json={"current_password": "Demo-password-123", "new_email": "new@example.org"}).status_code == 202
    client = TestClient(app)
    assert client.post("/api/v1/auth/account-token/confirm", json={"token": token_from(mail[0])}).status_code == 200
    assert client.post("/api/v1/auth/register", json={"name": "Other", "email": "new@example.org", "password": "Other-password-123"}).status_code == 201
    assert client.post("/api/v1/auth/account-token/confirm", json={"token": token_from(mail[1])}).status_code == 409
    assert logged_client.get("/api/v1/auth/me").json()["user"]["email"] == "pablo@example.org"


def test_recovery_generic_response_and_session_revocation(logged_client, mail):
    client = TestClient(app)
    missing = client.post("/api/v1/auth/password/reset/request", json={"email": "missing@example.org"})
    known = client.post("/api/v1/auth/password/reset/request", json={"email": "pablo@example.org"})
    assert missing.status_code == known.status_code == 202 and missing.json() == known.json()
    assert len(mail) == 1
    token = token_from(mail[0])
    assert token not in known.text
    assert client.post("/api/v1/auth/account-token/confirm", json={"token": token}).status_code == 422
    result = client.post("/api/v1/auth/account-token/confirm", json={"token": token, "new_password": "Recovered-password-456"})
    assert result.status_code == 200 and result.json()["kind"] == "password_reset"
    assert logged_client.get("/api/v1/auth/me").status_code == 401
    assert client.post("/api/v1/auth/account-token/confirm", json={"token": token, "new_password": "Recovered-password-456"}).status_code == 400
    assert client.post("/api/v1/auth/login", json={"email": "pablo@example.org", "password": "Recovered-password-456"}).status_code == 200
    assert any("Contrasena actualizada" in item[1] for item in mail)


def test_expired_and_superseded_tokens_cannot_change_password(logged_client, mail, isolated_database):
    client = TestClient(app)
    assert client.post("/api/v1/auth/password/reset/request", json={"email": "pablo@example.org"}).status_code == 202
    old = token_from(mail[0])
    assert client.post("/api/v1/auth/password/reset/request", json={"email": "pablo@example.org"}).status_code == 202
    new = token_from(mail[1])
    assert client.post("/api/v1/auth/account-token/confirm", json={"token": old, "new_password": "Recovered-password-456"}).status_code == 400
    with Session(isolated_database) as db:
        row = db.get(AccountToken, sha256(new.encode()).hexdigest())
        row.expires_at = utcnow() - timedelta(minutes=1)
        db.commit()
    assert client.post("/api/v1/auth/account-token/confirm", json={"token": new, "new_password": "Recovered-password-456"}).status_code == 400


def test_password_change_invalidates_outstanding_links(logged_client, mail):
    client = TestClient(app)
    client.post("/api/v1/auth/password/reset/request", json={"email": "pablo@example.org"})
    token = token_from(mail[0])
    assert logged_client.post("/api/v1/auth/password", json={"current_password": "Demo-password-123", "new_password": "Changed-password-456"}).status_code == 200
    assert client.post("/api/v1/auth/account-token/confirm", json={"token": token, "new_password": "Recovered-password-456"}).status_code == 400


def test_mail_failures_do_not_leak_links_or_credentials(logged_client, mail, monkeypatch, caplog):
    def fail(*args):
        raise RuntimeError("do-not-log-password-or-token")
    monkeypatch.setattr(account_email, "send_message", fail)
    result = logged_client.post("/api/v1/auth/password/reset/request", json={"email": "pablo@example.org"})
    assert result.status_code == 202
    assert "do-not-log" not in result.text + caplog.text
    assert "pablo@example.org" not in caplog.text


def test_reset_origin_token_rate_limit_and_no_get_side_effect(logged_client, mail):
    assert logged_client.post("/api/v1/auth/password/reset/request", json={"email": "pablo@example.org"}, headers={"Origin": "https://evil.example"}).status_code == 403
    assert logged_client.get("/api/v1/auth/account-token/confirm?token=" + "x" * 43).status_code == 405
    client = TestClient(app)
    for _ in range(10):
        assert client.post("/api/v1/auth/account-token/confirm", json={"token": "x" * 43}).status_code == 400
    assert client.post("/api/v1/auth/account-token/confirm", json={"token": "x" * 43}).status_code == 429


@pytest.mark.parametrize("mode", ["starttls", "ssl"])
def test_smtp_requires_validated_tls(mode, monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "smtp_host", "mail.example.org")
    monkeypatch.setattr(settings, "smtp_from", "account@example.org")
    monkeypatch.setattr(settings, "smtp_mode", mode)
    events = []
    class SMTP:
        def __init__(self, host, port, **kwargs):
            events.append((host, port, kwargs))
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def ehlo(self): pass
        def starttls(self, **kwargs): events.append(kwargs)
        def send_message(self, message): events.append(message["To"])
    monkeypatch.setattr(account_email.smtplib, "SMTP", SMTP)
    monkeypatch.setattr(account_email.smtplib, "SMTP_SSL", SMTP)
    account_email.send_message("pablo@example.org", "Account", "No secret")
    contexts = [item["context"] for item in events if isinstance(item, dict) and "context" in item]
    contexts += [item[2]["context"] for item in events if isinstance(item, tuple) and "context" in item[2]]
    assert len(contexts) == 1 and contexts[0].verify_mode == ssl.CERT_REQUIRED and contexts[0].check_hostname


def test_smtp_rejects_plaintext_modes_and_incomplete_credentials():
    with pytest.raises(ValueError): Settings(_env_file=None, SMTP_MODE="plain")
    with pytest.raises(ValueError): Settings(_env_file=None, SMTP_USERNAME="user", SMTP_PASSWORD="")
    with pytest.raises(ValueError): Settings(_env_file=None, SMTP_HOST="smtp://user:password@example.org")
