"""Collect structured test evidence without publishing traces, cookies or local paths."""
import json
from pathlib import Path
from datetime import datetime, timezone
from xml.etree import ElementTree

root = Path(__file__).resolve().parents[1]
evidence = root / 'docs/practica3/evidence'
xml_path = evidence / 'backend-tests.xml'
tree = ElementTree.parse(xml_path)
suites = list(tree.getroot().iter('testsuite'))
for suite in suites:
    suite.attrib.pop('hostname', None)
tree.write(xml_path, encoding='utf-8', xml_declaration=True)
browser = json.loads((root / 'frontend/test-results/results.json').read_text(encoding='utf-8-sig'))
backend = {key: sum(int(s.attrib.get(key, 0)) for s in suites) for key in ('tests', 'failures', 'errors', 'skipped')}
backend['seconds'] = round(sum(float(s.attrib.get('time', 0)) for s in suites), 2)
js_audit = json.loads((root / 'docs/practica3/dependency-audit-npm.json').read_text(encoding='utf-8-sig'))
python_audit = json.loads((root / 'docs/practica3/dependency-audit-python.json').read_text(encoding='utf-8-sig'))
result = {'collected_at': datetime.now(timezone.utc).isoformat(), 'backend': backend,
          'browser': browser['stats'], 'npm_vulnerabilities': js_audit['metadata']['vulnerabilities'],
          'python_known_vulnerabilities': sum(len(d['vulns']) for d in python_audit['dependencies']),
          'environment': 'Local Windows; Docker Linux; PostgreSQL 17; Node 24; Chromium',
          'external_deployment_verified': False, 'live_openai_verified': False,
          'database_restart': {'before': 4, 'after': 4, 'note': 'Manual psql check on 30/09/2026; separate from the restore test'},
          'restore_test': json.loads((evidence / 'restore-check.json').read_text(encoding='utf-8'))}
(evidence / 'verification.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps(result, indent=2, ensure_ascii=False))
