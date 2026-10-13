"""Persisted request ceilings, not a token/dollar budget or billing system."""
from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert as postgres_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db import AiUsage, User, utcnow


def reserve_ai_request(db: Session, user: User):
    settings = get_settings()
    if settings.ai_global_daily_limit == 0:
        raise HTTPException(503, "La IA esta desactivada temporalmente. Puedes analizar sin IA.")
    now = utcnow()
    hour_end = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    day_end = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    buckets = [
        ("global:" + now.strftime("%Y%m%d"), None, settings.ai_global_daily_limit, day_end,
         "Limite diario de IA alcanzado. Puedes analizar sin IA."),
        (f"user:{user.id}:" + now.strftime("%Y%m%d%H"), user.id, settings.ai_requests_per_hour, hour_end,
         "Has alcanzado tu limite horario de IA. Puedes analizar sin IA."),
    ]
    dialect = db.get_bind().dialect.name
    insert = postgres_insert if dialect == "postgresql" else sqlite_insert if dialect == "sqlite" else None
    if insert is None:
        raise HTTPException(503, "No se pudo comprobar la cuota de IA.")
    # Always lock the global row first. Both ceilings commit or roll back together.
    for key, owner, ceiling, boundary, message in buckets:
        db.execute(insert(AiUsage).values(bucket=key, owner_id=owner, used=0,
                   expires_at=boundary + timedelta(days=1)).on_conflict_do_nothing(index_elements=["bucket"]))
        updated = db.execute(update(AiUsage).where(AiUsage.bucket == key, AiUsage.used < ceiling)
                             .values(used=AiUsage.used + 1).execution_options(synchronize_session=False))
        if updated.rowcount != 1:
            db.rollback()
            raise HTTPException(429, message, headers={"Retry-After": str(max(1, int((boundary - now).total_seconds())))})
    db.commit()
