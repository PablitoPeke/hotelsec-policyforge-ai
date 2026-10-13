"""Email verification and recovery, disabled until SMTP is configured."""
from datetime import timezone
from hashlib import sha256
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, Response
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.v1.endpoints.account import CurrentPassword, reauthenticate
from app.core.config import get_settings
from app.core.security import COOKIE, get_current_user, limit, password_hasher, require_origin, verify_password
from app.db import AccountToken, LoginSession, User, audit, get_db, utcnow
from app.services.account_email import add_token, deliver_link, deliver_password_notice

router = APIRouter(prefix="/auth")
ACCEPTED = {"message": "Solicitud recibida. Revisa tu correo si la entrega esta disponible."}
INVALID = "Enlace no valido o caducado."


class EmailChange(CurrentPassword):
    new_email: EmailStr


class RecoveryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr


class ConfirmToken(BaseModel):
    model_config = ConfigDict(extra="forbid")
    token: str = Field(min_length=32, max_length=256)
    new_password: str | None = Field(default=None, min_length=12, max_length=128)


def require_email():
    if not get_settings().email_delivery_configured:
        raise HTTPException(503, "El servicio de correo aun no esta configurado.")


@router.get("/capabilities")
def capabilities():
    return {"email_delivery_configured": get_settings().email_delivery_configured,
            "email_change_requires_both_mailboxes": True}


@router.post("/email/verify", status_code=202)
def request_verification(tasks: BackgroundTasks, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_email()
    limit(f"mail:{user.id}", 3, 3600)
    if user.email_verified_at is not None:
        return {"message": "Correo ya verificado."}
    db.execute(delete(AccountToken).where(AccountToken.user_id == user.id, AccountToken.kind == "verify_email"))
    raw = add_token(db, user, "verify_email")
    audit(db, user.id, "email.verification_requested")
    db.commit()
    tasks.add_task(deliver_link, user.email, "verify_email", raw)
    return ACCEPTED


@router.post("/email/change", status_code=202)
def request_email_change(payload: EmailChange, tasks: BackgroundTasks, user: User = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    require_email()
    reauthenticate(payload, user, db)
    limit(f"mail:{user.id}", 3, 3600)
    target = str(payload.new_email).lower()
    if target == user.email or db.scalar(select(User.id).where(User.email == target)):
        raise HTTPException(409, "No se puede solicitar el cambio con esos datos.")
    db.execute(delete(AccountToken).where(AccountToken.user_id == user.id,
               AccountToken.kind.in_(("email_approve", "email_change"))))
    change_id = str(uuid4())
    old = add_token(db, user, "email_approve", target, change_id)
    new = add_token(db, user, "email_change", target, change_id)
    audit(db, user.id, "email.change_requested")
    db.commit()
    tasks.add_task(deliver_link, user.email, "email_approve", old)
    tasks.add_task(deliver_link, target, "email_change", new)
    return {"message": "Solicitud recibida. Debes confirmar el enlace de ambos correos."}


@router.post("/password/reset/request", status_code=202)
def request_recovery(payload: RecoveryRequest, request: Request, tasks: BackgroundTasks, db: Session = Depends(get_db)):
    require_origin(request)
    require_email()
    limit(f"recovery-ip:{request.client.host}", 5, 900)
    email = str(payload.email).lower()
    limit("recovery-mail:" + sha256(email.encode()).hexdigest(), 3, 3600)
    user = db.scalar(select(User).where(User.email == email))
    if user:
        db.execute(delete(AccountToken).where(AccountToken.user_id == user.id, AccountToken.kind == "reset_password"))
        raw = add_token(db, user, "reset_password")
        audit(db, user.id, "password.recovery_requested")
        db.commit()
        tasks.add_task(deliver_link, user.email, "reset_password", raw)
    return ACCEPTED


@router.post("/account-token/confirm")
def confirm_token(payload: ConfirmToken, request: Request, response: Response, tasks: BackgroundTasks,
                  db: Session = Depends(get_db)):
    require_origin(request)
    limit(f"account-token:{request.client.host}", 10, 300)
    row = db.get(AccountToken, sha256(payload.token.encode()).hexdigest())
    now = utcnow()
    if row is None or row.confirmed_at is not None or row.expires_at.replace(tzinfo=timezone.utc) <= now:
        raise HTTPException(400, INVALID)
    user = db.scalar(select(User).where(User.id == row.user_id).with_for_update().execution_options(populate_existing=True))
    if user is None or user.email != row.issued_email:
        raise HTTPException(400, INVALID)
    if row.kind == "reset_password":
        if payload.new_password is None or verify_password(payload.new_password, user.password_hash):
            raise HTTPException(422, "Introduce una nueva contrasena diferente de la anterior.")
    elif payload.new_password is not None:
        raise HTTPException(422, "Este enlace no admite una contrasena.")
    claimed = db.execute(update(AccountToken).where(AccountToken.token_hash == row.token_hash,
                         AccountToken.confirmed_at.is_(None), AccountToken.expires_at > now)
                         .values(confirmed_at=now).execution_options(synchronize_session="fetch")).rowcount
    if claimed != 1:
        raise HTTPException(400, INVALID)
    if row.kind in {"email_approve", "email_change"}:
        pair = db.scalars(select(AccountToken).where(AccountToken.change_id == row.change_id,
                           AccountToken.user_id == user.id)).all()
        if len(pair) != 2 or any(item.expires_at.replace(tzinfo=timezone.utc) <= now for item in pair):
            db.rollback()
            raise HTTPException(400, INVALID)
        if any(item.confirmed_at is None for item in pair):
            db.commit()
            return {"kind": "email_change_pending", "message": "Confirmacion guardada. Falta confirmar el otro correo."}
        user.email = row.target_email
        user.email_verified_at = now
        audit(db, user.id, "email.changed")
        result_kind = "email_changed"
    elif row.kind == "verify_email":
        user.email_verified_at = now
        db.execute(delete(AccountToken).where(AccountToken.user_id == user.id, AccountToken.kind == "verify_email"))
        audit(db, user.id, "email.verified")
        db.commit()
        return {"kind": "email_verified", "message": "Correo verificado correctamente."}
    elif row.kind == "reset_password":
        user.password_hash = password_hasher.hash(payload.new_password)
        user.email_verified_at = now
        audit(db, user.id, "password.recovered")
        result_kind = "password_reset"
    else:
        db.rollback()
        raise HTTPException(400, INVALID)
    try:
        with db.no_autoflush:
            db.execute(delete(LoginSession).where(LoginSession.user_id == user.id))
            db.execute(delete(AccountToken).where(AccountToken.user_id == user.id))
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "No se pudo completar el cambio con esos datos.") from None
    response.delete_cookie(COOKIE, path="/")
    if result_kind == "password_reset":
        tasks.add_task(deliver_password_notice, user.email)
    return {"kind": result_kind, "message": "Cambio completado. Inicia sesion con tus nuevos datos."}
