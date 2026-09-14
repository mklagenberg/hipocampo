#!/usr/bin/env python3
"""Adversarial V3 CRUD use cases exercised through the logical MCP boundary."""
from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path

import yaml

from v3_audit_engine import audit_delivery_graph
from v3_artifact_engine import source_hash
from v3_crud_engine import ContractError, RecordCrud, artifact_update
from v3_ingress_engine import IngressError, process_ingress
from v3_mcp_crud_adapter import McpCrudAdapter, McpCrudError
from v3_migration_engine import evaluate as evaluate_migration
from v3_transfer_engine import TransferError, accept_received


ACTIVE_COLLECTIONS = {"col-general": {"collection_id": "col-general", "active": True}}


def review(record_id: str, *, decision: str = "accepted") -> dict:
    return {
        "review_id": f"sem-{record_id}",
        "target_id": record_id,
        "reviewer": "reviewer-001",
        "purpose": "governed CRUD use-case validation",
        "evidence_refs": [f"meta/audits/{record_id}.yaml"],
        "rationale": "Sanitized fixture with explicit provenance and scope.",
        "reviewed_at": "2026-09-14T12:00:00Z",
        "decision": decision,
    }


def base_record(record_id: str = "rec-001", *, staleness: str = "current", current_use: bool = False) -> dict:
    digest = source_hash("sanitized artifact")
    return {
        "record_id": record_id,
        "record_version": 1,
        "entity": "entity-a",
        "scope": "project-alpha",
        "source": {"source_id": "source-001", "source_kind": "conversation", "entity": "entity-a"},
        "vault": {"vault_id": "vault-a", "entity": "entity-a", "profile": "entity", "role": "anchor"},
        "governance": {"owner": "owner-001", "authority": "authority-001"},
        "physical_path": f"records/{record_id}.md",
        "status": "active",
        "visibility": "internal",
        "staleness": staleness,
        "maturity": "curated",
        "current_use": current_use,
        "collection_ids": ["col-general"],
        "chunks": [{"chunk_id": f"{record_id}-chunk-1", "parent_record_id": record_id, "text_ref": "section-a"}],
        "artifacts": [{
            "artifact_id": "art-001", "role": "evidence", "version": 1,
            "reference": "external://sanitized/artifact", "source_hash": digest, "visibility": "internal",
        }],
    }


def request(record: dict, *, key: str, actor: dict | str = "curator-001", **extra: object) -> dict:
    return {
        "operation": "create",
        "record": record,
        "semantic_review": review(record["record_id"]),
        "actor": actor,
        "reason": "fixture operation",
        "idempotency_key": key,
        **extra,
    }


def expect_error(callback, label: str, errors: list[str], exc_type=Exception) -> None:
    try:
        callback()
    except exc_type:
        return
    errors.append(f"{label}: expected {exc_type.__name__}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    fixture = yaml.safe_load((root / "docs/v3-crud-use-case-fixtures.yaml").read_text(encoding="utf-8"))
    errors: list[str] = []
    cases = fixture.get("cases", [])
    if len(cases) != 18:
        errors.append("expected eighteen CRUD use-case fixtures")

    crud = RecordCrud(ACTIVE_COLLECTIONS)
    mcp = McpCrudAdapter(crud)
    record = base_record()

    created = mcp.call(request(record, key="create-001"))
    if created["status"] != "accepted" or created["transport"] != "mcp" or len(crud.events) != 1:
        errors.append("UC-CRUD-03: valid create did not cross MCP and CRUD exactly once")

    before_read = deepcopy(crud.read("rec-001"))
    read = mcp.call({"operation": "read", "record_id": "rec-001", "actor": {"authorized_vault_ids": ["vault-a"]}})
    if read["record"] != before_read or len(crud.events) != 1:
        errors.append("UC-CRUD-01: authorized read mutated the Record or event stream")
    expect_error(
        lambda: mcp.call({"operation": "read", "record_id": "rec-001", "actor": {"authorized_vault_ids": ["vault-other"]}}),
        "UC-CRUD-02 unauthorized read", errors, McpCrudError,
    )

    invalid = base_record("rec-invalid")
    invalid.pop("governance")
    expect_error(lambda: mcp.call(request(invalid, key="invalid-001")), "UC-CRUD-04 invalid structure", errors, McpCrudError)
    incomplete = request(base_record("rec-semantic"), key="semantic-001")
    incomplete["semantic_review"] = {"review_id": "sem-incomplete"}
    expect_error(lambda: mcp.call(incomplete), "UC-CRUD-05 incomplete semantic review", errors, McpCrudError)

    updated = mcp.call({
        "operation": "update", "record_id": "rec-001", "expected_version": 1,
        "patch": {"scope": "project-alpha-v2"}, "semantic_review": review("rec-001"),
        "actor": "curator-001", "reason": "scope refinement", "idempotency_key": "update-001",
    })
    if updated["record"]["record_version"] != 2 or updated["record"]["scope"] != "project-alpha-v2":
        errors.append("UC-CRUD-06 versioned update failed")
    expect_error(lambda: mcp.call({
        "operation": "update", "record_id": "rec-001", "expected_version": 1,
        "patch": {"scope": "stale-write"}, "semantic_review": review("rec-001"),
        "actor": "curator-001", "reason": "stale", "idempotency_key": "update-stale",
    }), "UC-CRUD-07 concurrent update", errors, McpCrudError)
    expect_error(lambda: mcp.call({
        "operation": "update", "record_id": "rec-001", "expected_version": 2,
        "patch": {"record_id": "rec-other"}, "semantic_review": review("rec-001"),
        "actor": "curator-001", "reason": "identity change", "idempotency_key": "update-identity",
    }), "UC-CRUD-08 immutable identity", errors, McpCrudError)

    proposed = artifact_update(crud.read("rec-001"), "art-001", 2)
    artifact_update_result = mcp.call({
        "operation": "update", "record_id": "rec-001", "expected_version": 2,
        "patch": {"artifacts": proposed["artifacts"]}, "semantic_review": review("rec-001"),
        "actor": "curator-001", "reason": "record Artifact divergence", "idempotency_key": "artifact-001",
    })
    link = artifact_update_result["record"]["artifacts"][0]
    if link["version"] != 1 or not link.get("review_required") or link.get("available_version") != 2:
        errors.append("UC-CRUD-09 Artifact divergence rewrote the used version")

    ingress_input = {
        "record_id": "rec-ingress", "destination_vault_id": "vault-a", "source_ref": "source-002",
        "content": "sanitized guide", "minimized": True, "anonymized": True,
        "redaction_complete": True, "destination_authorized": True,
    }
    ingress = process_ingress(record=ingress_input, destination_vault={"vault_id": "vault-a", "entity": "entity-a"}, operation="create", environment_authorized=True)
    if ingress["status"] != "processed" or ingress["raw_inbox"] is not False:
        errors.append("UC-CRUD-10 processed ingress was not prepared correctly")
    expect_error(lambda: process_ingress(
        record={**ingress_input, "record_id": "rec-raw", "minimized": False},
        destination_vault={"vault_id": "vault-a", "entity": "entity-a"}, operation="create", environment_authorized=True,
    ), "UC-CRUD-11 raw ingress", errors, IngressError)

    current_record = base_record("rec-current", current_use=True)
    current_record.update({"processing_state": "consolidated", "curation_status": "curated"})
    current_received = {"acceptance": "accepted", "local_record": current_record}
    current_crud = RecordCrud(ACTIVE_COLLECTIONS)
    current = accept_received(current_received, rem_status="passed", crud=current_crud, semantic_review=review("rec-current"), actor="curator-001")
    if current["status"] != "current" or not current["current_use"] or "rec-current" not in current_crud.records:
        errors.append("UC-CRUD-12 current-use promotion did not persist through CRUD")
    stale = base_record("rec-stale", staleness="stale", current_use=True)
    expect_error(lambda: RecordCrud(ACTIVE_COLLECTIONS).create(stale, semantic_review=review("rec-stale"), actor="curator-001", reason="stale current"), "UC-CRUD-13 stale current-use", errors, ContractError)

    migration = {"mapping": "complete", "privacy": "proven", "rollback": "defined", "target_contract": "v3", "human_approval": "present", "unsafe_raw_fallback": False, "semantic_review": "complete"}
    if evaluate_migration(migration) != "blocked":
        errors.append("UC-CRUD-14 migration missing versions was not blocked")

    sent = {"delivery_id": "del-1", "package_id": "pkg-1", "package_version": 1, "direction": "sent", "status": "sent", "recorded_at": "2026-09-14T12:00:00Z", "recorded_by": "curator", "fingerprint": "sha256:good", "source_record_id": "rec-a", "source_vault_id": "vault-a", "destination_vault_id": "vault-b", "selected_chunk_ids": [], "artifact_ids": []}
    received = {**sent, "direction": "received", "status": "accepted", "local_record_id": "rec-b"}
    audit_vaults = [
        {"vault_id": "vault-a", "entity": "entity-a", "accessible": True, "records": [{"record_id": "rec-a", "received_via": {}}], "packages_sent": [sent], "packages_received": []},
        {"vault_id": "vault-b", "entity": "entity-b", "accessible": True, "records": [{"record_id": "rec-b", "origin_vault_id": "vault-a", "origin_record_id": "rec-a", "received_via": {"package_id": "pkg-1", "package_version": 1, "fingerprint": "sha256:wrong"}}], "packages_sent": [], "packages_received": [received]},
    ]
    audit = audit_delivery_graph(audit_vaults, start_vault_id="vault-b", start_record_id="rec-b")
    if audit["integrity"] == "valid":
        errors.append("UC-CRUD-15 Record fingerprint mismatch was accepted as valid")

    archived = mcp.call({
        "operation": "delete", "record_id": "rec-001", "expected_version": 3,
        "semantic_review": review("rec-001"), "actor": "owner-001", "reason": "governed archive", "idempotency_key": "archive-001",
    })
    if archived["record"]["status"] != "archived" or archived["record"]["record_version"] != 4:
        errors.append("UC-CRUD-16 archive did not use tombstone-style CRUD update")

    retry_record = base_record("rec-idempotent")
    retry = request(retry_record, key="same-create")
    first = mcp.call(retry)
    second = mcp.call(retry)
    if first != second or len([event for event in crud.events if event["record_id"] == "rec-idempotent"]) != 1:
        errors.append("UC-CRUD-17 MCP retry was not idempotent")
    expect_error(lambda: mcp.call({"operation": "write-file", "path": "records/rec-001.md"}), "UC-CRUD-18 MCP bypass", errors, McpCrudError)

    normalize_source = (root / "scripts/normalize_frontmatter_queue.py").read_text(encoding="utf-8")
    if "\n    path.write_text(" in normalize_source or "write_document(" in normalize_source or "open(" in normalize_source:
        errors.append("UC-CRUD-18 legacy normalizer still writes Record documents outside CRUD")

    if errors:
        print(f"validate_v3_crud_use_cases: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_v3_crud_use_cases: OK — 18 MCP CRUD use cases, semantic gates, version control, audit and bypass blocking")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
