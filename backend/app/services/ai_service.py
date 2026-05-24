import json

import httpx

from app.core.config import get_settings
from app.schemas.ai import AiExecutiveSummaryRequest, AiExecutiveSummaryResponse


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


def generate_ai_executive_summary(
    payload: AiExecutiveSummaryRequest,
) -> AiExecutiveSummaryResponse:
    settings = get_settings()

    if not settings.openai_api_key:
        return AiExecutiveSummaryResponse(
            summary=_build_fallback_summary(payload),
            generated_by_ai=False,
            provider="rules",
            model=None,
        )

    try:
        summary = _call_openai_responses_api(payload, settings.openai_api_key, settings.openai_model)
    except httpx.HTTPError:
        return AiExecutiveSummaryResponse(
            summary=_build_fallback_summary(payload),
            generated_by_ai=False,
            provider="rules-fallback",
            model=None,
        )

    return AiExecutiveSummaryResponse(
        summary=summary,
        generated_by_ai=True,
        provider="openai",
        model=settings.openai_model,
    )


def _call_openai_responses_api(
    payload: AiExecutiveSummaryRequest,
    api_key: str,
    model: str,
) -> str:
    request_body = {
        "model": model,
        "instructions": (
            "Eres un consultor senior de ciberseguridad para hoteles en España. "
            "Escribe un resumen ejecutivo claro, profesional y breve para dirección. "
            "No inventes datos fuera del JSON recibido. No uses markdown."
        ),
        "input": json.dumps(
            {
                "assessment": payload.assessment.model_dump(),
                "policy_pack": payload.policy_pack.model_dump(),
            },
            ensure_ascii=False,
        ),
        "max_output_tokens": 500,
    }

    response = httpx.post(
        OPENAI_RESPONSES_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=request_body,
        timeout=30,
    )
    response.raise_for_status()
    return _extract_response_text(response.json())


def _extract_response_text(data: dict) -> str:
    output_text = data.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    for item in data.get("output", []):
        for content in item.get("content", []):
            text = content.get("text")
            if isinstance(text, str) and text.strip():
                return text.strip()

    return "La IA no devolvió texto interpretable. Se recomienda revisar el análisis generado por reglas."


def _build_fallback_summary(payload: AiExecutiveSummaryRequest) -> str:
    assessment = payload.assessment
    policy_pack = payload.policy_pack
    first_steps = " ".join(policy_pack.implementation_order[:3])

    return (
        f"{assessment.business_name} presenta una puntuación de madurez de "
        f"{assessment.overall_score}/100 y un nivel de riesgo {assessment.risk_level}. "
        f"El análisis detecta {len(assessment.risks)} riesgos activos y propone "
        f"{len(policy_pack.policies)} políticas iniciales. Las acciones prioritarias son: "
        f"{first_steps} Este resumen se ha generado con reglas porque no hay una clave "
        "OPENAI_API_KEY configurada."
    )
