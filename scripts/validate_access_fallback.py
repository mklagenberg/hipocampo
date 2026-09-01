from pathlib import Path
import sys
import yaml

def main() -> int:
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "access-pending-fallback.md").read_text(encoding="utf-8")
    data = yaml.safe_load((root / "docs" / "access-fallback-fixtures.yaml").read_text(encoding="utf-8"))
    for term in ("same-entity", "personal anchor", "block", "sensitive", "MRL-0004"):
        assert term in text, term
    assert len(data["fixtures"]) == 7
    assert any(x["action"] == "blocked" for x in data["fixtures"])
    print("validate_access_fallback: OK — diagnosis, provisional guardrails and limits")
    return 0

if __name__ == "__main__":
    sys.exit(main())
