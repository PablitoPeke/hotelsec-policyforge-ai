"""Collect structured test evidence without publishing traces, cookies or local paths."""
import json
from pathlib import Path
from datetime import datetime, timezone
from xml.etree import ElementTree

root = Path(__file__).resolve().parents[1]
evidence = root / 'docs/practica3/evidence'


def optional_report(name):
    path = evidence / name
    return json.loads(path.read_text(encoding='utf-8')) if path.is_file() else {}


remote_check = optional_report('deployment-remote-check.json')
remote_transport = optional_report('transport-remote-check.json')
live_ai_check = optional_report('live-ai-check.json')
xml_path = evidence / 'backend-tests.xml'
tree = ElementTree.parse(xml_path)
suites = list(tree.getroot().iter('testsuite'))
for suite in suites:
    suite.attrib.pop('hostname', None)
tree.write(xml_path, encoding='utf-8', xml_declaration=True)
browser_path = root / 'frontend/test-results/results.json'
if browser_path.is_file():
    browser_stats = json.loads(browser_path.read_text(encoding='utf-8-sig'))['stats']
else:
    browser_stats = optional_report('browser-local-check.json').get('stats')
    if not browser_stats:
        raise SystemExit('Local browser results missing; run local tests or restore their sanitized evidence.')
backend = {key: sum(int(s.attrib.get(key, 0)) for s in suites) for key in ('tests', 'failures', 'errors', 'skipped')}
backend['seconds'] = round(sum(float(s.attrib.get('time', 0)) for s in suites), 2)
js_audit = json.loads((root / 'docs/practica3/dependency-audit-npm.json').read_text(encoding='utf-8-sig'))
python_audit = json.loads((root / 'docs/practica3/dependency-audit-python.json').read_text(encoding='utf-8-sig'))
result = {'collected_at': datetime.now(timezone.utc).isoformat(), 'backend': backend,
          'browser': browser_stats, 'npm_vulnerabilities': js_audit['metadata']['vulnerabilities'],
          'local_browser_source': 'frontend/test-results/results.json' if browser_path.is_file() else 'docs/practica3/evidence/browser-local-check.json (historical metadata)',
          'python_known_vulnerabilities': sum(len(d['vulns']) for d in python_audit['dependencies']),
          'environment': 'Local Windows; Docker Linux; PostgreSQL 17; Node 24; Chromium',
          'external_deployment_verified': remote_check.get('passed') is True and remote_transport.get('passed') is True,
          'live_openai_verified': live_ai_check.get('passed') is True and live_ai_check.get('ai_requested') is True,
          'database_restart': {'before': 4, 'after': 4, 'note': 'Manual psql check on 30/09/2026; separate from the restore test'},
          'restore_test': json.loads((evidence / 'restore-check.json').read_text(encoding='utf-8')),
          'remote_ci': json.loads((evidence / 'ci-status.json').read_text(encoding='utf-8')),
          'local_deployment_check': json.loads((evidence / 'deployment-local-check.json').read_text(encoding='utf-8')),
          'student_manual_review': json.loads((evidence / 'manual-review.json').read_text(encoding='utf-8')),
          'remote_access_check': json.loads((evidence / 'remote-access-check.json').read_text(encoding='utf-8')),
          'legacy_remote_backup': json.loads((evidence / 'legacy-backup-check.json').read_text(encoding='utf-8')),
          'remote_deployment_check': remote_check,
          'remote_transport_check': remote_transport,
          'remote_browser_check': optional_report('browser-remote-check.json'),
          'live_ai_check': live_ai_check,
          'remote_runtime_check': optional_report('runtime-remote-check.json')}
(evidence / 'verification.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps(result, indent=2, ensure_ascii=False))
