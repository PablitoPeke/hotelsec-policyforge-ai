from fastapi import APIRouter

from app.api.v1.endpoints import account, ai, assessments, auth, health, policies, records


api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(account.router, tags=["account"])
api_router.include_router(records.router, tags=["records"])
api_router.include_router(ai.router, tags=["ai"])
api_router.include_router(assessments.router, tags=["assessments"])
api_router.include_router(health.router, tags=["health"])
api_router.include_router(policies.router, tags=["policies"])
