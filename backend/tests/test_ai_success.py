import json
import httpx
import pytest
from tests.test_product import payload
from app.core.config import get_settings


def test_valid_provider_responses_integrate_context_policies_and_summary(logged_client, monkeypatch):
    monkeypatch.setattr(get_settings(), 'openai_api_key', 'fake-for-tests-only')
    calls = []
    def respond(url, **kwargs):
        assert url == 'https://api.openai.com/v1/responses'
        assert kwargs['timeout'] == 30
        packet = kwargs['json']
        data = json.loads(packet['input'])
        calls.append(packet['instructions'])
        if 'Extrae SOLO' in packet['instructions']:
            text = json.dumps({'hotel_profile': {}, 'security_controls': {'uses_mfa': True}})
        elif 'Adapta estas' in packet['instructions']:
            text = json.dumps({'policies': [{'objective': 'Propuesta adaptada al PMS cloud.', 'scope': item['scope'], 'controls': item['controls']} for item in data['pack']['policies']]})
        else:
            text = 'Resumen de prueba basado en declaraciones. Priorizar copias y separar redes.'
        return httpx.Response(200, json={'output': [{'content': [{'type': 'output_text', 'text': text}]}]}, request=httpx.Request('POST', url))
    monkeypatch.setattr(httpx, 'post', respond)
    response = logged_client.post('/api/v1/records', json={'assessment': payload(), 'description': 'Utilizamos autenticacion reforzada.', 'use_ai': True})
    assert response.status_code == 201, response.text
    record = response.json()
    assert record['description_by_ai'] is True
    assert record['input']['security_controls']['uses_mfa'] is True
    assert record['policy_pack']['provider'] == 'openai'
    assert record['ai_summary']['generated_by_ai'] is True
    assert all(p['objective'] == 'Propuesta adaptada al PMS cloud.' for p in record['policy_pack']['policies'])
    assert len(calls) == 3


@pytest.mark.parametrize('provider_output', [[], {'output': ['invalid']}, {'output': None}])
def test_malformed_provider_structure_falls_back(logged_client, monkeypatch, provider_output):
    monkeypatch.setattr(get_settings(), 'openai_api_key', 'fake-for-tests-only')
    monkeypatch.setattr(httpx, 'post', lambda url, **kwargs: httpx.Response(200, json=provider_output, request=httpx.Request('POST', url)))
    result = logged_client.post('/api/v1/records', json={'assessment': payload(), 'use_ai': True})
    assert result.status_code == 201
    assert result.json()['ai_summary']['provider'] == 'rules-fallback'
    assert result.json()['policy_pack']['provider'] == 'rules-fallback'
