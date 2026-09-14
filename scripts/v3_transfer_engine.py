#!/usr/bin/env python3
"""Distinct delivery, acceptance and retraction primitives for V3 X4.3."""
from __future__ import annotations

from v3_crud_engine import ContractError, RecordCrud
from v3_policy_engine import evaluate_policy


class TransferError(ValueError):
    pass


def deliver_package(package: dict, *, source_policy: dict, destination_policy: dict, context: dict) -> dict:
    decision = evaluate_policy(source_policy, destination_policy, context)
    if not decision["allowed"]:
        return {"status": "blocked", "policy": decision}
    return {
        "status": "delivered",
        "delivery_id": package.get("delivery", {}).get("delivery_id"),
        "package_id": package.get("package", {}).get("package_id"),
        "policy": decision,
        "current_use": False,
        "publication": "not_performed",
    }


def accept_received(
    received: dict,
    *,
    rem_status: str,
    semantic_status: str = "accepted",
    crud: RecordCrud | None = None,
    semantic_review: dict | None = None,
    actor: str = "",
    reason: str = "accepted received Package",
) -> dict:
    if received.get("acceptance") != "accepted":
        raise TransferError("only an accepted receipt can become current")
    if rem_status != "passed":
        return {"status": "pending_rem", "current_use": False}
    if semantic_status not in {"accepted", "accepted_with_perspectives"}:
        return {"status": "pending_semantic_review", "current_use": False}
    if crud is None or semantic_review is None:
        return {"status": "pending_crud", "current_use": False}
    local_record = dict(received.get("local_record", {}))
    local_record["processing_state"] = "consolidated"
    local_record["curation_status"] = "curated"
    local_record["maturity"] = "curated"
    local_record["current_use"] = True
    try:
        result = crud.create(
            local_record,
            semantic_review=semantic_review,
            actor=actor,
            reason=reason,
            idempotency_key=f"receive-current:{local_record.get('record_id', '')}",
        )
    except (ContractError, TypeError) as exc:
        raise TransferError(str(exc)) from exc
    return {"status": "current", "current_use": True, "local_record": result["record"], "crud_event": result["event"]}


def retract_delivery(*, delivery_id: str, package_id: str, reason: str, recorded_by: str, recorded_at: str) -> dict:
    if not all([delivery_id, package_id, reason, recorded_by, recorded_at]):
        raise TransferError("retraction requires complete control metadata")
    return {
        "event_type": "package_retraction",
        "delivery_id": delivery_id,
        "package_id": package_id,
        "reason": reason,
        "recorded_by": recorded_by,
        "recorded_at": recorded_at,
        "tombstone": True,
        "preserve_history": True,
        "current_use": False,
    }
