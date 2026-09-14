#!/usr/bin/env python3
"""Validate the structural envelope of the unreleased V3 semantic fixtures.

This intentionally does not judge semantic truth.  It checks that each case
declares the context needed for a human/agent-reviewed evaluation and that no
fixture silently presents itself as an automated acceptance test.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


REQUIRED_CASE_FIELDS = {
    "id",
    "input_kind",
    "expected_epistemic",
    "expected_maturity",
    "required_guard",
    "negative_behavior",
    "review_boundary",
}
ALLOWED_REVIEW_BOUNDARIES = {
    "human-semantic-review",
    "explicit-human-decision",
    "REM-or-human-review",
    "host-or-human-review",
    "research-or-human-review",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--fixture", default="docs/v3-semantic-fixtures.yaml")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    fixture_path = root / args.fixture
    errors: list[str] = []
    try:
        data = yaml.safe_load(fixture_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"validate_semantic_fixtures: FAILED — {exc}")
        return 1

    if not isinstance(data, dict):
        errors.append("fixture root must be a mapping")
        data = {}
    policy = data.get("fixture_policy")
    if not isinstance(policy, dict):
        errors.append("fixture_policy must be a mapping")
    elif policy.get("privacy") != "sanitized-no-real-content":
        errors.append("fixture_policy.privacy must be sanitized-no-real-content")
    elif "structure only" not in str(policy.get("validator_limit", "")):
        errors.append("fixture_policy.validator_limit must declare the structural limit")

    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("cases must be a non-empty list")
        cases = []
    ids: set[str] = set()
    for index, case in enumerate(cases):
        label = f"cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{label} must be a mapping")
            continue
        missing = REQUIRED_CASE_FIELDS - case.keys()
        if missing:
            errors.append(f"{label} missing {sorted(missing)}")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            errors.append(f"{label}.id must be a non-empty string")
        elif case_id in ids:
            errors.append(f"{label}.id duplicates {case_id!r}")
        else:
            ids.add(case_id)
        boundary = case.get("review_boundary")
        if boundary not in ALLOWED_REVIEW_BOUNDARIES:
            errors.append(f"{label}.review_boundary {boundary!r} is not allowed")
        for field in REQUIRED_CASE_FIELDS - {"id", "review_boundary"}:
            if not isinstance(case.get(field), str) or not case[field].strip():
                errors.append(f"{label}.{field} must be a non-empty string")

    if errors:
        print(f"validate_semantic_fixtures: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print(f"validate_semantic_fixtures: OK — {len(cases)} fixtures; structure only")
    return 0


if __name__ == "__main__":
    sys.exit(main())
