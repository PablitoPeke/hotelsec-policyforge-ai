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
