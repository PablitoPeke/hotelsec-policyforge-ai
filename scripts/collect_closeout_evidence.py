"""Summarize closeout tests without publishing raw traces or secret detector matches."""
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree

root = Path(__file__).resolve().parents[1]
evidence = root / "docs/practica3/evidence"
temporary = root / "tmp/pdfs"


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


tree = ElementTree.parse(evidence / "closeout-backend-tests.xml")
suites = list(tree.getroot().iter("testsuite"))
for suite in suites:
    suite.attrib.pop("hostname", None)
tree.write(evidence / "closeout-backend-tests.xml", encoding="utf-8", xml_declaration=True)
backend = {key: sum(int(s.attrib.get(key, 0)) for s in suites)
           for key in ("tests", "failures", "errors", "skipped")}
backend["seconds"] = round(sum(float(s.attrib.get("time", 0)) for s in suites), 2)
pip = read(temporary / "closeout-pip-audit.json")
npm = read(temporary / "closeout-npm-audit.json")
raw = read(temporary / "gitleaks-closeout.json")
reviewed = read(temporary / "gitleaks-closeout-reviewed.json")
clean = read(evidence / "closeout-clean-deployment.json")
browser = read(root / "frontend/test-results/closeout-clean-install.json")["stats"]
result = {
    "checked_at": datetime.now(timezone.utc).isoformat(),
    "application_commit": "83d7b9b8a20e99bd5636d3bcb404ebc03deadc22",
    "application_version": "0.4.0", "backend": backend,
    "python_known_vulnerabilities": sum(len(d["vulns"]) for d in pip["dependencies"]),
    "npm_vulnerabilities": npm["metadata"]["vulnerabilities"],
    "gitleaks": {"version": "8.30.1", "scope": "all locally available Git refs; redacted scan",
                 "commits": int(subprocess.check_output(["git", "rev-list", "--all", "--count"], cwd=root, text=True)),
                 "raw_findings": len(raw), "reviewed_false_positives": len(raw) - len(reviewed),
                 "actionable_findings": len(reviewed),
                 "review": "Exact historical fingerprints: invalid fictional E2E token and Python csrf_token=csrf keyword expression. No broad rule/path exclusions.",
                 "limits": "Pattern-based review, not proof of absence; excludes unversioned data, external services and binary content."},
    "clean_install": {"source": "fresh GitHub clone, new private config and PostgreSQL volume",
                      "compose_project": "hotelsec-p3-clean-closeout", "port": 8086,
                      "browser": browser, "api": clean,
                      "human_external_tester": False,
                      "limits": "Independent automated environment, not the required external-person installation."},
    "remote_account_release": read(evidence / "account-center-verification.json"),
    "ci": {"run_id": 38465826974, "url": "https://github.com/PablitoPeke/hotelsec-policyforge-ai/actions/runs/38465826974",
           "conclusion": "failure", "job_steps": {"backend": 0, "frontend": 0},
           "reason": "The job was not started because your account is locked due to a billing issue.",
           "ci_tests_passed": False},
    "student_hours": {"total_estimated": 40, "basis": "Student estimate in chat on 2026-10-13; not an audited time log."},
    "new_paid_ai_calls": 0,
    "remaining_manual_items": ["group number", "video and exact timestamps", "external-person installation", "student PDF/repository review", "final commit/tag and campus submission"],
}
detail = root / "frontend/test-results/closeout-account-detail.json"
if detail.is_file():
    result['remote_account_detail_browser'] = read(detail)['stats']
layout = evidence / 'memory-layout.json'
if layout.is_file():
    result['memory_layout'] = read(layout)
qa = evidence / 'memory-margins-closeout.json'
if qa.is_file():
    result['memory_margin_check'] = read(qa)
(evidence / "closeout-verification.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps({k: v for k, v in result.items() if k != "remote_account_release"}, indent=2))
