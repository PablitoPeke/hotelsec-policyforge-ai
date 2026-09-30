from fastapi import APIRouter, Depends
from app.core.security import get_current_user

from app.schemas.policy import PolicyGenerateRequest, PolicyPackResponse
from app.services.policy_service import generate_policy_pack


router = APIRouter(prefix="/policies", dependencies=[Depends(get_current_user)])


@router.post("/generate", response_model=PolicyPackResponse)
def generate_policies(payload: PolicyGenerateRequest) -> PolicyPackResponse:
    return generate_policy_pack(payload.assessment)
