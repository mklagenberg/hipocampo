#!/usr/bin/env python3
"""Explainable source/destination policy intersection for V3 X4.1."""
from __future__ import annotations


class PolicyError(ValueError):
    pass


OUTCOMES = {"permitido", "redigido", "provisório", "bloqueado"}
VISIBILITY_RANK = {"public": 0, "internal": 1, "confidential": 2, "restricted": 3}


def _required(policy: dict, keys: tuple[str, ...], label: str) -> None:
    missing = [key for key in keys if not policy.get(key)]
    if missing:
        raise PolicyError(f"{label} policy missing required fields: {', '.join(missing)}")


def evaluate_policy(source_policy: dict, destination_policy: dict, context: dict) -> dict:
    """Evaluate origin permission and destination acceptance independently.

    The result intentionally contains only the minimum identifiers needed for
    explanation. It never copies source content or inaccessible source details.
    """
    _required(source_policy, ("entity", "vault_id"), "source")
    _required(destination_policy, ("entity", "vault_id"), "destination")
    _required(context, ("purpose", "visibility"), "operation")
    if context.get("boundary_evaluable") is False:
        return _blocked("objective_evaluation_failure", "policy boundary could not be evaluated")
    purpose = context["purpose"]
    visibility = context["visibility"]
    source_allowed = bool(source_policy.get("can_send", False))
    destination_allowed = bool(destination_policy.get("can_receive", False))
    source_purposes = source_policy.get("allowed_purposes", [])
    destination_purposes = destination_policy.get("allowed_purposes", [])
    if purpose not in source_purposes:
        return _blocked("origin_purpose_denied", "origin contract does not authorize this purpose")
    if purpose not in destination_purposes:
        return _blocked("destination_purpose_denied", "destination contract does not accept this purpose")
    if not source_allowed:
        return _blocked("origin_denied", "origin contract denied delivery")
    if not destination_allowed:
        return _blocked("destination_denied", "destination contract denied receipt")
    source_rank = VISIBILITY_RANK.get(visibility)
    destination_rank = VISIBILITY_RANK.get(destination_policy.get("maximum_visibility"))
    if source_rank is None or destination_rank is None:
        return _blocked("unknown_visibility", "visibility cannot be compared")
    redactions = list(context.get("redactions", []))
    if source_rank > destination_rank:
        if not redactions or not destination_policy.get("accepts_redaction", False):
            return _blocked("visibility_incompatible", "destination cannot receive effective visibility")
        outcome = "redigido"
    else:
        outcome = "permitido"
    if context.get("semantic_status") in {"uncertain", "unresolved", "conflict"}:
        if destination_policy.get("accepts_provisional", False):
            outcome = "provisório"
        else:
            return _blocked("destination_rejects_provisional", "semantic uncertainty is not accepted for this purpose")
    return {
        "outcome": outcome,
        "allowed": outcome != "bloqueado",
        "explanation": {
            "purpose": purpose,
            "source_entity": source_policy["entity"],
            "destination_entity": destination_policy["entity"],
            "source_vault_id": source_policy["vault_id"],
            "destination_vault_id": destination_policy["vault_id"],
            "source_gate": "authorized",
            "destination_gate": "accepted",
            "redactions": redactions,
        },
        "semantic_boundary": "semantic uncertainty remains explicit; no truth claim was made",
    }


def _blocked(code: str, message: str) -> dict:
    return {
        "outcome": "bloqueado",
        "allowed": False,
        "explanation": {"rule": code, "message": message},
        "semantic_boundary": "blocked by an objective policy boundary",
    }


def evaluate_passage(source_policy: dict, destination_policy: dict, *, passage: str, context: dict) -> dict:
    result = evaluate_policy(source_policy, destination_policy, {**context, "passage": passage})
    result["passage"] = passage
    return result
