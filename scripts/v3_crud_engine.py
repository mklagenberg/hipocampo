#!/usr/bin/env python3
"""In-memory V3 CRUD contract primitives used by the fixture validator."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
from typing import Protocol

import yaml
from v3_migration_engine import validate_execution_context
from v3_queue_engine import DEPRECATED_VALUES


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

RECORD_STATUSES = {"active", "archived", "superseded", "draft", "provisional"}
SEMANTIC_DECISIONS = {"accepted", "provisional", "needs_review", "blocked", "rework_required"}
FULL_RECORD_FIELDS = {
    "record_id", "record_version", "entity", "scope", "source", "vault", "governance",
    "content", "physical_path", "status", "visibility", "staleness", "collection_ids", "chunks", "artifacts",
}


class ContractError(ValueError):
    pass


class RecordPersistence(Protocol):
    def load_all(self, active_collections: dict[str, dict]) -> dict[str, dict]: ...

    def create(self, record: dict) -> None: ...

    def update(self, previous: dict, record: dict) -> None: ...

    def migrate(self, record: dict, source_path: str, expected_source_sha256: str) -> str: ...

    def read_legacy_document(self, relative_path: str) -> tuple[dict, str, str]: ...

    def normalize_legacy_document(
        self, relative_path: str, frontmatter: dict, body: str, expected_source_sha256: str
    ) -> None: ...


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


def validate_record_structure(record: dict, active_collections: dict[str, dict]) -> dict:
    if not isinstance(record, dict):
        raise ContractError("Record must be a mapping")
    missing = FULL_RECORD_FIELDS - record.keys()
    if missing:
        raise ContractError(f"missing Record fields: {sorted(missing)}")
    if not isinstance(record["record_id"], str) or not record["record_id"]:
        raise ContractError("Record identity must be a non-empty string")
    if not isinstance(record["record_version"], int) or record["record_version"] < 1:
        raise ContractError("Record version must be a positive integer")
    if not isinstance(record["entity"], str) or not record["entity"]:
        raise ContractError("Record entity is required")
    if not isinstance(record["scope"], str) or not record["scope"]:
        raise ContractError("Record scope is required")
    if not isinstance(record["content"], str) or not record["content"].strip():
        raise ContractError("Record content must be non-empty prose")
    validate_source(record["source"])
    validate_vault_contract(record["vault"])
    governance = record["governance"]
    if not isinstance(governance, dict) or not governance.get("owner") or not governance.get("authority"):
        raise ContractError("Record governance requires owner and authority")
    if not isinstance(record["physical_path"], str) or not record["physical_path"]:
        raise ContractError("Record physical_path is required")
    record_path = Path(record["physical_path"])
    if record_path.is_absolute() or ".." in record_path.parts:
        raise ContractError("Record physical_path must remain repository-relative")
    if record["status"] not in RECORD_STATUSES:
        raise ContractError(f"unknown Record status: {record['status']}")
    _rank(VISIBILITY_RANK, record["visibility"])
    _rank(STALENESS_RANK, record["staleness"])
    collections = record["collection_ids"]
    if not isinstance(collections, list) or not collections:
        raise ContractError("Record requires at least one Collection")
    if any(collection_id not in active_collections or not active_collections[collection_id].get("active") for collection_id in collections):
        raise ContractError("Record requires active Collection membership")
    seen: set[str] = set()
    for chunk in record["chunks"]:
        if not isinstance(chunk, dict) or not chunk.get("text_ref"):
            raise ContractError("Chunk requires a text_ref")
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


def validate_record(record: dict, active_collections: dict[str, dict]) -> dict:
    """Compatibility name for the deterministic structural validator."""
    return validate_record_structure(record, active_collections)


def validate_semantic_review(review: dict, *, target_id: str, operation: str) -> dict:
    required = {"review_id", "target_id", "reviewer", "purpose", "evidence_refs", "rationale", "reviewed_at", "decision"}
    missing = required - review.keys()
    if missing:
        raise ContractError(f"semantic review is incomplete: {sorted(missing)}")
    if review["target_id"] != target_id or not review["review_id"]:
        raise ContractError("semantic review target does not match Record")
    if review["decision"] not in SEMANTIC_DECISIONS:
        raise ContractError(f"unknown semantic decision: {review['decision']}")
    if not review["reviewer"] or not review["purpose"] or not review["rationale"] or not review["reviewed_at"]:
        raise ContractError("semantic review requires reviewer, purpose, rationale and timestamp")
    if not isinstance(review["evidence_refs"], list) or not review["evidence_refs"]:
        raise ContractError("semantic review requires evidence references")
    if operation == "current-use" and review["decision"] != "accepted":
        raise ContractError("current-use requires an accepted semantic review")
    return deepcopy(review)


def validate_record_semantics(record: dict, review: dict | None, *, operation: str) -> dict:
    if review is None:
        raise ContractError("Record mutation requires a semantic review")
    validated = validate_semantic_review(review, target_id=record["record_id"], operation=operation)
    if operation == "current-use":
        if record.get("staleness") in {"stale", "revalidation_required"}:
            raise ContractError("current-use semantic review cannot override stale Record")
        if record.get("maturity", "curated") != "curated":
            raise ContractError("current-use requires curated maturity")
    return validated


def _event(operation: str, record: dict, *, actor: str, result: str, reason: str) -> dict:
    return {
        "event_type": f"record_{operation}",
        "record_id": record.get("record_id"),
        "record_version": record.get("record_version"),
        "actor": actor,
        "result": result,
        "reason": reason,
    }


class RecordCrud:
    """The only persistence boundary for V3 Record mutations.

    Engines may prepare proposals, but only this gateway commits a Record.
    The gateway intentionally keeps semantic review separate from structural
    validation: semantic review supplies a decision; deterministic validation
    enforces the mutation and versioning rules.
    """

    def __init__(
        self,
        active_collections: dict[str, dict],
        records: dict[str, dict] | None = None,
        *,
        persistence: RecordPersistence | None = None,
    ):
        self.active_collections = deepcopy(active_collections)
        self._persistence = persistence
        if records is None and persistence is not None:
            self._records = persistence.load_all(self.active_collections)
        else:
            self._records = deepcopy(records or {})
        self.events: list[dict] = []
        self._idempotency: dict[str, dict] = {}
        self._migration_fingerprints: dict[str, str] = {}
        for record in self._records.values():
            validate_record_structure(record, self.active_collections)

    @property
    def records(self) -> dict[str, dict]:
        """Read-only snapshot; callers cannot mutate the persistence store."""
        return deepcopy(self._records)

    def _cached(self, idempotency_key: str | None) -> dict | None:
        return deepcopy(self._idempotency[idempotency_key]) if idempotency_key in self._idempotency else None

    def _remember(self, idempotency_key: str | None, result: dict) -> dict:
        if idempotency_key:
            self._idempotency[idempotency_key] = deepcopy(result)
        return deepcopy(result)

    def create(self, record: dict, *, semantic_review: dict, actor: str, reason: str, idempotency_key: str | None = None) -> dict:
        cached = self._cached(idempotency_key)
        if cached:
            return cached
        if not actor or not reason:
            raise ContractError("Record create requires actor and reason")
        structural = validate_record_structure(record, self.active_collections)
        semantic_operation = "current-use" if structural.get("current_use") else "create"
        validate_record_semantics(structural, semantic_review, operation=semantic_operation)
        if structural["record_id"] in self._records:
            raise ContractError("Record already exists")
        if self._persistence is not None:
            self._persistence.create(structural)
        self._records[structural["record_id"]] = structural
        event = _event("created", structural, actor=actor, result="accepted", reason=reason)
        self.events.append(event)
        return self._remember(idempotency_key, {"status": "accepted", "record": structural, "event": event})

    def migrate(
        self,
        record: dict,
        *,
        source_path: str,
        expected_source_sha256: str,
        semantic_review: dict,
        migration_context: dict,
        actor: str,
        reason: str,
        idempotency_key: str,
    ) -> dict:
        """Commit one explicitly mapped V2 document as a V3 Record.

        The migration executor may propose a complete target Record, but only
        this gateway validates it and invokes the configured persistence
        adapter. The adapter must compare the source fingerprint and replace
        the document atomically. This operation is internal and is not exposed
        by the logical MCP CRUD adapter.
        """
        if not actor or not reason or not idempotency_key:
            raise ContractError("Record migration requires actor, reason and idempotency key")
        request_fingerprint = hashlib.sha256(yaml.safe_dump({
            "record": record,
            "source_path": source_path,
            "expected_source_sha256": expected_source_sha256,
            "semantic_review": semantic_review,
            "migration_context": migration_context,
            "actor": actor,
            "reason": reason,
        }, sort_keys=True, allow_unicode=True).encode("utf-8")).hexdigest()
        previous_fingerprint = self._migration_fingerprints.get(idempotency_key)
        if previous_fingerprint and previous_fingerprint != request_fingerprint:
            raise ContractError("migration idempotency key was reused for a different request")
        cached = self._cached(idempotency_key)
        if cached:
            return cached
        if self._persistence is None:
            raise ContractError("Record migration requires canonical persistence")
        if not isinstance(source_path, str) or not source_path or source_path != record.get("physical_path"):
            raise ContractError("migration source path must match the target Record path")
        if not isinstance(expected_source_sha256, str) or len(expected_source_sha256) != 64:
            raise ContractError("migration requires the expected source SHA-256")
        if record.get("record_id") in self._records:
            raise ContractError("Record already exists in the V3 CRUD state")
        context_status = validate_execution_context(
            migration_context,
            target_vault_id=record.get("vault", {}).get("vault_id", ""),
            source_path=source_path,
            source_sha256=expected_source_sha256,
            record=record,
            semantic_review=semantic_review,
        )
        if context_status != "ready":
            raise ContractError(f"Record migration context blocked: {context_status}")
        structural = validate_record_structure(record, self.active_collections)
        semantic_operation = "current-use" if structural.get("current_use") else "migration"
        validate_record_semantics(structural, semantic_review, operation=semantic_operation)
        if semantic_review.get("decision") != "accepted":
            raise ContractError("Record migration requires an accepted semantic review")

        persistence_status = self._persistence.migrate(
            structural, source_path, expected_source_sha256
        )
        if persistence_status != "written":
            raise ContractError("canonical migration persistence returned an invalid status")
        self._records[structural["record_id"]] = structural
        self._migration_fingerprints[idempotency_key] = request_fingerprint
        event = _event("migrated", structural, actor=actor, result=persistence_status, reason=reason)
        self.events.append(event)
        return self._remember(idempotency_key, {
            "status": "accepted",
            "record": structural,
            "event": event,
        })

    def _read_record(self, record_id: str) -> dict:
        if record_id not in self._records:
            raise ContractError("Record not found")
        return deepcopy(self._records[record_id])

    def read(self, record_id: str, *, authorized_vault_ids: list[str] | None = None) -> dict:
        """Read a Record only with an explicit, bounded authorization context."""
        if (
            not isinstance(authorized_vault_ids, list)
            or not authorized_vault_ids
            or any(not isinstance(item, str) or not item.strip() for item in authorized_vault_ids)
        ):
            raise ContractError("Record read requires a non-empty authorized_vault_ids context")
        record = self._read_record(record_id)
        vault_id = record.get("vault", {}).get("vault_id")
        if vault_id not in authorized_vault_ids:
            raise ContractError("actor is not authorized for Record vault")
        return record

    def update(self, record_id: str, patch: dict, *, expected_version: int, semantic_review: dict,
               actor: str, reason: str, operation: str = "update", idempotency_key: str | None = None) -> dict:
        cached = self._cached(idempotency_key)
        if cached:
            return cached
        if not actor or not reason:
            raise ContractError("Record update requires actor and reason")
        current = self._read_record(record_id)
        if expected_version != current["record_version"]:
            raise ContractError("stale Record version; reread before update")
        if patch.get("record_id", record_id) != record_id:
            raise ContractError("Record identity is immutable")
        merged = deepcopy(current)
        for key, value in patch.items():
            if key == "record_version":
                raise ContractError("Record version is controlled by CRUD")
            merged[key] = deepcopy(value)
        merged["record_version"] = current["record_version"] + 1
        structural = validate_record_structure(merged, self.active_collections)
        validate_record_semantics(structural, semantic_review, operation=operation)
        if self._persistence is not None:
            self._persistence.update(current, structural)
        self._records[record_id] = structural
        event = _event("updated", structural, actor=actor, result="accepted", reason=reason)
        event["previous_record_version"] = current["record_version"]
        self.events.append(event)
        return self._remember(idempotency_key, {"status": "accepted", "record": structural, "event": event})

    def normalize_legacy_frontmatter(
        self,
        relative_path: str,
        proposed_frontmatter: dict,
        body: str,
        *,
        expected_revision: int,
        actor: str,
        reason: str,
    ) -> None:
        """Apply the narrow deterministic legacy vocabulary correction through CRUD."""
        if self._persistence is None or not actor or not reason:
            raise ContractError("legacy normalization requires canonical persistence, actor and reason")
        if not isinstance(proposed_frontmatter, dict) or not isinstance(body, str):
            raise ContractError("legacy normalization proposal is invalid")
        current, current_body, source_sha256 = self._persistence.read_legacy_document(relative_path)
        if current.get("revision") != expected_revision:
            raise ContractError("stale document revision; reread before normalization")
        if current_body != body:
            raise ContractError("legacy normalization cannot change Record prose")
        if {"record_id", "record_version"}.issubset(current):
            raise ContractError("V3 Records must use canonical RecordCrud.update")
        old_source = current.get("source")
        if not old_source or DEPRECATED_VALUES.get(old_source) != proposed_frontmatter.get("source"):
            raise ContractError("legacy normalization is not a supported deterministic value mapping")
        old_without_allowed = {key: value for key, value in current.items() if key not in {"source", "revision", "revision_note"}}
        new_without_allowed = {key: value for key, value in proposed_frontmatter.items() if key not in {"source", "revision", "revision_note"}}
        if old_without_allowed != new_without_allowed:
            raise ContractError("legacy normalization changed fields outside its deterministic mapping")
        if proposed_frontmatter.get("revision") != expected_revision + 1 or not proposed_frontmatter.get("revision_note"):
            raise ContractError("legacy normalization must increment revision and explain the change")
        self._persistence.normalize_legacy_document(
            relative_path, proposed_frontmatter, body, source_sha256
        )
        self.events.append({
            "event_type": "record_legacy_normalized",
            "physical_path": relative_path,
            "actor": actor,
            "result": "accepted",
            "reason": reason,
            "previous_revision": expected_revision,
            "record_revision": expected_revision + 1,
        })

    def archive(self, record_id: str, *, expected_version: int, semantic_review: dict, actor: str,
                reason: str, idempotency_key: str | None = None) -> dict:
        return self.update(
            record_id, {"status": "archived", "current_use": False},
            expected_version=expected_version, semantic_review=semantic_review, actor=actor,
            reason=reason, operation="delete", idempotency_key=idempotency_key,
        )

    def apply(self, request: dict) -> dict:
        """Apply a logical MCP CRUD request; no other operation is accepted."""
        operation = request.get("operation")
        if operation == "read":
            actor = request.get("actor") or {}
            if not isinstance(actor, dict):
                raise ContractError("Record read requires an authorization context")
            return {
                "status": "accepted",
                "record": self.read(
                    request.get("record_id", ""),
                    authorized_vault_ids=actor.get("authorized_vault_ids"),
                ),
            }
        common = {
            "semantic_review": request.get("semantic_review"),
            "actor": request.get("actor", ""),
            "reason": request.get("reason", ""),
            "idempotency_key": request.get("idempotency_key"),
        }
        if operation == "create":
            return self.create(request.get("record", {}), **common)
        if operation == "update":
            return self.update(request.get("record_id", ""), request.get("patch", {}), expected_version=request.get("expected_version"), **common)
        if operation == "delete":
            return self.archive(request.get("record_id", ""), expected_version=request.get("expected_version"), **common)
        raise ContractError("MCP request must use the canonical CRUD operations")


def _parse_document_for_crud(text: str) -> tuple[dict, str]:
    if text.startswith("---\r\n"):
        frontmatter_start = 5
    elif text.startswith("---\n"):
        frontmatter_start = 4
    else:
        return {}, text
    delimiter_start = -1
    delimiter_length = 0
    for delimiter in ("\r\n---\r\n", "\n---\n", "\r\n---", "\n---"):
        candidate = text.find(delimiter, frontmatter_start)
        if candidate >= 0 and (delimiter_start < 0 or candidate < delimiter_start):
            delimiter_start = candidate
            delimiter_length = len(delimiter)
    if delimiter_start < 0:
        return {}, text
    delimiter = text[delimiter_start:delimiter_start + delimiter_length]
    body_start = delimiter_start + len(delimiter.rstrip("\r\n"))
    frontmatter = yaml.safe_load(text[frontmatter_start:delimiter_start]) or {}
    return frontmatter, text[body_start:]


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
    """Return a governed divergence proposal; never rewrite the Record link."""
    updated = deepcopy(record)
    for artifact in updated["artifacts"]:
        if artifact.get("artifact_id") == artifact_id:
            if not isinstance(new_version, int) or new_version <= artifact.get("version", 0):
                raise ContractError("Artifact versions must increase monotonically")
            artifact["review_required"] = True
            artifact["available_version"] = new_version
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
