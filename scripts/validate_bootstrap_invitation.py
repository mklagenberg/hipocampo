from pathlib import Path
import sys
import yaml

def main() -> int:
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "bootstrap-invitation-procedure.md").read_text(encoding="utf-8")
    data = yaml.safe_load((root / "docs" / "bootstrap-invitation-fixtures.yaml").read_text(encoding="utf-8"))
    for term in ("preflight", "personal anchor", "explicit confirmation", "manifest", "does not copy", "No write"):
        assert term in text, term
    assert len(data["fixtures"]) == 6
    print("validate_bootstrap_invitation: OK — preflight, confirmation and blocking gates")
    return 0

if __name__ == "__main__":
    sys.exit(main())
