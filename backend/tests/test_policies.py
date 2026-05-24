from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_policy_generator_returns_policy_pack_for_hotel_profile():
    payload = {
        "assessment": {
            "hotel_profile": {
                "business_name": "Hotel Demo Lanzarote",
                "municipality": "Tías",
                "business_type": "hotel",
                "rooms_count": 42,
                "permanent_employees": 12,
                "temporary_employees": 8,
                "has_external_it_provider": True,
                "uses_pms": True,
                "offers_guest_wifi": True,
                "handles_card_payments": True,
                "stores_guest_documents": True,
            },
            "security_controls": {
                "uses_mfa": False,
                "uses_password_manager": False,
                "shared_accounts": True,
                "pms_individual_users": False,
                "employee_offboarding_process": False,
                "backup_frequency": "none",
                "backups_tested": False,
                "has_antivirus": True,
                "systems_updated": False,
                "guest_wifi_separated": False,
                "payment_terminal_isolated": False,
                "cctv_or_iot_devices": True,
                "iot_network_separated": False,
                "supplier_remote_access": True,
                "supplier_access_controlled": False,
                "has_incident_response_plan": False,
                "has_rgpd_breach_protocol": False,
                "rgpd_processing_register": False,
                "staff_phishing_training": False,
            },
        }
    }

    response = client.post("/api/v1/policies/generate", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["business_name"] == "Hotel Demo Lanzarote"
    assert body["risk_level"] == "critical"
    assert len(body["policies"]) == 6
    assert body["implementation_order"][0].startswith("Activar MFA")
    assert any(policy["name"] == "Política de copias de seguridad" for policy in body["policies"])
