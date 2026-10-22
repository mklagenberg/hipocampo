from pathlib import Path
import sys
import yaml

def main() -> int:
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "bootstrap-invitation-procedure.md").read_text(encoding="utf-8")
    data = yaml.safe_load((root / "docs" / "bootstrap-invitation-fixtures.yaml").read_text(encoding="utf-8"))
    normalized = " ".join(text.lower().split())
    for term in ("preflight", "personal anchor is optional", "explicit", "manifest", "does not copy", "No write", "bounded", "entity read"):
        assert term.lower() in normalized, term
    assert len(data["fixtures"]) == 7
    assert {case["id"]: case["action"] for case in data["fixtures"]}["invited-entity-read-without-personal-anchor"] == "bounded-read-after-target-and-permission-proof"
    print("validate_bootstrap_invitation: OK — preflight, confirmation and blocking gates")
    return 0

if __name__ == "__main__":
    sys.exit(main())
