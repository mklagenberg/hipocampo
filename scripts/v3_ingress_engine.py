#!/usr/bin/env python3
"""Processed destination-bound ingress and REM double-check for V3 X4.5."""
from __future__ import annotations

import re


class IngressError(ValueError):
    pass


SECRET_PATTERNS = (re.compile(r"(?i)api[_ -]?key\s*[:=]\s*\S+"), re.compile(r"(?i)password\s*[:=]\s*\S+"))


def process_ingress(*, record: dict, destination_vault: dict, operation: str, environment_authorized: bool,
                    approvals: list[str] | None = None) -> dict:
    if operation not in {"create", "update"}:
        raise IngressError("READ never persists ingress findings or records")
    if not environment_authorized:
        raise IngressError("processing environment is not authorized")
    if destination_vault.get("vault_id") != record.get("destination_vault_id"):
        raise IngressError("destination boundary mismatch")
    approvals = approvals or []
    content = str(record.get("content", ""))
    processed = content
    redactions: list[str] = []
    for pattern in SECRET_PATTERNS:
        if pattern.search(processed):
            processed = pattern.sub("[REDACTED]", processed)
            redactions.append("secret")
    if record.get("declassification_requested") and "owner-approval" not in approvals:
        raise IngressError("declassification requires explicit owner approval")
    queues = {
        "frontmatter": list(record.get("frontmatter_findings", [])),
        "semantic": list(record.get("semantic_findings", [])),
        "staleness": list(record.get("staleness_findings", [])),
    }
    local_record = {
        "record_id": record.get("record_id"),
        "entity": destination_vault.get("entity"),
        "vault": destination_vault,
        "content": processed,
        "processing_state": "new",
        "curation_status": "pending_rem",
        "redactions": redactions,
        "queues": queues,
        "provenance": {"source_ref": record.get("source_ref"), "destination_vault_id": destination_vault.get("vault_id")},
    }
    return {"status": "processed", "local_record": local_record, "raw_inbox": False}


def read_findings(*, record: dict) -> dict:
    """READ-only detection; persistence belongs to CREATE/UPDATE."""
    return {
        "write_performed": False,
        "frontmatter": list(record.get("frontmatter_findings", [])),
        "semantic": list(record.get("semantic_findings", [])),
        "staleness": list(record.get("staleness_findings", [])),
    }


def rem_double_check(local_record: dict, destination_vault: dict) -> dict:
    if local_record.get("vault", {}).get("vault_id") != destination_vault.get("vault_id"):
        return {"status": "blocked", "reason": "destination_boundary_mismatch"}
    if local_record.get("processing_state") != "new" or local_record.get("curation_status") != "pending_rem":
        return {"status": "blocked", "reason": "unexpected_receipt_state"}
    if "[REDACTED]" not in local_record.get("content", "") and local_record.get("redactions"):
        return {"status": "blocked", "reason": "redaction_not_materialized"}
    return {"status": "passed", "double_check": True}
