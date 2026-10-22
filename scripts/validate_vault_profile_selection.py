#!/usr/bin/env python3
"""Check the V3 profile selection state table and its scaffold declarations."""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from vault_profile_selection import SUGGESTED_DEFAULT, VAULT_PROFILES, evaluate


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    cases = yaml.safe_load((root / "docs/v3-vault-profile-selection-fixtures.yaml").read_text(encoding="utf-8"))["cases"]
    for case in cases:
        inputs = {key: value for key, value in case.items() if key not in {"id", "expected", "warning", "blocked_operation"}}
        actual = evaluate(**inputs)
        for key, expected in (("status", case["expected"]), ("warning", case.get("warning")), ("blocked_operation", case.get("blocked_operation"))):
            if actual.get(key) != expected:
                errors.append(f"{case['id']}: {key}: {actual.get(key)!r} != {expected!r}")
        if actual["suggested_default"] != "team":
            errors.append(f"{case['id']}: default is not team")
        if case["expected"] != "selection_confirmed" and actual["declaration_complete"]:
            errors.append(f"{case['id']}: unconfirmed declaration treated as complete")
    for name in ("pessoal", "empresa"):
        profile = yaml.safe_load((root / f"scaffold/profiles/{name}.yaml").read_text(encoding="utf-8"))
        inputs = [item for item in profile["inputs"] if item["id"] == "vault_profile"]
        if len(inputs) != 1 or set(inputs[0].get("enum", [])) != VAULT_PROFILES:
            errors.append(f"{name}: one three-value vault_profile input required")
        elif (inputs[0].get("suggested_default") != SUGGESTED_DEFAULT
              or inputs[0].get("requires_explicit_selection") is not True
              or "default" in inputs[0]):
            errors.append(f"{name}: team must be suggestion, never automatic value")
    skeleton = yaml.safe_load((root / "scaffold/skeleton/hipocampo.yaml").read_text(encoding="utf-8"))
    value = skeleton["instance"].get("vault_profile", "")
    if "fill in" not in value or "team | personal | entity" not in value:
        errors.append("skeleton: vault_profile must be an explicit-choice placeholder")
    semantic = (root / "docs/v3-vault-profile-selection.md").read_text(encoding="utf-8")
    for phrase in ("Team (suggested)", "PROFILE_UNDECLARED", "INCOMPLETE_CREATION", "never silently fill `team`", "V2/V2.1", "representative"):
        if phrase.lower() not in semantic.lower():
            errors.append(f"semantic procedure missing {phrase!r}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    errors = validate(Path(args.root))
    if errors:
        print(f"validate_vault_profile_selection: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print(f"validate_vault_profile_selection: OK — {len(yaml.safe_load((Path(args.root) / 'docs/v3-vault-profile-selection-fixtures.yaml').read_text(encoding='utf-8'))['cases'])} cases, two scaffold profiles and semantic contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
