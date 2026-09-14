#!/usr/bin/env python3
"""Validate synthetic vault-shaped V2.x to V3 migration inventories."""
from __future__ import annotations

from v3_f0_engine import ROOT, load_yaml
from v3_inventory_engine import evaluate


def main() -> int:
    errors: list[str] = []
    data = load_yaml("docs/v3-synthetic-vault-inventories.yaml")
    profiles = data.get("profiles", [])
    required = {
        "id", "entity", "role", "source_version", "target_version", "access",
        "mapping", "privacy", "rollback", "target_contract", "human_approval",
        "artifact_frontier", "external_reference_preserved", "unsafe_raw_fallback",
        "expected",
    }
    if len(profiles) < 4:
        errors.append("inventory fixtures must contain at least four synthetic profiles")
    ids = [profile.get("id") for profile in profiles]
    if len(ids) != len(set(ids)):
        errors.append("inventory profile ids must be unique")
    for profile in profiles:
        missing = required - set(profile)
        if missing:
            errors.append(f"{profile.get('id', '<unknown>')} missing fields: {sorted(missing)}")
            continue
        if profile["role"] not in {"anchor", "additional"}:
            errors.append(f"{profile['id']} has invalid role: {profile['role']}")
        if profile["source_version"] == profile["target_version"]:
            errors.append(f"{profile['id']} does not represent a version transition")
        if profile["access"] == "unavailable" and profile["external_reference_preserved"]:
            errors.append(f"{profile['id']} cannot claim preserved external reference while unavailable")
        actual = evaluate(profile)
        if actual != profile["expected"]:
            errors.append(f"{profile['id']} expected {profile['expected']}, got {actual}")
    for relative in ("docs/v3-synthetic-vault-inventories.yaml", "scripts/v3_inventory_engine.py"):
        if not (ROOT / relative).exists():
            errors.append(f"missing inventory artifact: {relative}")
    if errors:
        print(f"validate_v3_inventory: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print(f"validate_v3_inventory: OK — {len(profiles)} synthetic vault profiles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
