from datetime import timedelta, timezone
from hashlib import sha256
import secrets
from threading import Lock
from time import monotonic

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from fastapi import Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db import LoginSession, User, audit, get_db, utcnow
from app.services.usage_service import reserve_ai_request

password_hasher = PasswordHasher()
dummy_hash = password_hasher.hash(secrets.token_urlsafe(32))
COOKIE = "hotelsec_session"
_lock = Lock()
_buckets: dict[str, list[float]] = {}


def limit(key: str, count: int, seconds: int = 60):
    now = monotonic()
    with _lock:
        # Purge expired buckets as well as the current one to bound memory growth.
        for expired in [k for k, v in _buckets.items() if not v or v[-1] < now - 3600]:
            del _buckets[expired]
        recent = [t for t in _buckets.get(key, []) if t > now - seconds]
        if len(recent) >= count:
            raise HTTPException(429, "Demasiadas peticiones. Intentalo mas tarde.", headers={"Retry-After": str(seconds)})
        recent.append(now)
        _buckets[key] = recent


def verify_password(password: str, hashed: str) -> bool:
    try:
        return password_hasher.verify(hashed, password)
    except VerificationError:
        return False


def require_origin(request: Request):
    origin = request.headers.get("origin")
    if origin and origin not in get_settings().cors_origins:
        raise HTTPException(403, "Origen no permitido.")
    if request.headers.get("sec-fetch-site") == "cross-site":
        raise HTTPException(403, "Peticion entre sitios no permitida.")


def device_label(request: Request | None) -> str:
    agent = request.headers.get("user-agent", "").lower() if request else ""
    browser = next((label for marker, label in (("edg/", "Edge"), ("firefox/", "Firefox"),
                   ("chrome/", "Chrome"), ("safari/", "Safari")) if marker in agent), "Navegador")
    platform = next((label for marker, label in (("android", "Android"), ("iphone", "iOS"),
                    ("ipad", "iPadOS"), ("windows", "Windows"), ("macintosh", "macOS"),
                    ("linux", "Linux")) if marker in agent), "")
    return f"{browser} / {platform}" if platform else browser


def start_session(db: Session, user: User, response: Response, request: Request | None = None):
    token = secrets.token_urlsafe(48)
    csrf = secrets.token_hex(32)
    minutes = get_settings().access_token_expire_minutes
    db.add(LoginSession(token_hash=sha256(token.encode()).hexdigest(), user_id=user.id,
                        csrf_token=csrf, expires_at=utcnow() + timedelta(minutes=minutes),
                        device_label=device_label(request)))
    audit(db, user.id, "session.created")
    db.commit()
    response.set_cookie(COOKIE, token, max_age=minutes * 60, httponly=True,
                        secure=get_settings().cookie_secure, samesite="lax", path="/")
    return {"user": public_user(user), "csrf_token": csrf}


def public_user(user: User):
    return {"id": user.id, "name": user.name, "email": user.email, "role": user.role,
            "organization_name": user.organization_name, "job_title": user.job_title,
            "email_verified": user.email_verified_at is not None, "created_at": user.created_at}


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get(COOKIE, "")
    stored = db.get(LoginSession, sha256(token.encode()).hexdigest()) if token else None
    if not stored or stored.expires_at.replace(tzinfo=timezone.utc) <= utcnow():
        raise HTTPException(401, "Inicia sesion para continuar.")
    user = db.get(User, stored.user_id)
    if not user:
        raise HTTPException(401, "Sesion no valida.")
    request.state.login_session = stored
    if request.method not in {"GET", "HEAD", "OPTIONS"}:
        require_origin(request)
        if not secrets.compare_digest(request.headers.get("x-csrf-token", ""), stored.csrf_token):
            raise HTTPException(403, "Token de seguridad no valido. Recarga la pagina.")
    return user


def require_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403, "Se requiere rol de administrador.")
    return user


def ai_quota(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if get_settings().openai_api_key:
        reserve_ai_request(db, user)
    else:
        limit(f"ai:{user.id}", get_settings().ai_requests_per_hour, 3600)
    return user
