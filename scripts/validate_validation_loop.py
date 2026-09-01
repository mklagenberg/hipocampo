#!/usr/bin/env python3
"""Validate decision outcomes for the correction/revalidation loop."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

def expected(scenario: dict) -> str:
    return "stop" if scenario["source"] == "unavailable" or scenario["scope_change"] or scenario["repeated_without_evidence"] else "revalidate"

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    path = Path(args.root).resolve() / "docs" / "validation-loop-fixtures.yaml"
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"validate_validation_loop: FAILED — {exc}")
        return 1
    errors = []
    scenarios = data.get("scenarios", [])
    for scenario in scenarios:
        actual = scenario.get("expected")
        if actual != expected(scenario):
            errors.append(f"{scenario.get('id')}: expected {expected(scenario)!r}, got {actual!r}")
    if errors:
        print(f"validate_validation_loop: FAILED — {len(errors)} error(s)")
        for error in errors: print(f"  [FAIL] {error}")
        return 1
    print(f"validate_validation_loop: OK — {len(scenarios)} scenarios")
    return 0

if __name__ == "__main__":
    sys.exit(main())
