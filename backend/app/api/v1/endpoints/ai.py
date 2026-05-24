from fastapi import APIRouter

from app.schemas.ai import AiExecutiveSummaryRequest, AiExecutiveSummaryResponse
from app.services.ai_service import generate_ai_executive_summary


router = APIRouter(prefix="/ai")


@router.post("/executive-summary", response_model=AiExecutiveSummaryResponse)
def create_ai_executive_summary(
    payload: AiExecutiveSummaryRequest,
) -> AiExecutiveSummaryResponse:
    return generate_ai_executive_summary(payload)
