#!/usr/bin/env python3
"""In-memory V3 CRUD contract primitives used by the fixture validator."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json


VISIBILITY_RANK = {"public": 0, "internal": 1, "confidential": 2, "restricted": 3}
STALENESS_RANK = {"current": 0, "revalidation_required": 1, "stale": 2, "historical_exempt": 0}
VAULT_PROFILES = {"entity", "team", "personal"}
VAULT_ROLES = {"anchor", "additional"}
GOVERNANCE_ROLES = {"owner", "authority", "curator", "user"}
OPERATION_ROLES = {
    "read": {"owner", "authority", "curator", "user"},
    "create": {"owner", "curator"},
    "update": {"owner", "curator"},
    "split": {"owner", "curator"},
    "package": {"owner", "curator"},
    "send": {"owner", "curator"},
    "authorize": {"owner", "authority"},
}


class ContractError(ValueError):
    pass


def _rank(mapping: dict[str, int], value: str) -> int:
    if value not in mapping:
        raise ContractError(f"unknown controlled value: {value}")
    return mapping[value]


def validate_vault_contract(vault: dict) -> dict:
    required = {"vault_id", "entity", "profile", "role"}
    missing = required - vault.keys()
    if missing:
        raise ContractError(f"missing vault contract fields: {sorted(missing)}")
    if not vault["vault_id"] or not vault["entity"]:
        raise ContractError("vault_id and entity must be non-empty")
    if vault["profile"] not in VAULT_PROFILES:
        raise ContractError(f"unknown vault profile: {vault['profile']}")
    if vault["role"] not in VAULT_ROLES:
        raise ContractError(f"unknown vault role: {vault['role']}")
    if vault["profile"] == "team" and not vault.get("scope_description"):
        raise ContractError("team vault requires scope_description")
    return deepcopy(vault)


def validate_actor(actor: dict, operation: str) -> dict:
    if operation not in OPERATION_ROLES:
        raise ContractError(f"unknown entity-aware operation: {operation}")
    roles = actor.get("roles", [])
    if isinstance(roles, str):
        roles = [roles]
    if not roles or any(role not in GOVERNANCE_ROLES for role in roles):
        raise ContractError("actor must declare valid governance roles")
    if not OPERATION_ROLES[operation].intersection(roles):
        raise ContractError(f"actor role cannot perform {operation}")
    return {"actor_id": actor.get("actor_id", ""), "roles": list(roles)}


def validate_source(source: dict) -> dict:
    if not source.get("source_id") or not source.get("source_kind"):
        raise ContractError("Source requires source_id and source_kind")
    return deepcopy(source)


def validate_authority(authority: dict, entity: str, scope: str) -> dict:
    required = {"authority_id", "entity", "scope"}
    missing = required - authority.keys()
    if missing:
        raise ContractError(f"authority resolution is missing: {sorted(missing)}")
    if authority["entity"] != entity or authority["scope"] != scope:
        raise ContractError("authority resolution does not match entity and scope")
    return deepcopy(authority)


def validate_entity_operation(operation: dict) -> dict:
    required = {"operation", "actor", "source", "source_vault", "destination_vault"}
    missing = required - operation.keys()
    if missing:
        raise ContractError(f"missing entity-aware operation fields: {sorted(missing)}")
    operation_name = operation["operation"]
    actor = validate_actor(operation["actor"], operation_name)
    source = validate_source(operation["source"])
    source_vault = validate_vault_contract(operation["source_vault"])
    destination_vault = validate_vault_contract(operation["destination_vault"])
    if source.get("entity") and source["entity"] != source_vault["entity"]:
        raise ContractError("Source entity does not match source vault entity")
    if operation.get("entity") and operation["entity"] != source_vault["entity"]:
        raise ContractError("operation entity does not match source vault entity")
    if operation_name != "read" and not operation.get("scope"):
        raise ContractError("non-read entity-aware operations require scope")
    authority = None
    if operation_name != "read":
        authority = validate_authority(operation.get("authority", {}), source_vault["entity"], operation["scope"])
    transfer_mode = "local" if source_vault["vault_id"] == destination_vault["vault_id"] else (
        "intra-entity" if source_vault["entity"] == destination_vault["entity"] else "inter-entity"
    )
    if operation.get("transfer_mode") and operation["transfer_mode"] != transfer_mode:
        raise ContractError("declared transfer mode does not match vault entities")
    if operation_name in {"package", "send"}:
        if not operation.get("destination_accepted"):
            raise ContractError("destination acceptance is required for delivery")
        if transfer_mode == "inter-entity":
            if not operation.get("owner_approved"):
                raise ContractError("inter-entity delivery requires Owner approval")
            if not operation.get("minimized"):
                raise ContractError("inter-entity delivery requires minimization")
    return {
        "operation": operation_name,
        "actor": actor,
        "source": source,
        "source_vault": source_vault,
        "destination_vault": destination_vault,
        "transfer_mode": transfer_mode,
        "scope": operation.get("scope", ""),
        "authority": authority,
    }


def split_record(record: dict, split_specs: list[dict]) -> list[dict]:
    if not record.get("entity") or not record.get("scope"):
        raise ContractError("split requires source Record entity and scope")
    source = validate_source(record.get("source", {}))
    source_vault = validate_vault_contract(record["vault"]) if record.get("vault") else None
    available = {chunk["chunk_id"] for chunk in record.get("chunks", [])}
    used: set[str] = set()
    result: list[dict] = []
    for spec in split_specs:
        target_vault = validate_vault_contract(spec.get("target_vault", {}))
        if target_vault["entity"] != spec.get("entity"):
            raise ContractError("split target vault entity does not match split entity")
        if target_vault["entity"] != record["entity"]:
            if source_vault is None:
                raise ContractError("cross-entity split requires a governed source vault")
            if not spec.get("destination_accepted"):
                raise ContractError("cross-entity split requires destination acceptance")
            if not spec.get("owner_approved"):
                raise ContractError("cross-entity split requires Owner approval")
            if not spec.get("minimized"):
                raise ContractError("cross-entity split requires minimization")
        chunk_ids = spec.get("chunk_ids", [])
        if not chunk_ids or not set(chunk_ids).issubset(available):
            raise ContractError("split references an unknown or empty Chunk selection")
        if used.intersection(chunk_ids):
            raise ContractError("a mutable Chunk cannot be shared by split outputs")
        used.update(chunk_ids)
        new_id = spec.get("record_id")
        if not new_id:
            raise ContractError("split requires a new Record id")
        selected = []
        for chunk in record["chunks"]:
            if chunk["chunk_id"] not in chunk_ids:
                continue
            copied = deepcopy(chunk)
            copied["chunk_id"] = f"{new_id}--{chunk['chunk_id']}"
            copied["parent_record_id"] = new_id
            copied["source_record_id"] = record["record_id"]
            copied["source_chunk_id"] = chunk["chunk_id"]
            copied["entity"] = spec["entity"]
            copied["scope"] = spec.get("scope", record["scope"])
            selected.append(copied)
        derived = deepcopy(record)
        derived["record_id"] = new_id
        derived["record_version"] = 1
        derived["entity"] = spec["entity"]
        derived["scope"] = spec.get("scope", record["scope"])
        derived["vault"] = target_vault
        derived["source"] = source
        derived["split_from_record_id"] = record["record_id"]
        derived["chunks"] = selected
        result.append(derived)
    if not result or used != available:
        raise ContractError("split must explicitly account for every source Chunk")
    return result


def effective_visibility(items: list[dict]) -> str:
    return max((item.get("visibility", "public") for item in items), key=lambda value: _rank(VISIBILITY_RANK, value))


def effective_staleness(items: list[dict]) -> str:
    return max((item.get("staleness", "current") for item in items), key=lambda value: _rank(STALENESS_RANK, value))


def validate_record(record: dict, active_collections: dict[str, dict]) -> dict:
    required = {"record_id", "record_version", "physical_path", "status", "visibility", "staleness", "collection_ids", "chunks", "artifacts"}
    missing = required - record.keys()
    if missing:
        raise ContractError(f"missing Record fields: {sorted(missing)}")
    _rank(VISIBILITY_RANK, record["visibility"])
    _rank(STALENESS_RANK, record["staleness"])
    collections = record["collection_ids"]
    if not isinstance(collections, list) or not collections:
        raise ContractError("Record requires at least one Collection")
    if any(collection_id not in active_collections or not active_collections[collection_id].get("active") for collection_id in collections):
        raise ContractError("Record requires active Collection membership")
    seen: set[str] = set()
    for chunk in record["chunks"]:
        chunk_id = chunk.get("chunk_id")
        if not chunk_id or chunk_id in seen:
            raise ContractError("Chunk IDs must be unique and non-empty")
        seen.add(chunk_id)
        if chunk.get("parent_record_id") != record["record_id"]:
            raise ContractError("Chunk parent_record_id does not match Record")
        if _rank(VISIBILITY_RANK, chunk.get("visibility", record["visibility"])) < _rank(VISIBILITY_RANK, record["visibility"]):
            raise ContractError("Chunk visibility weakens Record visibility")
        if _rank(STALENESS_RANK, chunk.get("staleness", record["staleness"])) < _rank(STALENESS_RANK, record["staleness"]):
            raise ContractError("Chunk staleness weakens Record staleness")
    for artifact in record["artifacts"]:
        if not artifact.get("artifact_id") or not artifact.get("reference"):
            raise ContractError("Artifact requires artifact_id and reference")
        _rank(VISIBILITY_RANK, artifact.get("visibility", record["visibility"]))
    return deepcopy(record)


def read_chunk(record: dict, chunk_id: str) -> dict:
    for chunk in record["chunks"]:
        if chunk.get("chunk_id") == chunk_id:
            result = deepcopy(chunk)
            result["parent_context"] = {
                "record_id": record["record_id"],
                "record_version": record["record_version"],
                "physical_path": record["physical_path"],
                "collection_ids": deepcopy(record["collection_ids"]),
            }
            result["effective_visibility"] = effective_visibility([record, chunk])
            result["effective_staleness"] = effective_staleness([record, chunk])
            return result
    raise ContractError("Chunk not found")


def move_record(record: dict, new_path: str) -> dict:
    moved = deepcopy(record)
    moved["physical_path"] = new_path
    return moved


def artifact_update(record: dict, artifact_id: str, new_version: int) -> dict:
    updated = deepcopy(record)
    for artifact in updated["artifacts"]:
        if artifact.get("artifact_id") == artifact_id:
            artifact["version"] = new_version
            return updated
    raise ContractError("Artifact not found")


def package_fingerprint(
    record: dict,
    chunk_ids: list[str],
    artifact_ids: list[str],
    destination_visibility: str,
    *,
    current_use: bool,
    entity_operation: dict | None = None,
) -> str:
    material = {
        "source_record_id": record["record_id"],
        "record_version": record["record_version"],
        "chunk_ids": list(chunk_ids),
        "artifact_ids": list(artifact_ids),
        "destination_visibility": destination_visibility,
        "current_use": current_use,
        "entity_operation": entity_operation or {},
    }
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def create_package(
    record: dict,
    chunk_ids: list[str],
    destination_visibility: str,
    *,
    current_use: bool = True,
    entity_operation: dict | None = None,
    artifact_ids: list[str] | None = None,
) -> dict:
    _rank(VISIBILITY_RANK, destination_visibility)
    selected = [read_chunk(record, chunk_id) for chunk_id in chunk_ids]
    available_artifacts = {artifact["artifact_id"]: artifact for artifact in record.get("artifacts", [])}
    selected_artifact_ids = list(available_artifacts) if artifact_ids is None else list(artifact_ids)
    if len(set(selected_artifact_ids)) != len(selected_artifact_ids) or any(
        artifact_id not in available_artifacts for artifact_id in selected_artifact_ids
    ):
        raise ContractError("Package references an unknown or duplicated Artifact")
    selected_artifacts = [available_artifacts[artifact_id] for artifact_id in selected_artifact_ids]
    items = [record, *selected, *selected_artifacts]
    visibility = effective_visibility(items)
    if _rank(VISIBILITY_RANK, destination_visibility) < _rank(VISIBILITY_RANK, visibility):
        raise ContractError("destination visibility is weaker than package content")
    staleness = effective_staleness(items)
    if current_use and staleness in {"stale", "revalidation_required"}:
        raise ContractError("current-use package requires staleness revalidation")
    fingerprint = package_fingerprint(
        record,
        chunk_ids,
        selected_artifact_ids,
        destination_visibility,
        current_use=current_use,
        entity_operation=entity_operation,
    )
    package = {
        "package_id": f"pkg-{record['record_id']}-v{record['record_version']}-{fingerprint[7:19]}",
        "package_version": 1,
        "source_record_id": record["record_id"],
        "source_record_version": record["record_version"],
        "selected_chunk_ids": list(chunk_ids),
        "selected_chunks": deepcopy(selected),
        "partial": set(chunk_ids) != {chunk["chunk_id"] for chunk in record["chunks"]},
        "parent_context": {"record_id": record["record_id"], "record_version": record["record_version"]},
        "effective_visibility": visibility,
        "effective_staleness": staleness,
        "artifact_ids": selected_artifact_ids,
        "selected_artifacts": deepcopy(selected_artifacts),
        "fingerprint": fingerprint,
        "assembly_entity_operation": deepcopy(entity_operation) if entity_operation is not None else None,
    }
    if entity_operation is not None:
        package["entity_operation"] = validate_entity_operation(entity_operation)
    return package
