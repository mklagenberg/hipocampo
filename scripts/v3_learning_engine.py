#!/usr/bin/env python3
"""Deterministic signal triage and semantic-review boundary for V3 learning."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json


class LearningError(ValueError):
    pass


SIGNAL_TYPES = {"repeated-block", "incident", "lesson", "false-positive", "false-negative", "new-context", "manual-override"}
ENGINE_IDS = {
    "crud", "artifact-provenance", "ingress", "rem-curation", "package",
    "delivery-transfer", "governance", "operational-audit", "migration-compatibility",
    "maintenance", "learning-evolution",
}
SIGNAL_STATES = {"observed", "triaged", "candidate", "duplicate", "rejected", "approved", "implemented", "verified", "superseded"}
REVIEW_DECISIONS = {"accepted", "provisional", "needs_review", "blocked", "rework_required"}
SENSITIVE_KEYS = {
    "password", "credential", "credentials", "secret", "token", "api_key", "raw_content",
    "record_body", "chunk_body", "artifact_body", "package_body", "sensitive_content",
}


def _sanitize(value: object, key: str | None = None) -> object:
    if key and key.lower() in SENSITIVE_KEYS:
        return "[REDACTED]"
    if isinstance(value, dict):
        return {str(item_key): _sanitize(item_value, str(item_key)) for item_key, item_value in value.items()}
    if isinstance(value, list):
        return [_sanitize(item) for item in value]
    return deepcopy(value)


def _stable_id(prefix: str, material: object) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return f"{prefix}-{hashlib.sha256(encoded).hexdigest()[:16]}"


def _required_signal(signal: dict) -> dict:
    required = {"signal_id", "source_refs", "signal_type", "engine", "observed_behavior", "expected_behavior_gap", "proposed_use_case", "privacy_status", "status"}
    missing = required - signal.keys()
    if missing:
        raise LearningError(f"learning signal is incomplete: {sorted(missing)}")
    if not signal["signal_id"] or not isinstance(signal["source_refs"], list) or not signal["source_refs"]:
        raise LearningError("learning signal requires a stable ID and source references")
    if any(not isinstance(reference, str) or not reference.strip() for reference in signal["source_refs"]):
        raise LearningError("learning signal source references must be non-empty strings")
    for field in ("observed_behavior", "expected_behavior_gap", "proposed_use_case"):
        if not isinstance(signal[field], str) or not signal[field].strip():
            raise LearningError(f"learning signal requires non-empty {field}")
    if signal["signal_type"] not in SIGNAL_TYPES:
        raise LearningError(f"unknown learning signal type: {signal['signal_type']}")
    if signal["engine"] not in ENGINE_IDS:
        raise LearningError(f"unknown target engine: {signal['engine']}")
    if signal["privacy_status"] != "sanitized":
        raise LearningError("learning signals must be sanitized before triage")
    if signal["status"] not in SIGNAL_STATES:
        raise LearningError(f"unknown learning signal state: {signal['status']}")
    return deepcopy(signal)


def normalize_signal(signal: dict) -> dict:
    """Sanitize bounded operational input and validate its learning envelope."""
    normalized = _sanitize(signal)
    result = _required_signal(normalized)
    result["source_refs"] = sorted(set(result["source_refs"]))
    result["signal_fingerprint"] = signal_fingerprint(result)
    return result


def signal_fingerprint(signal: dict) -> str:
    material = {
        "signal_type": signal.get("signal_type"),
        "engine": signal.get("engine"),
        "observed_behavior": signal.get("observed_behavior"),
        "expected_behavior_gap": signal.get("expected_behavior_gap"),
        "proposed_use_case": signal.get("proposed_use_case"),
    }
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def deduplicate_signals(signals: list[dict]) -> list[dict]:
    """Keep one representative per behavioral fingerprint and retain lineage."""
    groups: dict[str, dict] = {}
    for raw in signals:
        signal = normalize_signal(raw)
        fingerprint = signal["signal_fingerprint"]
        if fingerprint not in groups:
            groups[fingerprint] = signal
            groups[fingerprint]["occurrence_count"] = 1
            continue
        groups[fingerprint]["occurrence_count"] += 1
        groups[fingerprint]["source_refs"] = sorted(set(groups[fingerprint]["source_refs"] + signal["source_refs"]))
    return list(groups.values())


def triage_signal(signal: dict, *, known_case_fingerprints: set[str] | None = None) -> dict:
    normalized = normalize_signal(signal)
    known = known_case_fingerprints or set()
    if normalized["signal_fingerprint"] in known:
        normalized["status"] = "duplicate"
        normalized["triage"] = "existing-case"
    else:
        normalized["status"] = "candidate"
        normalized["triage"] = "new-case-candidate"
    return normalized


def build_candidate(signal: dict, *, known_case_fingerprints: set[str] | None = None) -> dict:
    triaged = triage_signal(signal, known_case_fingerprints=known_case_fingerprints)
    if triaged["status"] == "duplicate":
        return triaged
    candidate = {
        "candidate_id": _stable_id("learn", [triaged["signal_fingerprint"], triaged["source_refs"]]),
        "source_refs": deepcopy(triaged["source_refs"]),
        "signal_type": triaged["signal_type"],
        "engine": triaged["engine"],
        "observed_behavior": triaged["observed_behavior"],
        "expected_behavior_gap": triaged["expected_behavior_gap"],
        "proposed_use_case": triaged["proposed_use_case"],
        "proposed_deterministic_test": triaged.get("proposed_deterministic_test", "assert expected outcome and no unsafe side effect"),
        "proposed_semantic_test": triaged.get("proposed_semantic_test", "review applicability, provenance, privacy and unresolved meaning"),
        "risk": triaged.get("risk", "medium"),
        "privacy_status": "sanitized",
        "signal_fingerprint": triaged["signal_fingerprint"],
        "status": "candidate",
    }
    return candidate


def validate_semantic_learning_review(review: dict, *, candidate_id: str) -> dict:
    required = {"review_id", "candidate_id", "reviewer", "purpose", "evidence_refs", "rationale", "reviewed_at", "decision"}
    missing = required - review.keys()
    if missing:
        raise LearningError(f"learning review is incomplete: {sorted(missing)}")
    if review["candidate_id"] != candidate_id or not review["review_id"]:
        raise LearningError("learning review target does not match candidate")
    if review["decision"] not in REVIEW_DECISIONS:
        raise LearningError(f"unknown learning review decision: {review['decision']}")
    if not review["reviewer"] or not review["purpose"] or not review["rationale"] or not review["reviewed_at"]:
        raise LearningError("learning review requires reviewer, purpose, rationale and timestamp")
    if not isinstance(review["evidence_refs"], list) or not review["evidence_refs"]:
        raise LearningError("learning review requires evidence references")
    return deepcopy(review)


def review_candidate(candidate: dict, review: dict) -> dict:
    if candidate.get("status") != "candidate":
        raise LearningError("only a candidate can enter semantic review")
    checked = validate_semantic_learning_review(review, candidate_id=candidate["candidate_id"])
    result = deepcopy(candidate)
    result["semantic_review"] = checked
    result["status"] = "approved" if checked["decision"] == "accepted" else checked["decision"]
    return result


def materialize_case(candidate: dict) -> dict:
    if candidate.get("status") != "approved":
        raise LearningError("only an approved learning candidate can materialize a case")
    return {
        "case_id": _stable_id("case", candidate["candidate_id"]),
        "engine": candidate["engine"],
        "source_refs": deepcopy(candidate["source_refs"]),
        "candidate_id": candidate["candidate_id"],
        "deterministic_test": candidate["proposed_deterministic_test"],
        "semantic_test": candidate["proposed_semantic_test"],
        "activation": "requires-change-set-and-verification",
        "status": "proposed",
    }
