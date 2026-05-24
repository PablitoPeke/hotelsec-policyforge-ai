from pydantic import BaseModel, Field

from app.schemas.assessment import AssessmentRequest, RiskLevel


class PolicyGenerateRequest(BaseModel):
    assessment: AssessmentRequest


class PolicyControl(BaseModel):
    title: str
    description: str
    priority: RiskLevel


class GeneratedPolicy(BaseModel):
    name: str
    objective: str
    scope: str
    controls: list[PolicyControl] = Field(min_length=1)
    evidence: list[str]
    review_frequency: str


class PolicyPackResponse(BaseModel):
    business_name: str
    municipality: str
    overall_score: int = Field(ge=0, le=100)
    risk_level: RiskLevel
    policies: list[GeneratedPolicy]
    implementation_order: list[str]
