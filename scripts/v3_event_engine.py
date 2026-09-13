"""In-memory V3 operational-event, capability and revocation primitives."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json


class EventError(ValueError):
    """Raised when an operational event violates the candidate contract."""


LAYERS = {"transient_session", "sensory_capture", "durable_operational"}
CAPABILITY_STATES = {"proven", "observational", "unavailable", "authorization_required"}
SENSITIVE_KEYS = {
    "password", "credential", "credentials", "secret", "token", "api_key",
    "source_body", "record_body", "chunk_body", "artifact_body", "package_body",
    "knowledge_body", "sensitive_content",
}


def _redact(value: object, key: str | None = None) -> object:
    if key and key.lower() in SENSITIVE_KEYS:
        return "[REDACTED]"
    if isinstance(value, dict):
        return {str(item_key): _redact(item_value, str(item_key)) for item_key, item_value in value.items()}
    if isinstance(value, list):
        return [_redact(item) for item in value]
    return deepcopy(value)


def _stable_id(prefix: str, material: object) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return f"{prefix}-{hashlib.sha256(encoded).hexdigest()[:16]}"


def build_event(
    event_type: str,
    layer: str,
    *,
    actor: dict,
    target: dict,
    payload: dict,
    rule_revision: str,
    proof_scope: str,
    limits: list[str],
    retention: str,
    correlation: dict | None = None,
    capabilities: dict | None = None,
) -> dict:
    if not event_type or layer not in LAYERS:
        raise EventError("event_type and a supported event layer are required")
    if not actor or not target or not rule_revision or not proof_scope or not retention:
        raise EventError("event requires actor, target, rule revision, proof scope and retention")
    if not isinstance(payload, dict):
        raise EventError("event payload must be a mapping")
    safe_payload = _redact(payload)
    event = {
        "event_id": _stable_id("evt", [event_type, layer, actor, target, safe_payload, rule_revision]),
        "event_type": event_type,
        "layer": layer,
        "actor": deepcopy(actor),
        "target": deepcopy(target),
        "payload": safe_payload,
        "rule_revision": rule_revision,
        "proof_scope": proof_scope,
        "limits": list(limits),
        "retention": retention,
    }
    if correlation is not None:
        event["correlation"] = deepcopy(correlation)
    if capabilities is not None:
        event["capabilities"] = deepcopy(capabilities)
    return event


def build_correlation(
    *,
    correlation_id: str,
    causation_id: str | None,
    targets: list[dict],
    fingerprints: list[str],
    evidence_refs: list[str],
    rule_revision: str,
    state: str,
    inaccessible_frontiers: list[dict] | None = None,
) -> dict:
    if not correlation_id or not targets or not rule_revision or not state:
        raise EventError("correlation requires ID, targets, rule revision and state")
    return {
        "correlation_id": correlation_id,
        "causation_id": causation_id,
        "targets": deepcopy(targets),
        "fingerprints": list(fingerprints),
        "evidence_refs": list(evidence_refs),
        "rule_revision": rule_revision,
        "state": state,
        "inaccessible_frontiers": deepcopy(inaccessible_frontiers or []),
    }


def build_capability_matrix(entries: list[dict]) -> dict:
    if not entries:
        raise EventError("capability matrix cannot be empty")
    normalized = []
    for entry in entries:
        if not entry.get("capability") or entry.get("state") not in CAPABILITY_STATES:
            raise EventError("each capability needs a name and supported state")
        normalized.append({
            "capability": entry["capability"],
            "state": entry["state"],
            "evidence": entry.get("evidence"),
            "scope": entry.get("scope", "local-host"),
            "tested_at": entry.get("tested_at"),
        })
    return {"host": "codex-local", "capabilities": normalized}


def session_disposition(*, capture_requested: bool, capture_authorized: bool, interrupted: bool = False) -> dict:
    if capture_requested and capture_authorized:
        disposition = "capture_authorized"
    else:
        disposition = "discard_transient_context"
    return {
        "disposition": disposition,
        "interrupted": interrupted,
        "durable_log_allowed": False,
        "reason": "explicit_capture_required" if disposition != "capture_authorized" else "explicit_authorization",
    }


def build_revocation_event(
    *,
    target_id: str,
    requester_id: str,
    approver_id: str | None,
    scope: str,
    surfaces: list[dict],
    reason_class: str,
) -> dict:
    if not target_id or not requester_id or not scope or not reason_class or not surfaces:
        raise EventError("revocation requires target, requester, scope, reason and surfaces")
    reach = []
    for surface in surfaces:
        name = surface.get("surface")
        if not name:
            raise EventError("revocation surfaces require names")
        reachable = bool(surface.get("reachable", False))
        requires_block = bool(surface.get("requires_block", True))
        reach.append({
            "surface": name,
            "status": "invalidated" if reachable else "not_reached",
            "reachable": reachable,
            "blocked": (not reachable and requires_block),
            "evidence": surface.get("evidence"),
        })
    return {
        "event_type": "revocation_requested",
        "target_id": target_id,
        "requester_id": requester_id,
        "approver_id": approver_id,
        "scope": scope,
        "reason_class": reason_class,
        "reach": reach,
        "result": "partially_completed" if any(item["blocked"] for item in reach) else "completed",
    }


def assert_safe_event(event: dict) -> None:
    if not event.get("event_id") or event.get("layer") not in LAYERS:
        raise EventError("event envelope is incomplete")
    payload = event.get("payload", {})
    for key, value in payload.items():
        if key.lower() in SENSITIVE_KEYS and value != "[REDACTED]":
            raise EventError(f"sensitive payload key was not redacted: {key}")
