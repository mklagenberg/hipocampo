#!/usr/bin/env python3
"""Validate the synthetic V2.x to V3 migration preflight fixtures."""
from __future__ import annotations

from v3_f0_engine import ROOT, load_yaml
from v3_migration_engine import evaluate


def main() -> int:
    errors: list[str] = []
    data = load_yaml("docs/v3-migration-fixtures.yaml")
    cases = data.get("cases", [])
    required = {
        "source_version",
        "target_version",
        "mapping",
        "privacy",
        "rollback",
        "target_contract",
        "human_approval",
        "unsafe_raw_fallback",
        "expected",
    }
    if len(cases) < 8:
        errors.append("migration fixtures must cover at least eight synthetic cases")
    for case in cases:
        missing = required - set(case)
        if missing:
            errors.append(f"{case.get('id', '<unknown>')} missing fields: {sorted(missing)}")
            continue
        actual = evaluate(case)
        if actual != case["expected"]:
            errors.append(f"{case['id']} expected {case['expected']}, got {actual}")
        if case["source_version"] == case["target_version"]:
            errors.append(f"{case['id']} does not represent a version transition")
    for relative in ("docs/v3-migration-fixtures.yaml", "scripts/v3_migration_engine.py"):
        if not (ROOT / relative).exists():
            errors.append(f"missing migration artifact: {relative}")
    if errors:
        print(f"validate_v3_migration: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print(f"validate_v3_migration: OK — {len(cases)} synthetic cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
