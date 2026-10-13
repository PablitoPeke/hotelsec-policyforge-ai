"""Collect only counters and checks for the account-center release, never raw traces."""
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree

root = Path(__file__).resolve().parents[1]
evidence = root / "docs/practica3/evidence"
xml_path = evidence / "backend-tests-account-center.xml"
tree = ElementTree.parse(xml_path)
suites = list(tree.getroot().iter("testsuite"))
for suite in suites:
    suite.attrib.pop("hostname", None)
tree.write(xml_path, encoding="utf-8", xml_declaration=True)
backend = {key: sum(int(s.attrib.get(key, 0)) for s in suites)
           for key in ("tests", "failures", "errors", "skipped")}
backend["seconds"] = round(sum(float(s.attrib.get("time", 0)) for s in suites), 2)
result = {
    "collected_at": datetime.now(timezone.utc).isoformat(),
    "code_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
    "version": "0.4.0", "backend": backend,
    "smtp_delivery_tested": False,
    "new_paid_ai_calls": 0,
    "scope": "Account/profile/session/email preparation and persistent AI quotas; not a pentest or commercial certification.",
}
for environment in ("local", "hetzner"):
    path = root / f"frontend/test-results/account-center-{environment}.json"
    if path.is_file():
        stats = json.loads(path.read_text(encoding="utf-8-sig"))["stats"]
        result[f"browser_{environment}"] = stats
for name in ("account-center-backup", "account-center-deployment", "account-center-runtime"):
    path = evidence / f"{name}.json"
    if path.is_file():
        result[name] = json.loads(path.read_text(encoding="utf-8-sig"))
(evidence / "account-center-verification.json").write_text(
    json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(result, indent=2, ensure_ascii=False))
