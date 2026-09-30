from app.schemas.assessment import AssessmentRequest
from app.schemas.ai import AiDescriptionAnalysisRequest, AiExecutiveSummaryRequest
from app.services.assessment_service import analyze_assessment
from app.services.policy_service import generate_policy_pack
from app.services.ai_service import PROMPT_VERSION, enrich_policies, generate_ai_executive_summary, parse_description

SOURCES = [
    {"name": "AEPD - Facilita RGPD", "url": "https://www.aepd.es/guias-y-herramientas/herramientas/facilita-rgpd", "topic": "Documentar tratamientos, encargados y medidas. Facilita se orienta a tratamientos de bajo riesgo; valorar cada caso."},
    {"name": "INCIBE - Politicas para pymes", "url": "https://www.incibe.es/empresas/herramientas/politicas", "topic": "Establecer responsables, procedimientos, formacion y evidencias de seguridad."},
    {"name": "ISO - Familia ISO/IEC 27000", "url": "https://www.iso.org/standard/iso-iec-27000-family", "topic": "Gestionar riesgos, controles y mejora continua. Esta herramienta no realiza una certificacion ISO."},
]


def build_bundle(payload: AssessmentRequest, description: str = "", use_ai: bool = False, resolution: str = "manual"):
    normalized, conflicts, parsed_by_ai = payload, [], False
    if description:
        profile = payload.hotel_profile
        normalized, conflicts, parsed_by_ai = parse_description(AiDescriptionAnalysisRequest(
            **{k: getattr(profile, k) for k in ("business_name", "municipality", "business_type", "rooms_count", "permanent_employees", "temporary_employees")},
            description=description, base_assessment=payload, conflict_resolution=resolution), use_ai=use_ai)
    result = analyze_assessment(normalized)
    policies = generate_policy_pack(normalized)
    if use_ai:
        policies = enrich_policies(normalized, policies)
    summary_payload = AiExecutiveSummaryRequest(assessment=result, policy_pack=policies)
    if use_ai:
        summary = generate_ai_executive_summary(summary_payload)
    else:
        from app.schemas.ai import AiExecutiveSummaryResponse
        summary = AiExecutiveSummaryResponse(summary=f"{result.business_name}: madurez {result.overall_score}/100. "
            f"Se detectan {len(result.risks)} riesgos. Priorizar: " + " ".join(result.next_steps), generated_by_ai=False, provider="rules")
    actions = []
    for index, risk in enumerate(result.risks):
        actions.append({"id": str(index), "title": risk.recommendation, "risk": risk.title,
            "priority": risk.severity, "deadline_days": 0 if risk.severity == "critical" else 30 if risk.severity == "high" else 90,
            "difficulty": "media" if risk.severity in {"critical", "high"} else "baja",
            "impact": risk.impact, "responsible": "Direccion y proveedor IT", "status": "pending"})
    return {"input": normalized.model_dump(), "description": description, "assessment": result.model_dump(),
        "policy_pack": policies.model_dump(), "ai_summary": summary.model_dump(), "actions": actions,
        "regulatory": SOURCES, "conflicts": conflicts, "description_by_ai": parsed_by_ai,
        "prompt_version": PROMPT_VERSION, "scoring_version": "rules-v2", "disclaimer":
        "Autodiagnostico basado en declaraciones. Probabilidad e impacto son estimaciones orientativas. "
        "Politicas propuestas para revision humana; no certifica ISO ni cumplimiento RGPD. "
        "No introduzca documentos, nombres de huespedes ni datos de pago."}
