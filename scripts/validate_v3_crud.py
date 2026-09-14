#!/usr/bin/env python3
"""Exercise the V3 Record–Chunk–Collection–Artifact–Package contract."""
from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path

import yaml

from v3_crud_engine import (
    ContractError,
    artifact_update,
    create_package,
    move_record,
    read_chunk,
    split_record,
    validate_entity_operation,
    validate_record,
    validate_record_semantics,
    validate_vault_contract,
)


def expect_block(callback, label: str, errors: list[str]) -> None:
    try:
        callback()
    except ContractError:
        return
    errors.append(f"{label}: expected contract block")


def base_record() -> dict:
    return {
        "record_id": "rec-001", "record_version": 1, "physical_path": "records/example.md",
        "status": "active", "visibility": "internal", "staleness": "current",
        "entity": "entity-a", "scope": "project-alpha",
        "source": {"source_id": "source-session-001", "source_kind": "conversation", "entity": "entity-a"},
        "vault": {"vault_id": "entity-a-anchor", "entity": "entity-a", "profile": "entity", "role": "anchor"},
        "governance": {"owner": "owner-001", "authority": "authority-001"},
        "maturity": "curated",
        "collection_ids": ["col-general"],
        "chunks": [
            {"chunk_id": "chk-001", "parent_record_id": "rec-001", "text_ref": "section-a"},
            {"chunk_id": "chk-002", "parent_record_id": "rec-001", "text_ref": "section-b"},
        ],
        "artifacts": [{"artifact_id": "art-001", "role": "supporting", "version": 1, "reference": "artifact/ref", "visibility": "internal"}],
    }


def entity_record() -> dict:
    record = base_record()
    record.update({
        "entity": "entity-a",
        "scope": "project-alpha",
        "source": {"source_id": "source-session-001", "source_kind": "sensory-capture", "entity": "entity-a"},
        "vault": {"vault_id": "entity-a-anchor", "entity": "entity-a", "profile": "entity", "role": "anchor"},
    })
    return record


def operation_record(operation: str, *, destination_vault: dict | None = None, **overrides: object) -> dict:
    source_vault = {"vault_id": "entity-a-anchor", "entity": "entity-a", "profile": "entity", "role": "anchor"}
    operation_data = {
        "operation": operation,
        "actor": {"actor_id": "actor-001", "roles": ["curator"]},
        "source": {"source_id": "source-session-001", "source_kind": "sensory-capture", "entity": "entity-a"},
        "source_vault": source_vault,
        "destination_vault": destination_vault or source_vault,
        "entity": "entity-a",
        "scope": "project-alpha",
        "authority": {"authority_id": "authority-001", "entity": "entity-a", "scope": "project-alpha"},
        "destination_accepted": True,
    }
    operation_data.update(overrides)
    return operation_data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    fixture = yaml.safe_load((root / "docs/v3-crud-fixtures.yaml").read_text(encoding="utf-8"))
    errors: list[str] = []
    if len(fixture.get("cases", [])) != 23:
        errors.append("expected twenty-three CRUD fixtures")
    active = {"col-general": {"collection_id": "col-general", "active": True}}
    record = base_record()
    try:
        persisted = validate_record(record, active)
        if persisted["record_id"] != "rec-001":
            errors.append("valid Record lost identity")
    except ContractError as exc:
        errors.append(f"valid Record was blocked: {exc}")
    orphan = deepcopy(record)
    orphan["chunks"][0]["parent_record_id"] = "rec-missing"
    expect_block(lambda: validate_record(orphan, active), "orphan chunk", errors)
    weaker = deepcopy(record)
    weaker["chunks"][0]["visibility"] = "public"
    expect_block(lambda: validate_record(weaker, active), "weaker visibility", errors)
    inactive = deepcopy(record)
    inactive["collection_ids"] = ["col-archived"]
    expect_block(lambda: validate_record(inactive, {"col-archived": {"active": False}}), "inactive collection", errors)
    try:
        chunk = read_chunk(record, "chk-001")
        if chunk["parent_context"]["record_id"] != "rec-001":
            errors.append("chunk read omitted parent context")
    except ContractError as exc:
        errors.append(f"chunk read failed: {exc}")
    moved = move_record(record, "records/archive/example.md")
    if moved["record_id"] != record["record_id"] or moved["collection_ids"] != record["collection_ids"]:
        errors.append("physical move changed logical identity or membership")
    try:
        package = create_package(record, ["chk-001"], "internal")
        if not package["partial"] or package["parent_context"]["record_id"] != "rec-001":
            errors.append("partial package lost explicit context")
    except ContractError as exc:
        errors.append(f"partial package failed: {exc}")
    expect_block(lambda: create_package(record, ["chk-001"], "public"), "incompatible destination", errors)
    stale = deepcopy(record)
    stale["staleness"] = "stale"
    expect_block(lambda: create_package(stale, ["chk-001"], "internal"), "stale current-use package", errors)
    artifact_changed = artifact_update(record, "art-001", 2)
    if artifact_changed["record_version"] != record["record_version"] or not artifact_changed["artifacts"][0].get("review_required"):
        errors.append("artifact update did not preserve Record and mark review")
    if artifact_changed["artifacts"][0].get("version") != record["artifacts"][0].get("version"):
        errors.append("artifact update silently rewrote used Artifact version")
    duplicate = deepcopy(record)
    duplicate["chunks"][1]["chunk_id"] = "chk-001"
    expect_block(lambda: validate_record(duplicate, active), "duplicate chunk id", errors)
    tag_only = deepcopy(record)
    tag_only["collection_ids"] = []
    tag_only["tags"] = ["topic-example"]
    expect_block(lambda: validate_record(tag_only, active), "tag replacing collection", errors)
    entity = entity_record()
    try:
        operation = validate_entity_operation(operation_record("update"))
        if operation["transfer_mode"] != "local" or operation["source"]["source_id"] != "source-session-001":
            errors.append("entity-aware operation lost local mode or Source lineage")
    except ContractError as exc:
        errors.append(f"valid entity-aware operation was blocked: {exc}")
    expect_block(
        lambda: validate_entity_operation(operation_record("create", actor={"actor_id": "actor-001", "roles": ["user"]})),
        "user creating governed content",
        errors,
    )
    missing_authority = operation_record("update")
    missing_authority.pop("authority")
    expect_block(lambda: validate_entity_operation(missing_authority), "missing authority resolution", errors)
    expect_block(
        lambda: validate_vault_contract({"vault_id": "team-a", "entity": "entity-a", "profile": "team", "role": "additional"}),
        "team vault without scope",
        errors,
    )
    team_vault = {
        "vault_id": "entity-a-project-alpha",
        "entity": "entity-a",
        "profile": "team",
        "role": "additional",
        "scope_description": "Project Alpha working team",
    }
    try:
        intra = validate_entity_operation(operation_record("send", destination_vault=team_vault))
        if intra["transfer_mode"] != "intra-entity":
            errors.append("intra-entity delivery was not classified correctly")
    except ContractError as exc:
        errors.append(f"valid intra-entity delivery was blocked: {exc}")
    foreign_vault = {
        "vault_id": "entity-b-anchor",
        "entity": "entity-b",
        "profile": "entity",
        "role": "anchor",
    }
    expect_block(
        lambda: validate_entity_operation(operation_record("send", destination_vault=foreign_vault)),
        "inter-entity delivery without approval",
        errors,
    )
    try:
        inter = validate_entity_operation(operation_record(
            "send",
            destination_vault=foreign_vault,
            owner_approved=True,
            minimized=True,
        ))
        if inter["transfer_mode"] != "inter-entity":
            errors.append("inter-entity delivery was not classified correctly")
    except ContractError as exc:
        errors.append(f"valid governed inter-entity delivery was blocked: {exc}")
    try:
        split = split_record(entity, [
            {
                "record_id": "rec-personal-001",
                "entity": "entity-a",
                "scope": "personal-reflection",
                "target_vault": {"vault_id": "entity-a-personal", "entity": "entity-a", "profile": "personal", "role": "additional"},
                "chunk_ids": ["chk-001"],
            },
            {
                "record_id": "rec-team-001",
                "entity": "entity-a",
                "scope": "project-alpha",
                "target_vault": team_vault,
                "chunk_ids": ["chk-002"],
            },
        ])
        if len(split) != 2 or any(item["split_from_record_id"] != entity["record_id"] for item in split):
            errors.append("governed split lost source Record lineage")
        for item in split:
            validate_record(item, active)
    except ContractError as exc:
        errors.append(f"valid personal/project split was blocked: {exc}")
    expect_block(
        lambda: split_record(entity, [{
            "record_id": "rec-shared-001",
            "entity": "entity-a",
            "target_vault": team_vault,
            "chunk_ids": ["chk-001", "chk-002"],
        }, {
            "record_id": "rec-shared-002",
            "entity": "entity-a",
            "target_vault": {"vault_id": "entity-a-personal", "entity": "entity-a", "profile": "personal", "role": "additional"},
            "chunk_ids": ["chk-002"],
        }]),
        "shared mutable Chunk across split outputs",
        errors,
    )
    foreign_split = {
        "record_id": "rec-foreign-001",
        "entity": "entity-b",
        "scope": "shared-project",
        "target_vault": foreign_vault,
        "chunk_ids": ["chk-001"],
    }
    expect_block(
        lambda: split_record(entity, [foreign_split, {
            "record_id": "rec-foreign-002",
            "entity": "entity-a",
            "scope": "project-alpha",
            "target_vault": team_vault,
            "chunk_ids": ["chk-002"],
        }]),
        "cross-entity split without delivery governance",
        errors,
    )
    foreign_split.update({"destination_accepted": True, "owner_approved": True, "minimized": True})
    try:
        split_record(entity, [foreign_split, {
            "record_id": "rec-foreign-003",
            "entity": "entity-a",
            "scope": "project-alpha",
            "target_vault": team_vault,
            "chunk_ids": ["chk-002"],
        }])
    except ContractError as exc:
        errors.append(f"governed cross-entity split was blocked: {exc}")
    try:
        packaged = create_package(entity, ["chk-001"], "internal", entity_operation=operation_record("package", destination_vault=team_vault))
        if packaged["entity_operation"]["transfer_mode"] != "intra-entity":
            errors.append("Package did not retain governed transfer mode")
    except ContractError as exc:
        errors.append(f"valid governed Package failed: {exc}")
    if errors:
        print(f"validate_v3_crud: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_v3_crud: OK — Record identity, Chunk context, monotonic restrictions, Collections, Artifacts, and Packages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
