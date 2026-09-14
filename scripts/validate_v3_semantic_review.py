#!/usr/bin/env python3
"""Validate the completeness envelope of the executed V3 semantic review.

This validator checks that the review package is complete, internally
consistent and provenance-safe. It does not determine whether a semantic
conclusion is true; that remains the primary and adversarial review recorded
in the evidence package.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


ALLOWED_DISPOSITIONS = {
    "accepted",
    "blocked",
    "needs_review",
    "partial",
    "provisional",
    "rework_required",
}
EXPECTED_ENGINES = {
    "crud",
    "artifact-provenance",
    "ingress",
    "rem-curation",
    "package",
    "delivery-transfer",
    "governance",
    "operational-audit",
    "migration-compatibility",
    "maintenance",
    "learning-evolution",
}
REQUIRED_CASE_FIELDS = {
    "review_id",
    "lot",
    "engine",
    "fixture",
    "source_refs",
    "primary_disposition",
    "adversarial_disposition",
    "final_disposition",
    "decision_basis",
    "negative_behavior_checked",
    "mutation",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--review", default="docs/v3-semantic-review.yaml")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    path = root / args.review
    errors: list[str] = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"validate_v3_semantic_review: FAILED — {exc}")
        return 1

    if not isinstance(data, dict):
        errors.append("review root must be a mapping")
        data = {}
    if data.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    policy = data.get("review_policy")
    if not isinstance(policy, dict):
        errors.append("review_policy must be a mapping")
    else:
        if policy.get("privacy") != "sanitized-no-real-content":
            errors.append("review_policy.privacy must be sanitized-no-real-content")
        if policy.get("record_mutations") != "none":
            errors.append("review_policy.record_mutations must be none")
        if policy.get("passes") != 2:
            errors.append("review_policy.passes must be 2")

    reconciliation = data.get("scope_reconciliation")
    if not isinstance(reconciliation, dict):
        errors.append("scope_reconciliation must be a mapping")
    else:
        if reconciliation.get("canonical_case_count") != 24:
            errors.append("canonical_case_count must be 24")
        if not reconciliation.get("corrected_conflicts"):
            errors.append("scope reconciliation must record corrected conflicts")

    sources = data.get("source_snapshots")
    if not isinstance(sources, list) or not sources:
        errors.append("source_snapshots must be a non-empty list")
        sources = []
    source_ids: set[str] = set()
    for index, source in enumerate(sources):
        label = f"source_snapshots[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{label} must be a mapping")
            continue
        source_id = source.get("id")
        if not isinstance(source_id, str) or not source_id.strip():
            errors.append(f"{label}.id must be non-empty")
        elif source_id in source_ids:
            errors.append(f"{label}.id duplicates {source_id}")
        else:
            source_ids.add(source_id)
        sha = source.get("sha256")
        if sha is not None and (not isinstance(sha, str) or len(sha) != 64):
            errors.append(f"{label}.sha256 must be a 64-character hash when present")

    cases = data.get("cases")
    if not isinstance(cases, list):
        errors.append("cases must be a list")
        cases = []
    if len(cases) != 24:
        errors.append(f"cases must contain 24 entries, found {len(cases)}")
    case_ids: set[str] = set()
    engines: set[str] = set()
    for index, case in enumerate(cases):
        label = f"cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{label} must be a mapping")
            continue
        missing = REQUIRED_CASE_FIELDS - case.keys()
        if missing:
            errors.append(f"{label} missing {sorted(missing)}")
        review_id = case.get("review_id")
        if not isinstance(review_id, str) or not review_id.strip():
            errors.append(f"{label}.review_id must be non-empty")
        elif review_id in case_ids:
            errors.append(f"{label}.review_id duplicates {review_id}")
        else:
            case_ids.add(review_id)
        engine = case.get("engine")
        if engine not in EXPECTED_ENGINES:
            errors.append(f"{label}.engine is not canonical: {engine!r}")
        else:
            engines.add(engine)
        refs = case.get("source_refs")
        if not isinstance(refs, list) or not refs or any(not isinstance(ref, str) for ref in refs):
            errors.append(f"{label}.source_refs must be a non-empty list of strings")
        for field in ("primary_disposition", "adversarial_disposition", "final_disposition"):
            if case.get(field) not in ALLOWED_DISPOSITIONS:
                errors.append(f"{label}.{field} has invalid disposition {case.get(field)!r}")
        if case.get("primary_disposition") != case.get("adversarial_disposition"):
            errors.append(f"{label} primary and adversarial dispositions disagree without adjudication")
        if case.get("adversarial_disposition") != case.get("final_disposition"):
            errors.append(f"{label} final disposition differs from adversarial disposition")
        if case.get("mutation") != "none":
            errors.append(f"{label}.mutation must be none")
        for field in ("fixture", "decision_basis", "negative_behavior_checked"):
            if not isinstance(case.get(field), str) or not case[field].strip():
                errors.append(f"{label}.{field} must be non-empty")

    if engines != EXPECTED_ENGINES:
        errors.append(f"engine coverage mismatch: {sorted(engines)}")

    if errors:
        print(f"validate_v3_semantic_review: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_v3_semantic_review: OK — 24 cases, 11 engines, 2 review passes, no Record mutations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
