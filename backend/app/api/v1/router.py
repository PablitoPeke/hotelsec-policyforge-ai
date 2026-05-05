from fastapi import APIRouter

from app.api.v1.endpoints import assessments, health


api_router = APIRouter()
api_router.include_router(assessments.router, tags=["assessments"])
api_router.include_router(health.router, tags=["health"])
