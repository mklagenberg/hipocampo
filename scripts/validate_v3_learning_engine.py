#!/usr/bin/env python3
"""Execute deterministic and semantic-boundary cases for V3 Learning & Evolution."""
from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path

import yaml

from v3_learning_engine import (
    LearningError,
    build_candidate,
    deduplicate_signals,
    materialize_case,
    normalize_signal,
    review_candidate,
    signal_fingerprint,
)


def signal(signal_id: str = "sig-001", *, behavior: str = "blocked partial Package", source_ref: str = "meta/events/evt-001") -> dict:
    return {
        "signal_id": signal_id,
        "source_refs": [source_ref],
        "signal_type": "repeated-block",
        "engine": "package",
        "observed_behavior": behavior,
        "expected_behavior_gap": "missing explicit current-use context",
        "proposed_use_case": "partial-package-current-use-boundary",
        "proposed_deterministic_test": "block current-use Package without parent context",
        "proposed_semantic_test": "review whether selected context is sufficient for the stated purpose",
        "risk": "medium",
        "privacy_status": "sanitized",
        "status": "observed",
    }


def review(candidate_id: str, *, decision: str = "accepted") -> dict:
    return {
        "review_id": f"review-{candidate_id}",
        "candidate_id": candidate_id,
        "reviewer": "reviewer-001",
        "purpose": "learning engine case discovery",
        "evidence_refs": ["meta/audits/learning-001.yaml"],
        "rationale": "Repeated sanitized operational signal reveals a bounded test gap.",
        "reviewed_at": "2026-09-14T12:00:00Z",
        "decision": decision,
    }


def expect_error(callback, label: str, errors: list[str]) -> None:
    try:
        callback()
    except LearningError:
        return
    errors.append(f"{label}: expected LearningError")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    data = yaml.safe_load((root / "docs/engines/learning-evolution-cases.yaml").read_text(encoding="utf-8"))
    errors: list[str] = []
    if len(data.get("deterministic_cases", [])) != 9 or len(data.get("semantic_cases", [])) != 4:
        errors.append("learning engine must declare nine deterministic and four semantic cases")

    normalized = normalize_signal(signal())
    if normalized["signal_fingerprint"] != signal_fingerprint(normalized) or normalized["privacy_status"] != "sanitized":
        errors.append("D-01 signal normalization lost privacy or stable fingerprint")
    secret = signal("sig-secret")
    secret["telemetry"] = {"api_key": "SECRET", "record_body": "private"}
    safe = normalize_signal(secret)
    if safe["telemetry"]["api_key"] != "[REDACTED]" or safe["telemetry"]["record_body"] != "[REDACTED]":
        errors.append("D-02 signal sanitizer failed to redact sensitive telemetry")

    second = signal("sig-002", source_ref="meta/events/evt-002")
    groups = deduplicate_signals([signal(), second])
    if len(groups) != 1 or groups[0]["occurrence_count"] != 2 or len(groups[0]["source_refs"]) != 2:
        errors.append("D-03 deduplication did not preserve repeated-signal lineage")
    duplicate = build_candidate(signal(), known_case_fingerprints={normalized["signal_fingerprint"]})
    if duplicate.get("status") != "duplicate":
        errors.append("D-04 known signal was not classified as duplicate")

    candidate = build_candidate(signal("sig-new"))
    if candidate.get("status") != "candidate" or not candidate.get("candidate_id"):
        errors.append("D-05 new signal did not produce a stable candidate")
    expect_error(lambda: materialize_case(candidate), "D-06 unreviewed candidate activation", errors)
    incomplete = deepcopy(candidate)
    incomplete["privacy_status"] = "raw"
    expect_error(lambda: normalize_signal(incomplete), "D-07 unsanitized signal", errors)
    malformed_refs = signal("sig-malformed")
    malformed_refs["source_refs"] = ["meta/events/evt-001", 42]
    expect_error(lambda: normalize_signal(malformed_refs), "D-08 malformed source references", errors)
    if not candidate["source_refs"] or candidate["engine"] != "package":
        errors.append("D-09 candidate lost source traceability or engine ownership")

    approved = review_candidate(candidate, review(candidate["candidate_id"]))
    case = materialize_case(approved)
    if approved["status"] != "approved" or case["activation"] != "requires-change-set-and-verification":
        errors.append("S-01 accepted candidate bypassed the governed activation boundary")
    expect_error(lambda: review_candidate(candidate, {"review_id": "incomplete"}), "S-02 incomplete semantic review", errors)
    provisional_candidate = build_candidate(signal("sig-provisional", behavior="lesson needs bounded wording"))
    provisional = review_candidate(provisional_candidate, review(provisional_candidate["candidate_id"], decision="provisional"))
    if provisional.get("status") != "provisional":
        errors.append("S-03 provisional semantic decision was not preserved")
    blocked_candidate = build_candidate(signal("sig-blocked", behavior="incident contains unresolved privacy risk"))
    blocked = review_candidate(blocked_candidate, review(blocked_candidate["candidate_id"], decision="blocked"))
    if blocked.get("status") != "blocked":
        errors.append("S-04 blocked semantic decision was not preserved")

    if errors:
        print(f"validate_v3_learning_engine: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_v3_learning_engine: OK — signal sanitization, deduplication, candidate review, activation boundary and lineage")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
