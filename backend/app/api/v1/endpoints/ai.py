from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import ai_quota, get_current_user
from app.db import User, get_db

from app.schemas.ai import (
    AiDescriptionAnalysisRequest,
    AiDescriptionAnalysisResponse,
    AiExecutiveSummaryRequest,
    AiExecutiveSummaryResponse,
)
from app.services.ai_service import analyze_description_with_ai, generate_ai_executive_summary


router = APIRouter(prefix="/ai")


@router.post("/executive-summary", response_model=AiExecutiveSummaryResponse)
def create_ai_executive_summary(
    payload: AiExecutiveSummaryRequest,
    user: User = Depends(get_current_user), db: Session = Depends(get_db),
) -> AiExecutiveSummaryResponse:
    ai_quota(user, db)
    return generate_ai_executive_summary(payload)


@router.post("/analyze-description", response_model=AiDescriptionAnalysisResponse)
def analyze_free_text_description(
    payload: AiDescriptionAnalysisRequest,
    user: User = Depends(get_current_user), db: Session = Depends(get_db),
) -> AiDescriptionAnalysisResponse:
    ai_quota(user, db)
    return analyze_description_with_ai(payload)
