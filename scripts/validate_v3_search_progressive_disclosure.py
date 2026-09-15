#!/usr/bin/env python3
"""Validate the deterministic envelope of the unreleased V3 search contract.

This validates contract shape and sanitized fixtures only. It does not prove
relevance, authority, privacy permission or semantic truth.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml


LEVELS = ["L0", "L1", "L2", "L3", "L4"]
EXPECTED = {
    "reject-unauthorized-expansion": ("blocked", "L0"),
    "preserve-independent-dimensions": ("needs_review", "L2"),
    "prose-default": ("partial", "L2"),
    "structured-only-on-request": ("accepted", "L2"),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    contract_path = root / "docs/v3-search-progressive-disclosure-contract.md"
    fixture_path = root / "docs/v3-search-progressive-disclosure-fixtures.yaml"
    errors: list[str] = []
    try:
        contract = contract_path.read_text(encoding="utf-8")
        fixtures = yaml.safe_load(fixture_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"validate_v3_search_progressive_disclosure: FAILED — {exc}")
        return 1

    required_sections = (
        "## Request envelope",
        "## Result envelope",
        "## Disclosure levels",
        "## Presentation policy",
        "## Guardrails and semantic boundary",
        "## CRUD and operational trail",
    )
    for section in required_sections:
        if section not in contract:
            errors.append(f"contract is missing {section}")
    for level in LEVELS:
        if f"`{level}`" not in contract:
            errors.append(f"contract does not declare {level}")
    for phrase in ("read-only", "mutation: \"none\"", "explicit authorization", "fail closed"):
        if phrase not in contract:
            errors.append(f"contract is missing guardrail text: {phrase}")

    if not isinstance(fixtures, dict):
        errors.append("fixture root must be a mapping")
        fixtures = {}
    if fixtures.get("schema_version") != "1.0":
        errors.append("fixture schema_version must be 1.0")
    policy = fixtures.get("fixture_policy", {})
    if policy.get("privacy") != "sanitized-no-real-content":
        errors.append("fixtures must declare sanitized-no-real-content")
    if policy.get("mutation") != "none":
        errors.append("fixtures must declare mutation none")
    if fixtures.get("levels") != LEVELS:
        errors.append("fixture levels must be exactly L0 through L4")

    cases = fixtures.get("cases", [])
    seen: set[str] = set()
    for index, case in enumerate(cases if isinstance(cases, list) else []):
        label = f"cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{label} must be a mapping")
            continue
        case_id = case.get("id")
        if case_id in seen:
            errors.append(f"{label} duplicates {case_id}")
        seen.add(case_id)
        if case_id not in EXPECTED:
            errors.append(f"{label} is not an assigned deterministic case")
            continue
        disposition, level = EXPECTED[case_id]
        if case.get("expected_disposition") != disposition:
            errors.append(f"{label} has unexpected disposition")
        if case.get("expected_disclosure_level") != level:
            errors.append(f"{label} has unexpected disclosure level")
        if case.get("mutation") != "none":
            errors.append(f"{label} must not mutate")
        if "content" in case or "record_body" in case:
            errors.append(f"{label} must not contain Record or Chunk body content")
    if seen != set(EXPECTED):
        errors.append(f"fixture case coverage mismatch: expected {sorted(EXPECTED)}, got {sorted(seen)}")
    expansion = next((case for case in cases if case.get("id") == "reject-unauthorized-expansion"), {})
    if expansion.get("requested_disclosure") != "L4" or expansion.get("explicit_expansion_authorization") is not False:
        errors.append("unauthorized expansion case must request L4 without authorization")
    independent = next((case for case in cases if case.get("id") == "preserve-independent-dimensions"), {})
    if independent.get("relevance") != "high" or independent.get("authority") != "unknown" or independent.get("epistemic_status") != "unresolved-conflict":
        errors.append("independent-dimensions case must keep high relevance separate from authority and epistemic state")

    if errors:
        print(f"validate_v3_search_progressive_disclosure: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_v3_search_progressive_disclosure: OK — contract envelope and 4 sanitized fixtures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
