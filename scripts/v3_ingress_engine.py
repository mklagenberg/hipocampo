#!/usr/bin/env python3
"""Processed destination-bound ingress and REM double-check for V3 X4.5."""
from __future__ import annotations

import re
from collections.abc import Callable

from v3_access_runtime import read_eligibility


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
    required_processing_proofs = ("minimized", "anonymized", "redaction_complete", "destination_authorized")
    missing_processing_proofs = [field for field in required_processing_proofs if record.get(field) is not True]
    if missing_processing_proofs:
        raise IngressError(f"processed ingress requires proof of: {', '.join(missing_processing_proofs)}")
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


def read_findings(*, record: dict, verified_read_context: dict | None = None,
                  read_context_checker: Callable[[dict], dict | None] | None = None,
                  host_proof_verifier: Callable[[dict], bool] | None = None,
                  metadata_proof_verifier: Callable[[dict, dict, dict], bool] | None = None) -> dict:
    """READ-only detection; persistence belongs to CREATE/UPDATE."""
    if verified_read_context is not None:
        if read_context_checker is None or host_proof_verifier is None:
            raise IngressError("READ findings requires a fresh authenticated host recheck")
        try:
            current = read_context_checker(dict(verified_read_context))
        except Exception as exc:
            raise IngressError("READ findings host recheck failed") from exc
        if not isinstance(current, dict):
            raise IngressError("READ findings host recheck did not confirm current access")
        proof = current.get("repo_read", {})
        if proof.get("nonce") == verified_read_context.get("proof", {}).get("nonce"):
            raise IngressError("READ findings recheck reused a prior nonce")
        target = verified_read_context.get("target")
        manifest = current.get("vault", {})
        eligibility = read_eligibility(target=target, repo_read=proof, vault=manifest,
            classification=verified_read_context.get("classification"),
            secure_filtering=current.get("secure_filtering") is True,
            host_proof_verifier=host_proof_verifier,
            legacy_registry=current.get("legacy_registry"),
            metadata_proof=current.get("metadata_proof"),
            metadata_proof_verifier=metadata_proof_verifier)
        record_vault_id = record.get("vault", {}).get("vault_id") or record.get("destination_vault_id")
        fresh_context = eligibility.get("context")
        if (not eligibility.get("eligible") or not isinstance(fresh_context, dict)
                or fresh_context.get("target") != verified_read_context.get("target")
                or fresh_context.get("vault_id") != verified_read_context.get("vault_id")
                or fresh_context.get("entity") != verified_read_context.get("entity")
                or fresh_context.get("account_id") != verified_read_context.get("account_id")):
            raise IngressError("READ findings requires a fresh verified target-scoped read context")
        if record_vault_id != verified_read_context.get("vault_id") or record.get("entity") not in (None, verified_read_context.get("entity")):
            raise IngressError("READ findings context does not match the record boundary")
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
