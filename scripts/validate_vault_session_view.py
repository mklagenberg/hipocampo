"""Validate the bounded, ephemeral vault session-view contract."""
from pathlib import Path
import sys
import yaml

REQUIRED = {"address", "entity", "role", "scope", "methodology_version", "compatibility_state", "access_observed", "verified_at", "source"}

def main() -> int:
    root = Path(__file__).resolve().parents[1]
    doc = (root / "docs" / "vault-session-view.md").read_text(encoding="utf-8")
    fixtures = yaml.safe_load((root / "docs" / "vault-session-fixtures.yaml").read_text(encoding="utf-8"))
    for term in ("transient", "discarded", "not a Git file", "ambiguous", "source of truth"):
        assert term in doc, term
    assert {x["id"] for x in fixtures["fixtures"]} == {"same-entity-specialized", "ambiguous-entity", "incompatible-vault", "context-isolation"}
    assert all(x["expected"] in {"allow_read", "blocked", "isolated"} for x in fixtures["fixtures"])
    print("validate_vault_session_view: OK — transient isolation and blocking fixtures")
    return 0

if __name__ == "__main__":
    sys.exit(main())
