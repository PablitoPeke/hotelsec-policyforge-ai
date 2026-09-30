from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import COOKIE, dummy_hash, get_current_user, limit, password_hasher, public_user, require_admin, require_origin, start_session, verify_password
from app.db import AuditEvent, LoginSession, User, audit, get_db

router = APIRouter(prefix="/auth")


class Credentials(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)


class Registration(Credentials):
    name: str = Field(min_length=2, max_length=120)


class DeleteAccount(BaseModel):
    password: str = Field(min_length=1, max_length=128)


@router.post("/register", status_code=201)
def register(payload: Registration, request: Request, response: Response, db: Session = Depends(get_db)):
    require_origin(request)
    limit(f"auth:{request.client.host}", 10, 300)
    user = User(name=payload.name, email=str(payload.email).lower(), password_hash=password_hasher.hash(payload.password), role="hotel")
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "No se pudo crear la cuenta con esos datos.") from None
    return start_session(db, user, response)


@router.post("/login")
def login(payload: Credentials, request: Request, response: Response, db: Session = Depends(get_db)):
    require_origin(request)
    limit(f"auth:{request.client.host}", 10, 300)
    user = db.scalar(select(User).where(User.email == str(payload.email).lower()))
    valid = verify_password(payload.password, user.password_hash if user else dummy_hash)
    if not user or not valid:
        audit(db, None, "login.failed")
        db.commit()
        raise HTTPException(401, "Correo o contrasena incorrectos.")
    if password_hasher.check_needs_rehash(user.password_hash):
        user.password_hash = password_hasher.hash(payload.password)
    return start_session(db, user, response)


@router.get("/me")
def me(request: Request, user: User = Depends(get_current_user)):
    return {"user": public_user(user), "csrf_token": request.state.login_session.csrf_token}


@router.post("/logout", status_code=204)
def logout(request: Request, response: Response, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.delete(request.state.login_session)
    audit(db, user.id, "session.revoked")
    db.commit()
    response.delete_cookie(COOKIE, path="/")


@router.delete("/account", status_code=204)
def delete_account(payload: DeleteAccount, response: Response, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(401, "Contrasena incorrecta.")
    db.delete(user)
    db.commit()
    response.delete_cookie(COOKIE, path="/")


@router.get("/audit")
def audit_log(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.scalars(select(AuditEvent).where(AuditEvent.user_id == user.id).order_by(AuditEvent.created_at.desc()).limit(100)).all()
    return [{"event": row.event, "resource_id": row.resource_id, "created_at": row.created_at} for row in rows]


@router.get("/admin/users")
def users(_=Depends(require_admin), db: Session = Depends(get_db)):
    return [public_user(user) for user in db.scalars(select(User).limit(100))]
