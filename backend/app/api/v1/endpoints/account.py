"""Self-service account operations; identity always comes from the current session."""
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.core.security import COOKIE, get_current_user, limit, password_hasher, public_user, start_session, verify_password
from app.db import AccountToken, AuditEvent, Company, LoginSession, SavedAssessment, User, audit, get_db, utcnow
from app.services.account_email import deliver_password_notice

router = APIRouter(prefix="/auth")


class ProfileUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str | None = Field(default=None, min_length=2, max_length=120)
    organization_name: str | None = Field(default=None, max_length=120)
    job_title: str | None = Field(default=None, max_length=120)

    @field_validator("name", "organization_name", "job_title", mode="before")
    @classmethod
    def clean_text(cls, value):
        if not isinstance(value, str):
            raise ValueError("Introduce texto valido.")
        return value.strip()

    @model_validator(mode="after")
    def require_changes(self):
        if not self.model_fields_set:
            raise ValueError("Indica al menos un campo.")
        return self


class CurrentPassword(BaseModel):
    model_config = ConfigDict(extra="forbid")
    current_password: str = Field(min_length=1, max_length=128)


class PasswordChange(CurrentPassword):
    new_password: str = Field(min_length=12, max_length=128)


def reauthenticate(payload: CurrentPassword, user: User, db: Session):
    limit(f"sensitive:{user.id}", 10, 900)
    db.refresh(user, with_for_update=True)
    if not verify_password(payload.current_password, user.password_hash):
        raise HTTPException(403, "La contrasena actual no es correcta.")


@router.patch("/profile")
def update_profile(payload: ProfileUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    limit(f"profile:{user.id}", 20)
    for name, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, name, value)
    audit(db, user.id, "profile.updated")
    db.commit()
    return public_user(user)


@router.post("/password")
def change_password(payload: PasswordChange, request: Request, response: Response, tasks: BackgroundTasks,
                    user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    reauthenticate(payload, user, db)
    if verify_password(payload.new_password, user.password_hash):
        raise HTTPException(422, "La nueva contrasena debe ser diferente de la actual.")
    user.password_hash = password_hasher.hash(payload.new_password)
    db.execute(delete(LoginSession).where(LoginSession.user_id == user.id))
    db.execute(delete(AccountToken).where(AccountToken.user_id == user.id))
    audit(db, user.id, "password.changed")
    # The new password, revocations and replacement session commit together.
    result = start_session(db, user, response, request)
    tasks.add_task(deliver_password_notice, user.email)
    return result


@router.get("/sessions")
def active_sessions(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.scalars(select(LoginSession).where(LoginSession.user_id == user.id,
                      LoginSession.expires_at > utcnow()).order_by(LoginSession.expires_at.desc())).all()
    return [{"id": row.public_id, "device": row.device_label, "created_at": row.created_at,
             "expires_at": row.expires_at, "current": row.public_id == request.state.login_session.public_id}
            for row in rows]


@router.post("/sessions/revoke-others", status_code=204)
def revoke_others(payload: CurrentPassword, request: Request, user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    reauthenticate(payload, user, db)
    db.execute(delete(LoginSession).where(LoginSession.user_id == user.id,
               LoginSession.public_id != request.state.login_session.public_id))
    audit(db, user.id, "sessions.others_revoked")
    db.commit()


@router.delete("/sessions/{session_id}", status_code=204)
def revoke_session(session_id: str, request: Request, response: Response,
                   user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.scalar(select(LoginSession).where(LoginSession.public_id == session_id, LoginSession.user_id == user.id))
    if row is None:
        raise HTTPException(404, "Sesion no encontrada.")
    current = row.public_id == request.state.login_session.public_id
    db.delete(row)
    audit(db, user.id, "session.revoked")
    db.commit()
    if current:
        response.delete_cookie(COOKIE, path="/")


@router.post("/export")
def export_data(payload: CurrentPassword, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    reauthenticate(payload, user, db)
    limit(f"export:{user.id}", 3, 3600)
    count = db.scalar(select(func.count()).select_from(SavedAssessment).where(SavedAssessment.owner_id == user.id))
    if count > 1000:
        raise HTTPException(413, "La exportacion automatica admite hasta 1000 analisis.")
    companies = db.scalars(select(Company).where(Company.owner_id == user.id)).all()
    records = db.scalars(select(SavedAssessment).where(SavedAssessment.owner_id == user.id)
                         .order_by(SavedAssessment.created_at, SavedAssessment.id)).all()
    events = db.scalars(select(AuditEvent).where(AuditEvent.user_id == user.id)
                        .order_by(AuditEvent.created_at).limit(10000)).all()
    data = {"format_version": 1, "exported_at": utcnow(), "profile": public_user(user),
            "companies": [{"id": row.id, "name": row.name, "municipality": row.municipality,
                           "created_at": row.created_at} for row in companies],
            "assessments": [{"id": row.id, "company_id": row.company_id, "created_at": row.created_at,
                            "snapshot": row.bundle, "action_statuses": row.action_statuses} for row in records],
            "activity": [{"event": row.event, "created_at": row.created_at, "resource_id": row.resource_id}
                         for row in events], "activity_limit": 10000}
    audit(db, user.id, "account.exported")
    db.commit()
    return JSONResponse(jsonable_encoder(data), headers={
        "Content-Disposition": 'attachment; filename="hotelsec-mis-datos.json"', "Cache-Control": "no-store"})
