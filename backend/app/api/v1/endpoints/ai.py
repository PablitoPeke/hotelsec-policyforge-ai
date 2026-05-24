from fastapi import APIRouter

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
) -> AiExecutiveSummaryResponse:
    return generate_ai_executive_summary(payload)


@router.post("/analyze-description", response_model=AiDescriptionAnalysisResponse)
def analyze_free_text_description(
    payload: AiDescriptionAnalysisRequest,
) -> AiDescriptionAnalysisResponse:
    return analyze_description_with_ai(payload)
