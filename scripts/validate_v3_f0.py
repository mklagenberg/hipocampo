#!/usr/bin/env python3
"""Integrated deterministic validation for the unreleased V3 F0 candidate."""
from __future__ import annotations

from v3_f0_engine import ALLOWED_CLASSES, ROOT, load_yaml, operational_scripts, outcome


def main() -> int:
    errors: list[str] = []
    classification = load_yaml("docs/v3-f0-script-classification.yaml")
    listed = {item["path"] for item in classification["scripts"]}
    missing = operational_scripts() - listed
    if missing:
        errors.append(f"unclassified operational scripts: {sorted(missing)}")
    for item in classification["scripts"]:
        if item["class"] not in ALLOWED_CLASSES:
            errors.append(f"invalid script class: {item}")
        if not (ROOT / item["path"]).exists():
            errors.append(f"missing classified script: {item['path']}")
        if not item.get("proof"):
            errors.append(f"missing proof boundary: {item['path']}")

    matrix = load_yaml("docs/v3-f0-verification-matrix.yaml")
    phases = {item["id"]: item for item in matrix["phases"]}
    expected_phases = {"execution", "review", "publication", "migration", "retraction"}
    if set(phases) != expected_phases:
        errors.append("phase matrix does not cover execution, review, publication, migration and retraction")
    for phase, data in phases.items():
        if not data.get("required_checks") or not data.get("blocking_results") or not data.get("evidence"):
            errors.append(f"incomplete phase matrix: {phase}")

    hardcodes = load_yaml("docs/v3-f0-hardcode-review.yaml")
    if not hardcodes.get("findings") or any(item["status"] not in {"resolved", "justified", "reviewed"} for item in hardcodes["findings"]):
        errors.append("hardcode review has unresolved findings")

    fixtures = load_yaml("docs/v3-f0-fixtures.yaml")["fixtures"]
    for fixture in fixtures:
        authorization_missing = fixture["id"] == "f0-authorization-required-migration"
        actual = outcome(fixture["required"], fixture["observed"], fixture["blocking"], authorization_missing=authorization_missing)
        if actual != fixture["expected"]:
            errors.append(f"fixture {fixture['id']} expected {fixture['expected']}, got {actual}")

    required_docs = [
        "docs/v3-f0-contract.md",
        "docs/v3-f0-script-classification.yaml",
        "docs/v3-f0-verification-matrix.yaml",
        "docs/v3-f0-hardcode-review.yaml",
        "docs/v3-f0-fixtures.yaml",
    ]
    for relative in required_docs:
        if not (ROOT / relative).exists():
            errors.append(f"missing F0 artifact: {relative}")
    if errors:
        print(f"validate_v3_f0: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_v3_f0: OK — inventory, phase matrix, hardcode review, typed outcomes and fixtures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
