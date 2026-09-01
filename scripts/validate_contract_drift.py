"""Validate deterministic contract-drift routing."""
from pathlib import Path
import sys
import yaml

def main() -> int:
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "contract-drift-procedure.md").read_text(encoding="utf-8")
    data = yaml.safe_load((root / "docs" / "contract-drift-fixtures.yaml").read_text(encoding="utf-8"))
    for term in ("content change", "instruction change", "contract change", "methodology-version change", "unavailable", "blocked"):
        assert term in text, term
    expected = {"content-change", "instruction-change", "contract-change", "methodology-version-change", "unavailable"}
    assert {x["id"] for x in data["fixtures"]} == expected
    print("validate_contract_drift: OK — five drift classifications")
    return 0

if __name__ == "__main__":
    sys.exit(main())
