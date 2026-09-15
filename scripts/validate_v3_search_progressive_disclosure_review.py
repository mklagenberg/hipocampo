#!/usr/bin/env python3
"""Validate the envelope of the candidate Search semantic review."""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml


EXPECTED = {
    "SEM-SPD-001": ("SPD-S-001", "needs_review"),
    "SEM-SPD-002": ("SPD-S-002", "blocked"),
    "SEM-SPD-003": ("SPD-S-003", "blocked"),
    "SEM-SPD-004": ("SPD-S-004", "needs_review"),
    "SEM-SPD-005": ("SPD-S-005", "needs_review"),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    path = root / "docs/v3-search-progressive-disclosure-semantic-review.yaml"
    errors: list[str] = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"validate_v3_search_progressive_disclosure_review: FAILED — {exc}")
        return 1
    if not isinstance(data, dict) or data.get("schema_version") != "1.0":
        errors.append("review schema_version must be 1.0")
        data = {}
    policy = data.get("review_policy", {})
    for key, expected in (("privacy", "sanitized-no-real-content"), ("mutation", "none"), ("human_confirmation", "required")):
        if policy.get(key) != expected:
            errors.append(f"review_policy.{key} must be {expected}")
    cases = data.get("cases", [])
    seen: set[str] = set()
    for index, case in enumerate(cases if isinstance(cases, list) else []):
        label = f"cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{label} must be a mapping")
            continue
        review_id = case.get("review_id")
        if review_id in seen:
            errors.append(f"{label} duplicates {review_id}")
        seen.add(review_id)
        if review_id not in EXPECTED:
            errors.append(f"{label} is not an assigned Search semantic review")
            continue
        case_id, disposition = EXPECTED[review_id]
        if case.get("case_id") != case_id or case.get("agent_disposition") != disposition:
            errors.append(f"{label} does not preserve the assigned case and disposition")
        if case.get("human_confirmation") != "pending":
            errors.append(f"{label} must remain pending human confirmation")
        if case.get("mutation") != "none":
            errors.append(f"{label} must declare mutation none")
        for field in ("fixture_ref", "rationale", "negative_behavior_checked"):
            if not isinstance(case.get(field), str) or not case[field].strip():
                errors.append(f"{label}.{field} must be non-empty")
        filename, separator, case_name = str(case.get("fixture_ref", "")).partition("#")
        if not separator or not (root / "docs" / filename).is_file():
            errors.append(f"{label} fixture reference is not readable")
        else:
            fixture_data = yaml.safe_load((root / "docs" / filename).read_text(encoding="utf-8"))
            if not any(item.get("id") == case_name for item in fixture_data.get("cases", [])):
                errors.append(f"{label} fixture case does not exist")
    if seen != set(EXPECTED):
        errors.append(f"review coverage mismatch: expected {sorted(EXPECTED)}, got {sorted(seen)}")
    if errors:
        print(f"validate_v3_search_progressive_disclosure_review: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_v3_search_progressive_disclosure_review: OK — 5 agent-reviewed cases pending human confirmation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
