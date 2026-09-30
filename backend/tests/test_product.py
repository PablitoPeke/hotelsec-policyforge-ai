from io import BytesIO
import httpx
from fastapi.testclient import TestClient
from pypdf import PdfReader
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.main import app
from app.db import SavedAssessment
from app.schemas.assessment import AssessmentRequest
from app.schemas.ai import AiDescriptionAnalysisRequest, AiExecutiveSummaryRequest
from app.services.ai_service import parse_description, generate_ai_executive_summary
from app.services.product_service import build_bundle


def payload():
    from app.schemas.assessment import SecurityControls
    return {"hotel_profile": {"business_name": "Hotel Prueba Lanzarote", "municipality": "Tias", "business_type": "hotel", "rooms_count": 20,
        "permanent_employees": 5, "temporary_employees": 2, "has_external_it_provider": True, "uses_pms": True,
        "offers_guest_wifi": True, "handles_card_payments": True, "stores_guest_documents": True},
        "security_controls": {k: ("none" if k == "backup_frequency" else False) for k in SecurityControls.model_fields}}


def test_full_flow_persistence_pdf_progress_and_delete(logged_client, isolated_database):
    response = logged_client.post("/api/v1/records", json={"assessment": payload()})
    assert response.status_code == 201, response.text
    record = response.json()
    record_id = record["id"]
    assert len(record["policy_pack"]["policies"]) == 10
    assert record["actions"] and record["regulatory"]
    with Session(isolated_database) as another_session:
        assert another_session.get(SavedAssessment, record_id).bundle["input"] == record["input"]
    history = logged_client.get("/api/v1/records").json()
    assert history["total"] == 1
    updated = logged_client.patch(f"/api/v1/records/{record_id}/actions/0", json={"status": "done"})
    assert updated.json()["actions"][0]["status"] == "done"
    pdf = logged_client.get(f"/api/v1/records/{record_id}/report.pdf")
    assert pdf.status_code == 200 and pdf.headers["content-type"] == "application/pdf"
    reader = PdfReader(BytesIO(pdf.content))
    text = "\n".join(page.extract_text() for page in reader.pages)
    assert "Hotel Prueba Lanzarote" in text
    assert "Plan de accion" in text and "teletrabajo" in text and "AEPD" in text
    for risk in record["assessment"]["risks"]:
        assert risk["title"] in text
    normalized_text = ' '.join(text.split())
    for policy in record['policy_pack']['policies']:
        assert policy['name'] in text
        for control in policy['controls']:
            assert ' '.join(control['description'].split()) in normalized_text
    assert logged_client.delete(f"/api/v1/records/{record_id}").status_code == 204
    assert logged_client.get(f"/api/v1/records/{record_id}").status_code == 404


def test_pdf_keeps_company_names_even_when_they_match_enums(logged_client):
    data = payload()
    data['hotel_profile']['business_name'] = 'low'
    record = logged_client.post('/api/v1/records', json={'assessment': data}).json()
    pdf = logged_client.get(f"/api/v1/records/{record['id']}/report.pdf")
    text = ' '.join(' '.join(page.extract_text() for page in PdfReader(BytesIO(pdf.content)).pages).split())
    assert 'Nombre del alojamiento low' in text


def test_isolation_of_all_record_routes(logged_client):
    record_id = logged_client.post("/api/v1/records", json={"assessment": payload()}).json()["id"]
    other = TestClient(app)
    created = other.post("/api/v1/auth/register", json={"name": "Otro Hotel", "email": "other@example.org", "password": "Other-password-123"})
    other.headers["X-CSRF-Token"] = created.json()["csrf_token"]
    assert other.get("/api/v1/records").json()["total"] == 0
    for suffix in ("", "/report.pdf"):
        assert other.get(f"/api/v1/records/{record_id}{suffix}").status_code == 404
    assert other.delete(f"/api/v1/records/{record_id}").status_code == 404
    assert other.patch(f"/api/v1/records/{record_id}/actions/0", json={"status": "done"}).status_code == 404
    assert logged_client.get(f"/api/v1/records/{record_id}").status_code == 200


def test_description_conflicts_require_confirmation(logged_client):
    base = payload()
    base["security_controls"]["uses_mfa"] = True
    base["security_controls"]["backup_frequency"] = "daily"
    request = {"assessment": base, "description": "No usamos MFA y no hacemos copias."}
    response = logged_client.post("/api/v1/records", json=request)
    assert response.status_code == 409
    assert logged_client.get("/api/v1/records").json()["total"] == 0
    assert len(response.json()["detail"]["conflicts"]) == 2
    response = logged_client.post("/api/v1/records", json={**request, "conflict_resolution": "text"})
    assert response.status_code == 201
    assert response.json()["input"]["security_controls"]["uses_mfa"] is False
    assert response.json()["input"]["security_controls"]["backup_frequency"] == "none"


def test_input_errors_and_progress_validation(logged_client):
    data = payload()
    data["hotel_profile"]["rooms_count"] = -1
    assert logged_client.post("/api/v1/records", json={"assessment": data}).status_code == 422
    assert logged_client.post("/api/v1/records", content="x" * 100001).status_code == 413
    assert logged_client.post("/api/v1/records", json={"assessment": payload(), "description": "x" * 6001}).status_code == 422
    record_id = logged_client.post("/api/v1/records", json={"assessment": payload()}).json()["id"]
    assert logged_client.patch(f"/api/v1/records/{record_id}/actions/0", json={"status": "invented"}).status_code == 422
    assert logged_client.patch(f"/api/v1/records/{record_id}/actions/999", json={"status": "done"}).status_code == 404


def test_provider_timeout_and_malformed_response_fall_back(logged_client, monkeypatch):
    from app.core.config import get_settings
    monkeypatch.setattr(get_settings(), "openai_api_key", "fake-key-for-unit-test")
    def broken(*args, **kwargs):
        raise httpx.ReadTimeout("offline")
    monkeypatch.setattr(httpx, "post", broken)
    response = logged_client.post("/api/v1/records", json={"assessment": payload(), "use_ai": True})
    assert response.status_code == 201
    assert response.json()["ai_summary"]["provider"] == "rules-fallback"
    assert response.json()["policy_pack"]["provider"] == "rules-fallback"
    monkeypatch.setattr(httpx, "post", lambda *a, **k: httpx.Response(200, json={"output_text": "not JSON"}, request=httpx.Request("POST", "https://api.openai.com")))
    response = logged_client.post("/api/v1/records", json={"assessment": payload(), "description": "Usamos PMS y no usamos MFA.", "use_ai": True})
    assert response.status_code == 201
    assert response.json()["description_by_ai"] is False


def test_company_history_and_account_erasure(logged_client, isolated_database):
    first = logged_client.post("/api/v1/records", json={"assessment": payload()}).json()
    second = logged_client.post("/api/v1/records", json={"assessment": payload()}).json()
    assert first["company_id"] == second["company_id"]
    history = logged_client.get("/api/v1/records", params={"company_id": first["company_id"], "limit": 1}).json()
    assert history["total"] == 2 and len(history["items"]) == 1
    assert logged_client.request("DELETE", "/api/v1/auth/account", json={"password": "Demo-password-123"}).status_code == 204
    with Session(isolated_database) as db:
        assert db.scalar(select(SavedAssessment)) is None
