#!/usr/bin/env python3
"""Validate the second semantic review against its prior review and Constitution."""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml


ALLOWED = {"accepted", "blocked", "needs_review", "partial", "provisional", "rework_required"}
JUDGMENTS = {"compatible", "compatible-under-condition", "conflict", "obsolete", "human-review-required"}


def load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors: list[str] = []
    try:
        current = load(root / "docs/v3-semantic-constitutional-revalidation.yaml")
        prior = load(root / "docs/v3-semantic-review.yaml")
        basis = load(root / "docs/v3-constitutional-test-basis.yaml")
    except (OSError, yaml.YAMLError) as exc:
        print(f"validate_v3_semantic_constitutional_revalidation: FAILED — {exc}")
        return 1
    prior_map = {case.get("review_id"): case for case in prior.get("cases", [])}
    basis_map = {
        case.get("review_id"): case
        for case in basis.get("cases", [])
        if case.get("review_status") != "pending"
    }
    cases = current.get("cases", [])
    if current.get("review_policy", {}).get("passes") != 2:
        errors.append("constitutional revalidation must contain two passes")
    if current.get("review_policy", {}).get("record_mutations") != "none":
        errors.append("semantic revalidation must not mutate Records")
    if len(cases) != len(prior_map) or len(cases) != 28:
        errors.append(f"expected 28 revalidated cases and 28 prior cases, got current={len(cases)}, prior={len(prior_map)}")
    seen: set[str] = set()
    deltas: list[str] = []
    for index, case in enumerate(cases):
        label = f"cases[{index}]"
        review_id = case.get("review_id")
        if review_id in seen:
            errors.append(f"{label} duplicates {review_id}")
        seen.add(review_id)
        old = prior_map.get(review_id)
        basis_case = basis_map.get(review_id)
        if old is None:
            errors.append(f"{label} is absent from prior review: {review_id}")
            continue
        if basis_case is None:
            errors.append(f"{label} is absent from constitutional basis: {review_id}")
            continue
        for field in ("primary_disposition", "adversarial_disposition", "final_disposition"):
            if case.get(field) not in ALLOWED:
                errors.append(f"{label}.{field} is invalid")
        if case.get("constitutional_judgment") not in JUDGMENTS:
            errors.append(f"{label}.constitutional_judgment is invalid")
        if case.get("prior_disposition") != old.get("final_disposition"):
            errors.append(f"{label} does not preserve prior disposition")
        if case.get("final_disposition") != basis_case.get("expected_disposition"):
            errors.append(f"{label} differs from constitutional basis disposition")
        actual_delta = "unchanged" if case.get("final_disposition") == case.get("prior_disposition") else "changed"
        if case.get("delta") != actual_delta:
            errors.append(f"{label} has incorrect delta {case.get('delta')!r}; expected {actual_delta!r}")
        if case.get("primary_disposition") != case.get("adversarial_disposition") or case.get("final_disposition") != case.get("adversarial_disposition"):
            errors.append(f"{label} primary, adversarial and final dispositions disagree")
        deltas.append(case.get("delta"))
    if seen != set(prior_map):
        errors.append("revalidation review-id coverage differs from prior review")
    if set(basis_map) != seen:
        errors.append("revalidation review-id coverage differs from constitutional basis")
    if deltas.count("unchanged") != 28:
        errors.append("all 28 cases must be explicitly classified as unchanged or diagnosed")
    if errors:
        print(f"validate_v3_semantic_constitutional_revalidation: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_v3_semantic_constitutional_revalidation: OK — 28 cases compared; 28 dispositions unchanged; two passes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
