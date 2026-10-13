"""Optional TLS-only SMTP delivery; never expose links or credentials through logs."""
from datetime import timedelta
from email.message import EmailMessage
from hashlib import sha256
import logging
import secrets
import smtplib
import ssl
from urllib.parse import urlencode

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db import AccountToken, User, utcnow


def add_token(db: Session, user: User, kind: str, target_email: str | None = None, change_id: str | None = None):
    raw = secrets.token_urlsafe(32)
    db.add(AccountToken(token_hash=sha256(raw.encode()).hexdigest(), user_id=user.id, kind=kind,
                        issued_email=user.email, target_email=target_email or user.email, change_id=change_id,
                        expires_at=utcnow() + timedelta(minutes=15 if kind == "reset_password" else 30)))
    return raw


def send_message(recipient: str, subject: str, content: str):
    settings = get_settings()
    if not settings.email_delivery_configured:
        raise RuntimeError("Email delivery is not configured.")
    message = EmailMessage()
    message["From"] = str(settings.smtp_from)
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(content)
    context = ssl.create_default_context()
    connection = (smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port, timeout=10, context=context)
                  if settings.smtp_mode == "ssl" else smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=10))
    with connection as client:
        if settings.smtp_mode == "starttls":
            client.ehlo()
            client.starttls(context=context)
            client.ehlo()
        if settings.smtp_username:
            client.login(settings.smtp_username, settings.smtp_password.get_secret_value())
        client.send_message(message)


def deliver_link(recipient: str, kind: str, raw_token: str):
    subjects = {"verify_email": "Verifica tu correo", "reset_password": "Restablece tu contrasena",
                "email_approve": "Autoriza el cambio de correo", "email_change": "Confirma tu nuevo correo"}
    # Fragments do not reach access logs; APP_URL is operator configuration, never a request Host header.
    link = get_settings().frontend_url.rstrip("/") + "/#" + urlencode({"account_token": raw_token, "purpose": kind})
    text = (f"HotelSec PolicyForge AI\n\n{subjects[kind]}\n\n{link}\n\n"
            "El enlace caduca y solo puede utilizarse una vez. Un cambio de correo requiere confirmar ambos buzones.\n"
            "Si no has solicitado esta accion, no confirmes el enlace. No compartas este mensaje.\n")
    try:
        send_message(recipient, "HotelSec - " + subjects[kind], text)
    except Exception as error:
        logging.getLogger("hotelsec").warning("account_email_delivery_failed kind=%s exception=%s", kind, type(error).__name__)


def deliver_password_notice(recipient: str):
    if not get_settings().email_delivery_configured:
        return
    try:
        send_message(recipient, "HotelSec - Contrasena actualizada",
                     "La contrasena de tu cuenta HotelSec se ha actualizado. Las sesiones anteriores se han cerrado.\n"
                     "Si no lo has solicitado, utiliza la recuperacion de contrasena y revisa el acceso a tu correo.\n")
    except Exception as error:
        logging.getLogger("hotelsec").warning("account_notice_delivery_failed exception=%s", type(error).__name__)
