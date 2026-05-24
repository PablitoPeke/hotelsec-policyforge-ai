from pydantic import BaseModel
from typing import Literal

from app.schemas.assessment import AssessmentRequest, AssessmentResponse
from app.schemas.policy import PolicyPackResponse


class AiExecutiveSummaryRequest(BaseModel):
    assessment: AssessmentResponse
    policy_pack: PolicyPackResponse


class AiExecutiveSummaryResponse(BaseModel):
    summary: str
    generated_by_ai: bool
    provider: str
    model: str | None = None


class AiDescriptionAnalysisRequest(BaseModel):
    business_name: str
    municipality: str
    business_type: Literal[
        "hotel",
        "apartahotel",
        "villa",
        "hostal",
        "alquiler_vacacional",
        "agencia_turistica",
    ]
    rooms_count: int
    permanent_employees: int
    temporary_employees: int
    description: str
    base_assessment: AssessmentRequest | None = None


class AiDescriptionAnalysisResponse(BaseModel):
    normalized_assessment: AssessmentRequest
    assessment: AssessmentResponse
    policy_pack: PolicyPackResponse
    ai_summary: AiExecutiveSummaryResponse
    generated_by_ai: bool
