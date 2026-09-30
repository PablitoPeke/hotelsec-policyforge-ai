from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.core.security import ai_quota, get_current_user
from app.db import Company, SavedAssessment, User, audit, get_db
from app.schemas.assessment import AssessmentRequest
from app.services.product_service import build_bundle
from app.services.report_service import render_report

router = APIRouter(prefix="/records")


class CreateRecord(BaseModel):
    assessment: AssessmentRequest
    description: str = Field(default="", max_length=6000)
    use_ai: bool = False
    conflict_resolution: Literal["manual", "text"] | None = None
    company_id: str | None = None


class ActionUpdate(BaseModel):
    status: Literal["pending", "in_progress", "done"]


def owned_record(db: Session, user: User, identifier: str):
    record = db.scalar(select(SavedAssessment).where(SavedAssessment.id == identifier, SavedAssessment.owner_id == user.id))
    if record is None:
        audit(db, user.id, "record.access_denied", identifier[:36])
        db.commit()
        raise HTTPException(404, "Analisis no encontrado.")
    return record


def detail(record: SavedAssessment):
    bundle = {**record.bundle, "actions": [{**action, "status": record.action_statuses.get(action["id"], "pending")} for action in record.bundle["actions"]]}
    return {"id": record.id, "company_id": record.company_id, "created_at": record.created_at, **bundle}


@router.post("", status_code=201)
def create(payload: CreateRecord, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if payload.use_ai or payload.description:
        ai_quota(user)
    company = None
    if payload.company_id:
        company = db.scalar(select(Company).where(Company.id == payload.company_id, Company.owner_id == user.id))
        if company is None:
            raise HTTPException(404, "Alojamiento no encontrado.")
    bundle = build_bundle(payload.assessment, payload.description, payload.use_ai, payload.conflict_resolution or "manual")
    if bundle["conflicts"] and payload.conflict_resolution is None:
        raise HTTPException(409, detail={"message": "El texto contradice controles marcados. Confirma que fuente conservar.", "conflicts": bundle["conflicts"]})
    profile = payload.assessment.hotel_profile
    if company is None:
        company = db.scalar(select(Company).where(Company.owner_id == user.id, Company.name == profile.business_name, Company.municipality == profile.municipality))
    if company is None:
        company = Company(owner_id=user.id, name=profile.business_name, municipality=profile.municipality)
        db.add(company)
        db.flush()
    record = SavedAssessment(owner_id=user.id, company_id=company.id, bundle=bundle, action_statuses={})
    db.add(record)
    db.flush()
    audit(db, user.id, "record.created", record.id)
    db.commit()
    return detail(record)


@router.get("")
def history(company_id: str | None = None, offset: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = select(SavedAssessment).where(SavedAssessment.owner_id == user.id)
    if company_id:
        query = query.where(SavedAssessment.company_id == company_id)
    rows = db.scalars(query.order_by(SavedAssessment.created_at.desc(), SavedAssessment.id).offset(offset).limit(limit)).all()
    total = db.scalar(select(func.count()).select_from(query.subquery()))
    return {"total": total, "items": [{"id": row.id, "company_id": row.company_id, "created_at": row.created_at,
        "business_name": row.bundle["assessment"]["business_name"], "overall_score": row.bundle["assessment"]["overall_score"],
        "risk_level": row.bundle["assessment"]["risk_level"], "risk_count": len(row.bundle["assessment"]["risks"]),
        "pending_actions": sum(row.action_statuses.get(a["id"]) != "done" for a in row.bundle["actions"])} for row in rows]}


@router.get("/{record_id}")
def read(record_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return detail(owned_record(db, user, record_id))


@router.patch("/{record_id}/actions/{action_id}")
def update_action(record_id: str, action_id: str, payload: ActionUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = owned_record(db, user, record_id)
    if action_id not in {a["id"] for a in record.bundle["actions"]}:
        raise HTTPException(404, "Accion no encontrada.")
    record.action_statuses = {**record.action_statuses, action_id: payload.status}
    audit(db, user.id, "action.updated", record.id)
    db.commit()
    return detail(record)


@router.delete("/{record_id}", status_code=204)
def remove(record_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = owned_record(db, user, record_id)
    audit(db, user.id, "record.deleted", record.id)
    db.delete(record)
    db.commit()


@router.get("/{record_id}/report.pdf")
def report(record_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = owned_record(db, user, record_id)
    result = render_report(detail(record), record.created_at.isoformat(), record.id)
    audit(db, user.id, "report.downloaded", record.id)
    db.commit()
    return Response(result, media_type="application/pdf", headers={"Content-Disposition": f'attachment; filename="hotelsec-{record.id}.pdf"'})
