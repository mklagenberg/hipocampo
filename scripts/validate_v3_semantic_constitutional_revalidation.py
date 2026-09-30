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
        search_current = load(root / "docs/v3-search-constitutional-revalidation.yaml")
        search_prior = load(root / "docs/v3-search-progressive-disclosure-semantic-review.yaml")
    except (OSError, yaml.YAMLError) as exc:
        print(f"validate_v3_semantic_constitutional_revalidation: FAILED — {exc}")
        return 1
    prior_map = {case.get("review_id"): case for case in prior.get("cases", [])}
    basis_all = {case.get("review_id"): case for case in basis.get("cases", [])}
    # Keep the original 28-case historical round scoped to its own review IDs;
    # the five later Search cases are validated as an additive supplement below.
    basis_map = {review_id: basis_all[review_id] for review_id in prior_map if review_id in basis_all}
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

    search_review_map = {case.get("review_id"): case for case in search_prior.get("cases", [])}
    search_cases = search_current.get("cases", [])
    if search_current.get("historical_revalidation") != "v3-semantic-constitutional-revalidation.yaml":
        errors.append("Search supplement must point to the preserved historical constitutional round")
    if search_current.get("review_policy", {}).get("passes") != 2:
        errors.append("Search constitutional supplement must contain two review passes")
    if search_current.get("review_policy", {}).get("record_mutations") != "none":
        errors.append("Search constitutional supplement must declare no Record mutations")
    required_search_ids = {f"SEM-SPD-{index:03d}" for index in range(1, 6)}
    search_seen: set[str] = set()
    allowed_dispositions = ALLOWED
    for index, case in enumerate(search_cases if isinstance(search_cases, list) else []):
        label = f"search_cases[{index}]"
        review_id = case.get("review_id")
        if not isinstance(review_id, str) or review_id in search_seen:
            errors.append(f"{label}.review_id is missing or duplicated")
            continue
        search_seen.add(review_id)
        previous = search_review_map.get(review_id)
        basis_case = basis_all.get(review_id)
        if previous is None or basis_case is None:
            errors.append(f"{label} lacks a prior Search review or constitutional basis")
            continue
        if previous.get("human_confirmation") != "confirmed" or not previous.get("confirmation_basis"):
            errors.append(f"{label} cannot enter canonical revalidation before human confirmation")
        if case.get("case_id") != previous.get("case_id"):
            errors.append(f"{label} does not preserve its prior Search case identity")
        if case.get("prior_disposition") != previous.get("agent_disposition"):
            errors.append(f"{label} does not preserve the prior Search disposition")
        if basis_case.get("review_status") != "confirmed" or basis_case.get("human_confirmation") != "confirmed":
            errors.append(f"{label} constitutional basis is not marked confirmed")
        if basis_case.get("revalidation_run_id") != search_current.get("run_id"):
            errors.append(f"{label} basis is not linked to this revalidation run")
        if case.get("final_disposition") != basis_case.get("expected_disposition"):
            errors.append(f"{label} differs from its constitutional basis disposition")
        judgments = (
            case.get("primary_constitutional_judgment"),
            case.get("adversarial_constitutional_judgment"),
            case.get("final_constitutional_judgment"),
        )
        if any(judgment not in JUDGMENTS for judgment in judgments):
            errors.append(f"{label} has an invalid constitutional judgment")
        if len(set(judgments)) != 1:
            errors.append(f"{label} primary, adversarial and final constitutional judgments disagree")
        dispositions = (
            case.get("primary_disposition"),
            case.get("adversarial_disposition"),
            case.get("final_disposition"),
        )
        if any(disposition not in allowed_dispositions for disposition in dispositions):
            errors.append(f"{label} has an invalid semantic disposition")
        if len(set(dispositions)) != 1:
            errors.append(f"{label} primary, adversarial and final dispositions disagree")
        actual_delta = "unchanged" if case.get("final_disposition") == case.get("prior_disposition") else "changed"
        if case.get("delta") != actual_delta:
            errors.append(f"{label} has incorrect disposition delta; expected {actual_delta}")
        for field in ("primary_rationale", "adversarial_rationale", "diagnosis"):
            if not isinstance(case.get(field), str) or not case[field].strip():
                errors.append(f"{label}.{field} must be non-empty")
        if case.get("mutation") != "none":
            errors.append(f"{label}.mutation must be none")
    if search_seen != required_search_ids:
        errors.append(f"Search supplement coverage mismatch: expected {sorted(required_search_ids)}, got {sorted(search_seen)}")
    if errors:
        print(f"validate_v3_semantic_constitutional_revalidation: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_v3_semantic_constitutional_revalidation: OK — historical 28/28 preserved; 5 Search cases revalidated in two passes; zero disposition deltas or Record mutations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
