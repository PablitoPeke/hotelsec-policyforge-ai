from pydantic import BaseModel, Field
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
    business_name: str = Field(min_length=2, max_length=120)
    municipality: str = Field(min_length=2, max_length=80)
    business_type: Literal[
        "hotel",
        "apartahotel",
        "villa",
        "hostal",
        "alquiler_vacacional",
        "agencia_turistica",
    ]
    rooms_count: int = Field(ge=1, le=1000)
    permanent_employees: int = Field(ge=0, le=500)
    temporary_employees: int = Field(ge=0, le=500)
    description: str = Field(min_length=10, max_length=6000)
    base_assessment: AssessmentRequest | None = None
    conflict_resolution: Literal["manual", "text"] = "manual"


class AiDescriptionAnalysisResponse(BaseModel):
    normalized_assessment: AssessmentRequest
    assessment: AssessmentResponse
    policy_pack: PolicyPackResponse
    ai_summary: AiExecutiveSummaryResponse
    generated_by_ai: bool
    conflicts: list[dict] = Field(default_factory=list)
