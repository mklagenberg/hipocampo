#!/usr/bin/env python3
"""Scoped profile lifecycle and local violation audit for V3 X4.6."""
from __future__ import annotations


class ProfileError(ValueError):
    pass


ROLES = {"owner", "authority", "curator", "user"}


def evaluate_profile(link: dict, *, at: str, required_role: str | None = None) -> dict:
    if link.get("role") not in ROLES:
        raise ProfileError("unknown governance role")
    valid = link.get("accepted") is True and link.get("revoked") is not True
    if link.get("valid_from") and at < link["valid_from"]:
        valid = False
    if link.get("valid_until") and at > link["valid_until"]:
        valid = False
    if required_role and link.get("role") != required_role:
        valid = False
    return {"valid": valid, "status": "accepted" if valid else "not_authorized", "scope": link.get("scope")}


def accept_profile(*, user_id: str, entity: str, vault_id: str, role: str, scope: str, version: int, recorded_at: str) -> dict:
    if role not in ROLES:
        raise ProfileError("unknown governance role")
    return {
        "user_id": user_id, "entity": entity, "vault_id": vault_id, "role": role, "scope": scope,
        "version": version, "accepted": True, "revoked": False, "recorded_at": recorded_at,
    }


def revoke_profile(link: dict, *, recorded_by: str, recorded_at: str, reason: str) -> dict:
    result = dict(link)
    result.update({"revoked": True, "revoked_by": recorded_by, "revoked_at": recorded_at, "revocation_reason": reason})
    return result


def record_violation(*, vault_id: str, actor: dict, event: dict, recorded_at: str) -> dict:
    if actor.get("vault_id") != vault_id or not actor.get("can_write_audit", False):
        raise ProfileError("actor cannot write this vault audit")
    required = ("what", "destination", "result")
    if any(not event.get(key) for key in required):
        raise ProfileError("violation event is incomplete")
    return {
        "audit_id": f"audit-{len(event.get('what', ''))}-{recorded_at}",
        "vault_id": vault_id,
        "who": actor.get("user_id"),
        "when": recorded_at,
        "what": event["what"],
        "destination": event["destination"],
        "result": event["result"],
        "attempt": bool(event.get("attempt", True)),
        "correction_of": event.get("correction_of"),
    }


def append_correction(audit: list[dict], *, original_audit_id: str, correction: dict, actor: dict, recorded_at: str) -> list[dict]:
    event = record_violation(
        vault_id=actor.get("vault_id", ""), actor=actor,
        event={**correction, "correction_of": original_audit_id}, recorded_at=recorded_at,
    )
    return [*audit, event]
