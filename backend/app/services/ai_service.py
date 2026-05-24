import json

import httpx

from app.core.config import get_settings
from app.schemas.ai import (
    AiDescriptionAnalysisRequest,
    AiDescriptionAnalysisResponse,
    AiExecutiveSummaryRequest,
    AiExecutiveSummaryResponse,
)
from app.schemas.assessment import AssessmentRequest, HotelProfile, SecurityControls
from app.services.assessment_service import analyze_assessment
from app.services.policy_service import generate_policy_pack


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


def analyze_description_with_ai(
    payload: AiDescriptionAnalysisRequest,
) -> AiDescriptionAnalysisResponse:
    settings = get_settings()
    generated_by_ai = False

    if settings.openai_api_key:
        try:
            normalized = _call_openai_description_parser(
                payload,
                settings.openai_api_key,
                settings.openai_model,
            )
            generated_by_ai = True
        except (httpx.HTTPError, ValueError, KeyError, TypeError):
            normalized = _build_assessment_from_description_rules(payload)
    else:
        normalized = _build_assessment_from_description_rules(payload)

    assessment = analyze_assessment(normalized)
    policy_pack = generate_policy_pack(normalized)
    ai_summary = generate_ai_executive_summary(
        AiExecutiveSummaryRequest(assessment=assessment, policy_pack=policy_pack)
    )

    return AiDescriptionAnalysisResponse(
        normalized_assessment=normalized,
        assessment=assessment,
        policy_pack=policy_pack,
        ai_summary=ai_summary,
        generated_by_ai=generated_by_ai,
    )


def _call_openai_responses_api(
    payload: AiExecutiveSummaryRequest,
    api_key: str,
    model: str,
) -> str:
    request_body = {
        "model": model,
        "instructions": (
            "Eres un consultor senior de ciberseguridad para hoteles en Espana. "
            "Escribe un resumen ejecutivo claro, profesional y breve para direccion. "
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


def _call_openai_description_parser(
    payload: AiDescriptionAnalysisRequest,
    api_key: str,
    model: str,
) -> AssessmentRequest:
    request_body = {
        "model": model,
        "instructions": (
            "Convierte una descripcion libre de un alojamiento turistico en un JSON "
            "de controles de ciberseguridad. Responde solo con JSON valido, sin markdown. "
            "Si un dato no aparece claro, usa un valor conservador para una pyme hotelera."
        ),
        "input": json.dumps(
            {
                "business_name": payload.business_name,
                "municipality": payload.municipality,
                "business_type": payload.business_type,
                "rooms_count": payload.rooms_count,
                "permanent_employees": payload.permanent_employees,
                "temporary_employees": payload.temporary_employees,
                "description": payload.description,
                "base_assessment": (
                    payload.base_assessment.model_dump()
                    if payload.base_assessment
                    else None
                ),
                "required_schema": {
                    "hotel_profile": {
                        "has_external_it_provider": "boolean",
                        "uses_pms": "boolean",
                        "offers_guest_wifi": "boolean",
                        "handles_card_payments": "boolean",
                        "stores_guest_documents": "boolean",
                    },
                    "security_controls": {
                        "uses_mfa": "boolean",
                        "uses_password_manager": "boolean",
                        "shared_accounts": "boolean",
                        "pms_individual_users": "boolean",
                        "employee_offboarding_process": "boolean",
                        "backup_frequency": "none|monthly|weekly|daily",
                        "backups_tested": "boolean",
                        "has_antivirus": "boolean",
                        "systems_updated": "boolean",
                        "guest_wifi_separated": "boolean",
                        "payment_terminal_isolated": "boolean",
                        "cctv_or_iot_devices": "boolean",
                        "iot_network_separated": "boolean",
                        "supplier_remote_access": "boolean",
                        "supplier_access_controlled": "boolean",
                        "has_incident_response_plan": "boolean",
                        "has_rgpd_breach_protocol": "boolean",
                        "rgpd_processing_register": "boolean",
                        "staff_phishing_training": "boolean",
                    },
                },
            },
            ensure_ascii=False,
        ),
        "max_output_tokens": 900,
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
    parsed = _parse_json_object(_extract_response_text(response.json()))
    profile_data = parsed["hotel_profile"]
    controls_data = parsed["security_controls"]

    base = payload.base_assessment
    return AssessmentRequest(
        hotel_profile=HotelProfile(
            business_name=payload.business_name,
            municipality=payload.municipality,
            business_type=payload.business_type,
            rooms_count=payload.rooms_count,
            permanent_employees=payload.permanent_employees,
            temporary_employees=payload.temporary_employees,
            has_external_it_provider=_merge_bool(
                base.hotel_profile.has_external_it_provider if base else False,
                profile_data.get("has_external_it_provider"),
            ),
            uses_pms=_merge_bool(base.hotel_profile.uses_pms if base else False, profile_data.get("uses_pms")),
            offers_guest_wifi=_merge_bool(
                base.hotel_profile.offers_guest_wifi if base else False,
                profile_data.get("offers_guest_wifi"),
            ),
            handles_card_payments=_merge_bool(
                base.hotel_profile.handles_card_payments if base else False,
                profile_data.get("handles_card_payments"),
            ),
            stores_guest_documents=_merge_bool(
                base.hotel_profile.stores_guest_documents if base else False,
                profile_data.get("stores_guest_documents"),
            ),
        ),
        security_controls=SecurityControls(
            uses_mfa=_merge_bool(base.security_controls.uses_mfa if base else False, controls_data.get("uses_mfa")),
            uses_password_manager=_merge_bool(
                base.security_controls.uses_password_manager if base else False,
                controls_data.get("uses_password_manager"),
            ),
            shared_accounts=_merge_bool(
                base.security_controls.shared_accounts if base else False,
                controls_data.get("shared_accounts"),
            ),
            pms_individual_users=_merge_bool(
                base.security_controls.pms_individual_users if base else False,
                controls_data.get("pms_individual_users"),
            ),
            employee_offboarding_process=_merge_bool(
                base.security_controls.employee_offboarding_process if base else False,
                controls_data.get("employee_offboarding_process")
            ),
            backup_frequency=_backup_frequency(
                str(
                    controls_data.get(
                        "backup_frequency",
                        base.security_controls.backup_frequency if base else "none",
                    )
                )
            ),
            backups_tested=_merge_bool(
                base.security_controls.backups_tested if base else False,
                controls_data.get("backups_tested"),
            ),
            has_antivirus=_merge_bool(
                base.security_controls.has_antivirus if base else False,
                controls_data.get("has_antivirus"),
            ),
            systems_updated=_merge_bool(
                base.security_controls.systems_updated if base else False,
                controls_data.get("systems_updated"),
            ),
            guest_wifi_separated=_merge_bool(
                base.security_controls.guest_wifi_separated if base else False,
                controls_data.get("guest_wifi_separated"),
            ),
            payment_terminal_isolated=_merge_bool(
                base.security_controls.payment_terminal_isolated if base else False,
                controls_data.get("payment_terminal_isolated"),
            ),
            cctv_or_iot_devices=_merge_bool(
                base.security_controls.cctv_or_iot_devices if base else False,
                controls_data.get("cctv_or_iot_devices"),
            ),
            iot_network_separated=_merge_bool(
                base.security_controls.iot_network_separated if base else False,
                controls_data.get("iot_network_separated"),
            ),
            supplier_remote_access=_merge_bool(
                base.security_controls.supplier_remote_access if base else False,
                controls_data.get("supplier_remote_access"),
            ),
            supplier_access_controlled=_merge_bool(
                base.security_controls.supplier_access_controlled if base else False,
                controls_data.get("supplier_access_controlled"),
            ),
            has_incident_response_plan=_merge_bool(
                base.security_controls.has_incident_response_plan if base else False,
                controls_data.get("has_incident_response_plan"),
            ),
            has_rgpd_breach_protocol=_merge_bool(
                base.security_controls.has_rgpd_breach_protocol if base else False,
                controls_data.get("has_rgpd_breach_protocol"),
            ),
            rgpd_processing_register=_merge_bool(
                base.security_controls.rgpd_processing_register if base else False,
                controls_data.get("rgpd_processing_register"),
            ),
            staff_phishing_training=_merge_bool(
                base.security_controls.staff_phishing_training if base else False,
                controls_data.get("staff_phishing_training"),
            ),
        ),
    )


def _extract_response_text(data: dict) -> str:
    output_text = data.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    for item in data.get("output", []):
        for content in item.get("content", []):
            text = content.get("text")
            if isinstance(text, str) and text.strip():
                return text.strip()

    return "La IA no devolvio texto interpretable. Se recomienda revisar el analisis generado por reglas."


def _parse_json_object(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.removeprefix("json").strip()
    return json.loads(cleaned)


def _build_assessment_from_description_rules(
    payload: AiDescriptionAnalysisRequest,
) -> AssessmentRequest:
    text = payload.description.lower()
    has_wifi = _contains_any(text, ["wifi", "wi-fi", "inalambrica"])
    has_pms = _contains_any(text, ["pms", "channel", "reservas", "booking"])
    has_card_payments = _contains_any(text, ["tpv", "tarjeta", "datafono", "pago"])
    has_iot = _contains_any(text, ["camara", "cctv", "iot", "domotica", "cerradura"])
    shared_accounts = _contains_any(
        text,
        ["cuenta compartida", "cuentas compartidas", "usuario generico", "misma cuenta"],
    )

    base = payload.base_assessment
    inferred = AssessmentRequest(
        hotel_profile=HotelProfile(
            business_name=payload.business_name,
            municipality=payload.municipality,
            business_type=payload.business_type,
            rooms_count=payload.rooms_count,
            permanent_employees=payload.permanent_employees,
            temporary_employees=payload.temporary_employees,
            has_external_it_provider=_contains_any(
                text, ["proveedor", "externo", "informatica"]
            ),
            uses_pms=has_pms,
            offers_guest_wifi=has_wifi,
            handles_card_payments=has_card_payments,
            stores_guest_documents=_contains_any(
                text, ["dni", "documento", "pasaporte", "parte de viajeros"]
            ),
        ),
        security_controls=SecurityControls(
            uses_mfa=_contains_any(text, ["mfa", "2fa", "doble factor", "segundo factor"]),
            uses_password_manager=_contains_any(
                text, ["gestor de contrasenas", "1password", "bitwarden"]
            ),
            shared_accounts=shared_accounts,
            pms_individual_users=has_pms
            and not shared_accounts
            and _contains_any(text, ["usuario individual", "usuarios individuales", "cada empleado"]),
            employee_offboarding_process=_contains_any(
                text, ["baja de empleado", "retirada de accesos", "offboarding"]
            ),
            backup_frequency=_infer_backup_frequency(text),
            backups_tested=_contains_any(
                text, ["restauracion", "probamos copias", "prueba de backup"]
            ),
            has_antivirus=_contains_any(text, ["antivirus", "edr", "defender"]),
            systems_updated=_contains_any(text, ["actualizado", "actualizaciones", "parches"]),
            guest_wifi_separated=has_wifi
            and _contains_any(text, ["wifi separado", "red separada", "vlan", "red de invitados"]),
            payment_terminal_isolated=has_card_payments
            and _contains_any(text, ["tpv aislado", "red de pagos", "segmento de pagos"]),
            cctv_or_iot_devices=has_iot,
            iot_network_separated=has_iot
            and _contains_any(text, ["iot separado", "cctv separado", "red de camaras"]),
            supplier_remote_access=_contains_any(
                text, ["acceso remoto", "teamviewer", "anydesk", "proveedor entra"]
            ),
            supplier_access_controlled=_contains_any(
                text, ["mfa proveedor", "vpn", "registro de accesos", "horario"]
            ),
            has_incident_response_plan=_contains_any(
                text, ["plan de respuesta", "procedimiento de incidente"]
            ),
            has_rgpd_breach_protocol=_contains_any(
                text, ["brecha rgpd", "notificacion rgpd"]
            ),
            rgpd_processing_register=_contains_any(
                text, ["registro de tratamientos", "rgpd documentado"]
            ),
            staff_phishing_training=_contains_any(
                text, ["phishing", "formacion", "concienciacion"]
            ),
        ),
    )

    return _merge_assessments(base, inferred) if base else inferred


def _build_fallback_summary(payload: AiExecutiveSummaryRequest) -> str:
    assessment = payload.assessment
    policy_pack = payload.policy_pack
    first_steps = " ".join(policy_pack.implementation_order[:3])

    return (
        f"{assessment.business_name} presenta una puntuacion de madurez de "
        f"{assessment.overall_score}/100 y un nivel de riesgo {assessment.risk_level}. "
        f"El analisis detecta {len(assessment.risks)} riesgos activos y propone "
        f"{len(policy_pack.policies)} politicas iniciales. Las acciones prioritarias son: "
        f"{first_steps} Este resumen se ha generado con reglas porque no hay una clave "
        "OPENAI_API_KEY configurada."
    )


def _contains_any(text: str, patterns: list[str]) -> bool:
    normalized = _normalize(text)
    return any(_normalize(pattern) in normalized for pattern in patterns)


def _normalize(value: str) -> str:
    return (
        value.replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ñ", "n")
    )


def _infer_backup_frequency(text: str) -> str:
    if _contains_any(text, ["diaria", "diario", "cada dia"]):
        return "daily"
    if _contains_any(text, ["semanal", "cada semana"]):
        return "weekly"
    if _contains_any(text, ["mensual", "cada mes"]):
        return "monthly"
    if _contains_any(text, ["no hacemos copias", "sin copias", "no hay backup", "no hay copias"]):
        return "none"
    return "monthly"


def _backup_frequency(value: str) -> str:
    if value in {"none", "monthly", "weekly", "daily"}:
        return value
    return "none"


def _as_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in {"true", "yes", "si", "sí", "1"}
    return bool(value)


def _merge_bool(base_value: bool, inferred_value: object) -> bool:
    return base_value or _as_bool(inferred_value)


def _merge_assessments(
    base: AssessmentRequest | None,
    inferred: AssessmentRequest,
) -> AssessmentRequest:
    if not base:
        return inferred

    return AssessmentRequest(
        hotel_profile=HotelProfile(
            business_name=inferred.hotel_profile.business_name,
            municipality=inferred.hotel_profile.municipality,
            business_type=inferred.hotel_profile.business_type,
            rooms_count=inferred.hotel_profile.rooms_count,
            permanent_employees=inferred.hotel_profile.permanent_employees,
            temporary_employees=inferred.hotel_profile.temporary_employees,
            has_external_it_provider=base.hotel_profile.has_external_it_provider
            or inferred.hotel_profile.has_external_it_provider,
            uses_pms=base.hotel_profile.uses_pms or inferred.hotel_profile.uses_pms,
            offers_guest_wifi=base.hotel_profile.offers_guest_wifi
            or inferred.hotel_profile.offers_guest_wifi,
            handles_card_payments=base.hotel_profile.handles_card_payments
            or inferred.hotel_profile.handles_card_payments,
            stores_guest_documents=base.hotel_profile.stores_guest_documents
            or inferred.hotel_profile.stores_guest_documents,
        ),
        security_controls=SecurityControls(
            uses_mfa=base.security_controls.uses_mfa or inferred.security_controls.uses_mfa,
            uses_password_manager=base.security_controls.uses_password_manager
            or inferred.security_controls.uses_password_manager,
            shared_accounts=base.security_controls.shared_accounts
            or inferred.security_controls.shared_accounts,
            pms_individual_users=base.security_controls.pms_individual_users
            or inferred.security_controls.pms_individual_users,
            employee_offboarding_process=base.security_controls.employee_offboarding_process
            or inferred.security_controls.employee_offboarding_process,
            backup_frequency=_strongest_backup_frequency(
                base.security_controls.backup_frequency,
                inferred.security_controls.backup_frequency,
            ),
            backups_tested=base.security_controls.backups_tested
            or inferred.security_controls.backups_tested,
            has_antivirus=base.security_controls.has_antivirus
            or inferred.security_controls.has_antivirus,
            systems_updated=base.security_controls.systems_updated
            or inferred.security_controls.systems_updated,
            guest_wifi_separated=base.security_controls.guest_wifi_separated
            or inferred.security_controls.guest_wifi_separated,
            payment_terminal_isolated=base.security_controls.payment_terminal_isolated
            or inferred.security_controls.payment_terminal_isolated,
            cctv_or_iot_devices=base.security_controls.cctv_or_iot_devices
            or inferred.security_controls.cctv_or_iot_devices,
            iot_network_separated=base.security_controls.iot_network_separated
            or inferred.security_controls.iot_network_separated,
            supplier_remote_access=base.security_controls.supplier_remote_access
            or inferred.security_controls.supplier_remote_access,
            supplier_access_controlled=base.security_controls.supplier_access_controlled
            or inferred.security_controls.supplier_access_controlled,
            has_incident_response_plan=base.security_controls.has_incident_response_plan
            or inferred.security_controls.has_incident_response_plan,
            has_rgpd_breach_protocol=base.security_controls.has_rgpd_breach_protocol
            or inferred.security_controls.has_rgpd_breach_protocol,
            rgpd_processing_register=base.security_controls.rgpd_processing_register
            or inferred.security_controls.rgpd_processing_register,
            staff_phishing_training=base.security_controls.staff_phishing_training
            or inferred.security_controls.staff_phishing_training,
        ),
    )


def _strongest_backup_frequency(base_frequency: str, inferred_frequency: str) -> str:
    order = {"none": 0, "monthly": 1, "weekly": 2, "daily": 3}
    return base_frequency if order[base_frequency] >= order[inferred_frequency] else inferred_frequency
