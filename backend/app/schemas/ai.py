from pydantic import BaseModel

from app.schemas.assessment import AssessmentResponse
from app.schemas.policy import PolicyPackResponse


class AiExecutiveSummaryRequest(BaseModel):
    assessment: AssessmentResponse
    policy_pack: PolicyPackResponse


class AiExecutiveSummaryResponse(BaseModel):
    summary: str
    generated_by_ai: bool
    provider: str
    model: str | None = None
