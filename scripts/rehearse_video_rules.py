"""Check proposed demo inputs in memory: no HTTP, database writes or paid AI."""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
sys.path.insert(0, str(ROOT))
from app.schemas.assessment import AssessmentRequest
from app.services.product_service import build_bundle
from scripts.verify_deployment import sample_assessment

data = sample_assessment()
data['hotel_profile'].update(business_name='Hotel Demo Lanzarote - Video', rooms_count=40,
    permanent_employees=12, temporary_employees=8, technology_inventory=['PMS en la nube', 'Microsoft 365', 'TPV'],
    personal_data_categories=['Reservas', 'facturacion'], high_season='Todo el ano', retention_days=180, it_response_hours=24)
data['security_controls'].update(uses_mfa=True, uses_password_manager=False, shared_accounts=True,
    pms_individual_users=False, employee_offboarding_process=False, business_continuity_plan=False)
assessment = AssessmentRequest.model_validate(data)
with patch('app.services.ai_service._request', side_effect=AssertionError('Paid AI must not run')) as provider:
    conflict = build_bundle(assessment, 'No usamos MFA y no hacemos copias.', use_ai=False, resolution='manual')
    assert any(c['field'] == 'uses_mfa' and c['manual'] is True and c['text'] is False for c in conflict['conflicts'])
    initial = build_bundle(assessment, 'No usamos MFA y no hacemos copias.', use_ai=False, resolution='text')
    assert initial['input']['security_controls']['uses_mfa'] is False
    assert initial['input']['hotel_profile']['rooms_count'] == 40
    improved_data = deepcopy(initial['input'])
    improved_data['security_controls'].update(uses_mfa=True, uses_password_manager=True, backup_frequency='daily',
        backups_tested=True, systems_updated=True, guest_wifi_separated=True)
    improved = build_bundle(AssessmentRequest.model_validate(improved_data), '', use_ai=False)
    assert improved['assessment']['overall_score'] > initial['assessment']['overall_score']
    consistent_text = 'El correo del hotel usa doble factor. Las copias de seguridad se realizan a diario y se prueba su restauracion.'
    coherent = build_bundle(AssessmentRequest.model_validate(improved_data), consistent_text, use_ai=False)
    assert coherent['conflicts'] == []
    assert coherent['input']['hotel_profile']['rooms_count'] == 40
    assert len(initial['policy_pack']['policies']) == 10
    assert provider.call_count == 0
result = {'checked_at': datetime.now(timezone.utc).isoformat(), 'passed': True,
          'scope': 'Pure in-memory rules rehearsal of recording inputs; not HTTP/browser/video verification.',
          'mfa_contradiction_detected': True, 'text_resolution_preserves_profile': True,
          'initial_score': initial['assessment']['overall_score'], 'improved_score': improved['assessment']['overall_score'],
          'coherent_followup_has_no_conflict': True, 'policies': 10, 'paid_ai_calls': 0,
          'actual_video_recorded': False}
(ROOT / 'docs/practica3/evidence/video-rules-rehearsal.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
