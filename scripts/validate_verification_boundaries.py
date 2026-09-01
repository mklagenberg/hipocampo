#!/usr/bin/env python3
"""Validate the structured proof-boundary registry."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

FIELDS = ("id", "mechanism", "inputs", "outputs", "coverage", "rule_revision",
          "legacy_treatment", "limits", "human_or_environmental_boundary")

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    path = root / "docs" / "verification-boundaries.yaml"
    errors: list[str] = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"validate_verification_boundaries: FAILED — {exc}")
        return 1
    if data.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        errors.append("entries must be a non-empty list")
        entries = []
    ids: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"entry {index} is not a mapping")
            continue
        missing = [field for field in FIELDS if not entry.get(field)]
        errors.extend(f"entry {index} missing {field}" for field in missing)
        entry_id = entry.get("id")
        if entry_id in ids:
            errors.append(f"duplicate entry id {entry_id!r}")
        ids.add(entry_id)
        mechanism = entry.get("mechanism", "")
        if mechanism.startswith("scripts/") and not (root / mechanism).is_file():
            errors.append(f"entry {entry_id!r} names missing mechanism {mechanism!r}")
    if errors:
        print(f"validate_verification_boundaries: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print(f"validate_verification_boundaries: OK — {len(entries)} boundary entries")
    return 0

if __name__ == "__main__":
    sys.exit(main())
