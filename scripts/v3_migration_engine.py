#!/usr/bin/env python3
"""Deterministic preflight evaluation for synthetic V2.x to V3 migration cases."""
from __future__ import annotations

from typing import Any
import hashlib
import json
import re


BLOCKING = {
    "mapping": {"missing", "ambiguous"},
    "privacy": {"unknown", "unproven"},
    "rollback": {"missing"},
    "target_contract": {"missing", "unknown"},
}
VERSION_RE = re.compile(r"^\d+\.\d+(?:\.\d+)?$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
APPROVAL_SCOPE = "v2.2-to-v3-branch-local"


def evaluate(case: dict[str, Any]) -> str:
    # This module is a migration preflight, not an execution or recovery
    # engine. Any already-started/incomplete state requires a dedicated,
    # reviewed recovery path and cannot be declared ready by preflight.
    if case.get("execution_state", "not_started") != "not_started":
        return "blocked"
    if case.get("unsafe_raw_fallback"):
        return "blocked"
    source_version = case.get("source_version")
    target_version = case.get("target_version")
    if not isinstance(source_version, str) or not VERSION_RE.fullmatch(source_version):
        return "blocked"
    if not isinstance(target_version, str) or not VERSION_RE.fullmatch(target_version):
        return "blocked"
    if source_version == target_version:
        return "blocked"
    if any(case.get(field) in values for field, values in BLOCKING.items()):
        return "blocked"
    if case.get("human_approval") != "present":
        return "authorization_required"
    if case.get("semantic_review") == "partial":
        return "partial"
    return "ready"


def inventory_fingerprint(records: list[dict[str, Any]]) -> str:
    entries = sorted(
        ({"source_path": item["source_path"], "source_sha256": item["source_sha256"]} for item in records),
        key=lambda item: item["source_path"],
    )
    canonical = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def validate_execution_manifest(manifest: dict[str, Any]) -> str:
    """Fail closed on incomplete manifest-level migration gates."""
    if not isinstance(manifest, dict):
        return "manifest_invalid"
    if manifest.get("execution_state") != "not_started":
        return "execution_not_started_required"
    if manifest.get("mapping") != "complete":
        return "field_and_semantic_mapping_incomplete"
    if manifest.get("privacy") != "proven":
        return "privacy_review_incomplete"
    if manifest.get("rollback") != "tested":
        return "rollback_not_tested"
    if manifest.get("target_contract") != "verified":
        return "target_contract_unverified"
    if manifest.get("semantic_review_status") != "complete":
        return "semantic_review_incomplete"
    if manifest.get("unsafe_raw_fallback") is not False:
        return "unsafe_raw_fallback_enabled"
    gate = evaluate(manifest)
    if gate != "ready":
        return gate
    if not VERSION_RE.fullmatch(str(manifest.get("source_version", ""))) or not str(manifest["source_version"]).startswith("2."):
        return "source_version_not_v2"
    if not VERSION_RE.fullmatch(str(manifest.get("target_version", ""))) or not str(manifest["target_version"]).startswith("3."):
        return "target_version_not_v3"
    vault_id = manifest.get("vault_id")
    if not vault_id or manifest.get("approved_vault_id") != vault_id:
        return "authorization_scope_mismatch"
    if manifest.get("approval_scope") != APPROVAL_SCOPE or not manifest.get("approval_ref"):
        return "authorization_scope_incomplete"
    if not SHA256_RE.fullmatch(str(manifest.get("source_inventory_sha256", ""))):
        return "source_inventory_fingerprint_missing"
    if not isinstance(manifest.get("active_collections"), dict) or not manifest["active_collections"]:
        return "active_collections_missing"
    if not isinstance(manifest.get("actor"), str) or not manifest["actor"].strip():
        return "migration_actor_missing"
    records = manifest.get("records")
    if not isinstance(records, list) or not records:
        return "record_mapping_missing"
    if any(
        not isinstance(item, dict)
        or not {"mapping_ref", "privacy_review_ref", "semantic_review", "reason"}.issubset(item)
        or not isinstance(item.get("source_path"), str)
        or not SHA256_RE.fullmatch(str(item.get("source_sha256", "")))
        or not isinstance(item.get("record"), dict)
        or not item.get("record", {}).get("record_id")
        or not item.get("idempotency_key")
        or not item.get("mapping_ref")
        or not item.get("privacy_review_ref")
        or not isinstance(item.get("semantic_review"), dict)
        or not item.get("reason")
        for item in records
    ):
        return "record_inventory_incomplete"
    if len({item["source_path"] for item in records}) != len(records):
        return "duplicate_source_path"
    if len({item["record"]["record_id"] for item in records}) != len(records):
        return "duplicate_record_id"
    if len({item["idempotency_key"] for item in records}) != len(records):
        return "duplicate_idempotency_key"
    if inventory_fingerprint(records) != manifest["source_inventory_sha256"]:
        return "source_inventory_fingerprint_mismatch"
    return "ready"


def validate_execution_context(
    manifest: dict[str, Any], *, target_vault_id: str, source_path: str,
    source_sha256: str, record: dict[str, Any], semantic_review: dict[str, Any],
) -> str:
    """Require each gateway mutation to match one entry in the approved manifest."""
    status = validate_execution_manifest(manifest)
    if status != "ready":
        return status
    if target_vault_id != manifest["vault_id"]:
        return "target_vault_mismatch"
    matches = [item for item in manifest["records"] if item["source_path"] == source_path]
    if len(matches) != 1:
        return "record_not_in_approved_manifest"
    item = matches[0]
    if (
        item["source_sha256"] != source_sha256
        or item["record"] != record
        or item.get("semantic_review") != semantic_review
    ):
        return "record_proposal_does_not_match_manifest"
    return "ready"
