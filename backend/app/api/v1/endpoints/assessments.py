from fastapi import APIRouter

from app.schemas.assessment import AssessmentRequest, AssessmentResponse
from app.services.assessment_service import analyze_assessment


router = APIRouter(prefix="/assessments")


@router.post("/analyze", response_model=AssessmentResponse)
def analyze_hotel_assessment(payload: AssessmentRequest) -> AssessmentResponse:
    return analyze_assessment(payload)
