from pathlib import Path
import sys
import yaml

def main() -> int:
    root = Path(__file__).resolve().parents[1]
    text = (root / "docs" / "skill-recovery-runbook.md").read_text(encoding="utf-8")
    data = yaml.safe_load((root / "docs" / "skill-recovery-fixtures.yaml").read_text(encoding="utf-8"))
    for term in ("manifest", "lock", "rollback", "known-good", "unverified", "credentials"):
        assert term in text, term
    assert len(data["fixtures"]) == 4
    print("validate_skill_recovery: OK — bounded recovery and rollback fixtures")
    return 0

if __name__ == "__main__":
    sys.exit(main())
