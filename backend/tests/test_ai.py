from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_ai_summary_endpoint_returns_fallback_without_api_key():
    payload = {
        "assessment": {
            "business_name": "Hotel Demo Lanzarote",
            "overall_score": 32,
            "risk_level": "critical",
            "area_scores": [{"area": "Identidad y accesos", "score": 20}],
            "risks": [
                {
                    "title": "Falta de doble factor",
                    "description": "Cuentas críticas sin MFA.",
                    "severity": "high",
                    "recommendation": "Activar MFA.",
                }
            ],
            "next_steps": ["Activar MFA."],
        },
        "policy_pack": {
            "business_name": "Hotel Demo Lanzarote",
            "municipality": "Tías",
            "overall_score": 32,
            "risk_level": "critical",
            "policies": [
                {
                    "name": "Política de contraseñas y accesos",
                    "objective": "Reducir accesos no autorizados.",
                    "scope": "Personal y proveedores.",
                    "controls": [
                        {
                            "title": "Doble factor",
                            "description": "Activar MFA.",
                            "priority": "high",
                        }
                    ],
                    "evidence": ["Capturas de MFA activado."],
                    "review_frequency": "Trimestral.",
                }
            ],
            "implementation_order": ["Activar MFA.", "Revisar backups."],
        },
    }

    response = client.post("/api/v1/ai/executive-summary", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["generated_by_ai"] is False
    assert body["provider"] in {"rules", "rules-fallback"}
    assert "Hotel Demo Lanzarote" in body["summary"]


def test_ai_description_analysis_returns_assessment_from_free_text():
    payload = {
        "business_name": "Hotel Texto Libre",
        "municipality": "Tías",
        "business_type": "hotel",
        "rooms_count": 30,
        "permanent_employees": 8,
        "temporary_employees": 4,
        "description": (
            "Tenemos PMS de reservas, WiFi para clientes en la misma red que recepcion, "
            "TPV con tarjeta, camaras CCTV, usamos cuentas compartidas y no hacemos copias."
        ),
    }

    response = client.post("/api/v1/ai/analyze-description", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["assessment"]["business_name"] == "Hotel Texto Libre"
    assert body["assessment"]["risk_level"] == "critical"
    assert body["policy_pack"]["policies"]
    assert body["normalized_assessment"]["hotel_profile"]["uses_pms"] is True
    assert body["normalized_assessment"]["security_controls"]["shared_accounts"] is True


def test_ai_description_analysis_merges_manual_assessment_with_free_text():
    payload = {
        "business_name": "Hotel Mixto",
        "municipality": "Yaiza",
        "business_type": "hotel",
        "rooms_count": 20,
        "permanent_employees": 6,
        "temporary_employees": 2,
        "description": "Usamos PMS y proveedores entran por AnyDesk.",
        "base_assessment": {
            "hotel_profile": {
                "business_name": "Hotel Mixto",
                "municipality": "Yaiza",
                "business_type": "hotel",
                "rooms_count": 20,
                "permanent_employees": 6,
                "temporary_employees": 2,
                "has_external_it_provider": True,
                "uses_pms": False,
                "offers_guest_wifi": True,
                "handles_card_payments": True,
                "stores_guest_documents": True,
            },
            "security_controls": {
                "uses_mfa": True,
                "uses_password_manager": True,
                "shared_accounts": False,
                "pms_individual_users": True,
                "employee_offboarding_process": True,
                "backup_frequency": "daily",
                "backups_tested": True,
                "has_antivirus": True,
                "systems_updated": True,
                "guest_wifi_separated": True,
                "payment_terminal_isolated": True,
                "cctv_or_iot_devices": False,
                "iot_network_separated": False,
                "supplier_remote_access": False,
                "supplier_access_controlled": False,
                "has_incident_response_plan": True,
                "has_rgpd_breach_protocol": True,
                "rgpd_processing_register": True,
                "staff_phishing_training": True,
            },
        },
    }

    response = client.post("/api/v1/ai/analyze-description", json=payload)

    assert response.status_code == 200
    body = response.json()
    normalized = body["normalized_assessment"]
    assert normalized["security_controls"]["uses_mfa"] is True
    assert normalized["security_controls"]["backup_frequency"] == "daily"
    assert normalized["hotel_profile"]["uses_pms"] is True
    assert normalized["security_controls"]["supplier_remote_access"] is True
