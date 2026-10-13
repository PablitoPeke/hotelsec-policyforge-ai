from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
import logging

from app.api.v1.router import api_router
from app.core.config import get_settings


settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        description="API for HotelSec PolicyForge AI.",
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.exception_handler(RequestValidationError)
    async def invalid_request(request: Request, exception: RequestValidationError):
        errors = [{key: value for key, value in error.items() if key in {"loc", "msg", "type"}}
                  for error in exception.errors()]
        return JSONResponse({"detail": errors}, status_code=422)

    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        length = request.headers.get("content-length", "0")
        if not length.isdigit() or int(length) > 100000:
            return JSONResponse({"detail": "Peticion demasiado grande o invalida."}, status_code=413)
        if len(await request.body()) > 100000:
            return JSONResponse({"detail": "Peticion demasiado grande."}, status_code=413)
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "same-origin"
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.exception_handler(Exception)
    async def unexpected_error(request: Request, exception: Exception):
        logging.getLogger("hotelsec").error("request_failed method=%s exception=%s", request.method, type(exception).__name__)
        return JSONResponse({"detail": "Error interno. Reintenta o contacta con soporte."}, status_code=500)

    @app.get("/")
    def read_root() -> dict[str, str]:
        return {
            "service": settings.app_name,
            "version": settings.app_version,
            "environment": settings.app_env,
            "docs": "/docs",
            "health": f"{settings.api_v1_prefix}/health",
        }

    return app


app = create_app()
