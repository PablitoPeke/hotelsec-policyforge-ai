from functools import lru_cache
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, create_engine, event
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from app.core.config import get_settings


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def identifier() -> str:
    return str(uuid4())


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=identifier)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(512))
    role: Mapped[str] = mapped_column(String(20), default="hotel")
    organization_name: Mapped[str] = mapped_column(String(120), default="", server_default="")
    job_title: Mapped[str] = mapped_column(String(120), default="", server_default="")
    email_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class LoginSession(Base):
    __tablename__ = "login_sessions"
    token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    public_id: Mapped[str] = mapped_column(String(36), default=identifier, unique=True, index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    csrf_token: Mapped[str] = mapped_column(String(64))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=utcnow)
    device_label: Mapped[str] = mapped_column(String(80), default="Navegador", server_default="Sesion anterior")


class AccountToken(Base):
    __tablename__ = "account_tokens"
    token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    kind: Mapped[str] = mapped_column(String(30))
    issued_email: Mapped[str] = mapped_column(String(254))
    target_email: Mapped[str] = mapped_column(String(254))
    change_id: Mapped[str | None] = mapped_column(String(36), index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class AiUsage(Base):
    __tablename__ = "ai_usage"
    bucket: Mapped[str] = mapped_column(String(100), primary_key=True)
    owner_id: Mapped[str | None] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    used: Mapped[int] = mapped_column(Integer, default=0)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


class Company(Base):
    __tablename__ = "companies"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=identifier)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    municipality: Mapped[str] = mapped_column(String(80))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class SavedAssessment(Base):
    __tablename__ = "saved_assessments"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=identifier)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)
    bundle: Mapped[dict] = mapped_column(JSON)
    # Status lives outside the immutable result snapshot so progress can change independently.
    action_statuses: Mapped[dict] = mapped_column(JSON, default=dict)


class AuditEvent(Base):
    __tablename__ = "audit_events"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=identifier)
    user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    event: Mapped[str] = mapped_column(String(80))
    resource_id: Mapped[str | None] = mapped_column(String(36))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


@lru_cache
def get_engine():
    url = get_settings().database_url
    options = {"check_same_thread": False} if url.startswith("sqlite") else {}
    engine = create_engine(url, pool_pre_ping=True, connect_args=options)
    if url.startswith("sqlite"):
        @event.listens_for(engine, "connect")
        def enable_foreign_keys(connection, _):
            connection.execute("PRAGMA foreign_keys=ON")
    return engine


def get_db():
    with Session(get_engine(), expire_on_commit=False) as session:
        yield session


def audit(db: Session, user_id: str | None, event: str, resource_id: str | None = None):
    db.add(AuditEvent(user_id=user_id, event=event, resource_id=resource_id))
