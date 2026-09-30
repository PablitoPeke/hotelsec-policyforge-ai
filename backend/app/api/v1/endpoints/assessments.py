from fastapi import APIRouter, Depends
from app.core.security import get_current_user

from app.schemas.assessment import AssessmentRequest, AssessmentResponse
from app.services.assessment_service import analyze_assessment


router = APIRouter(prefix="/assessments", dependencies=[Depends(get_current_user)])


@router.post("/analyze", response_model=AssessmentResponse)
def analyze_hotel_assessment(payload: AssessmentRequest) -> AssessmentResponse:
    return analyze_assessment(payload)
