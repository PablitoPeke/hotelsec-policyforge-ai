from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_assessment_returns_score_and_risks_for_weak_security_profile():
    payload = {
        "hotel_profile": {
            "business_name": "Hotel Demo Lanzarote",
            "municipality": "Tías",
            "business_type": "hotel",
            "rooms_count": 42,
            "permanent_employees": 12,
            "temporary_employees": 8,
            "has_external_it_provider": True,
        },
        "security_controls": {
            "uses_mfa": False,
            "uses_password_manager": False,
            "shared_accounts": True,
            "backup_frequency": "none",
            "backups_tested": False,
            "has_antivirus": True,
            "systems_updated": False,
            "guest_wifi_separated": False,
            "has_incident_response_plan": False,
            "has_rgpd_breach_protocol": False,
            "staff_phishing_training": False,
        },
    }

    response = client.post("/api/v1/assessments/analyze", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["business_name"] == "Hotel Demo Lanzarote"
    assert body["risk_level"] == "critical"
    assert body["overall_score"] < 50
    assert len(body["risks"]) >= 4


def test_assessment_returns_low_risk_for_strong_security_profile():
    payload = {
        "hotel_profile": {
            "business_name": "Villa Segura",
            "municipality": "Yaiza",
            "business_type": "villa",
            "rooms_count": 8,
            "permanent_employees": 4,
            "temporary_employees": 1,
            "has_external_it_provider": True,
        },
        "security_controls": {
            "uses_mfa": True,
            "uses_password_manager": True,
            "shared_accounts": False,
            "backup_frequency": "daily",
            "backups_tested": True,
            "has_antivirus": True,
            "systems_updated": True,
            "guest_wifi_separated": True,
            "has_incident_response_plan": True,
            "has_rgpd_breach_protocol": True,
            "staff_phishing_training": True,
        },
    }

    response = client.post("/api/v1/assessments/analyze", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["risk_level"] == "low"
    assert body["overall_score"] == 100
    assert body["risks"] == []
