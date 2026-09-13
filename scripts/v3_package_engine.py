#!/usr/bin/env python3
"""In-memory V3 Package, logical authority and bilateral-ledger primitives."""
from __future__ import annotations

from copy import deepcopy
import hashlib

from v3_crud_engine import ContractError, create_package, package_fingerprint, validate_vault_contract


CONCILIATION_STATES = {
    "equivalent",
    "complementary",
    "update",
    "entity_specific",
    "unresolved_conflict",
    "irreconcilable_perspectives",
}
PACKAGE_PURPOSES = {"discussion", "review", "analysis", "current_use"}
LEDGER_DIRECTIONS = {"sent", "received"}
RECEIPT_STATES = {"received", "accepted", "rejected"}


def _delivery_id(package_id: str, package_version: int, origin_vault_id: str, destination_vault_id: str) -> str:
    material = f"{package_id}|{package_version}|{origin_vault_id}|{destination_vault_id}".encode("utf-8")
    return f"del-{hashlib.sha256(material).hexdigest()[:16]}"


def resolve_authority(
    entity: str,
    scope: str,
    chain: list[dict],
    accessible_authority_ids: set[str] | None = None,
) -> dict:
    """Resolve a logical authority without persisting active/inactive flags."""
    if not entity or not scope or not chain:
        raise ContractError("authority resolution requires entity, scope and a non-empty chain")
    seen: set[str] = set()
    eligible: list[dict] = []
    for position, candidate in enumerate(chain, start=1):
        if "active" in candidate or "inactive" in candidate or "accessible" in candidate:
            raise ContractError("authority chain must not persist active/inactive/access state")
        authority_id = candidate.get("authority_id")
        if not authority_id or authority_id in seen:
            raise ContractError("authority chain IDs must be unique and non-empty")
        if candidate.get("entity") != entity or candidate.get("scope") != scope:
            raise ContractError("authority chain candidate does not match entity and scope")
        seen.add(authority_id)
        status = candidate.get("status", "eligible")
        if status not in {"eligible", "revoked"}:
            raise ContractError(f"unknown logical authority status: {status}")
        item = {
            "authority_id": authority_id,
            "entity": entity,
            "scope": scope,
            "position": position,
            "status": status,
            "authorized": bool(candidate.get("authorized", True)),
        }
        if item["status"] == "eligible" and item["authorized"]:
            eligible.append(item)

    if not eligible:
        return {
            "status": "revoked",
            "entity": entity,
            "scope": scope,
            "selected_authority_id": None,
            "chain": deepcopy(chain),
            "resolution_basis": "no-authorized-candidate",
        }

    accessible = {item["authority_id"] for item in eligible} if accessible_authority_ids is None else accessible_authority_ids
    selected = next((item for item in eligible if item["authority_id"] in accessible), None)
    if selected is None:
        return {
            "status": "unavailable",
            "entity": entity,
            "scope": scope,
            "selected_authority_id": eligible[0]["authority_id"],
            "succession_position": eligible[0]["position"],
            "chain": deepcopy(eligible),
            "resolution_basis": "ordered-chain-frontier",
        }
    return {
        "status": "resolved",
        "entity": entity,
        "scope": scope,
        "selected_authority_id": selected["authority_id"],
        "succession_position": selected["position"],
        "chain": deepcopy(eligible),
        "resolution_basis": "ordered-chain-access-context",
    }


def classify_conciliation(state: str, sources: list[dict], *, authoritative_source_id: str | None = None) -> dict:
    if state not in CONCILIATION_STATES:
        raise ContractError(f"unknown conciliation state: {state}")
    if not sources:
        raise ContractError("conciliation requires at least one source")
    required = {"source_id", "entity", "vault_id", "scope", "provenance", "epistemic_nature", "version", "staleness"}
    source_ids: list[str] = []
    normalized_sources: list[dict] = []
    for source in sources:
        missing = required - source.keys()
        if missing:
            raise ContractError(f"conciliation source is missing context: {sorted(missing)}")
        source_id = source.get("source_id")
        if not source_id or source_id in source_ids:
            raise ContractError("conciliation sources require unique non-empty source IDs")
        source_ids.append(source_id)
        normalized_sources.append(deepcopy(source))
    if authoritative_source_id and authoritative_source_id not in source_ids:
        raise ContractError("authoritative source must be part of the conciliation set")
    return {
        "state": state,
        "source_ids": source_ids,
        "sources": normalized_sources,
        "authoritative_source_id": authoritative_source_id,
    }


def _validate_package_authority(package_authority: dict) -> dict:
    vault = validate_vault_contract(package_authority.get("vault", {}))
    generator_vault_id = package_authority.get("generator_vault_id")
    if not generator_vault_id or generator_vault_id != vault["vault_id"]:
        raise ContractError("Package authority must identify the vault that generates the Package")
    if not package_authority.get("generator_id"):
        raise ContractError("Package authority requires generator_id")
    return {
        "generator_id": package_authority["generator_id"],
        "generator_vault_id": generator_vault_id,
        "vault": vault,
    }


def _authority_snapshot(resolution: dict) -> dict:
    return {
        "status": resolution.get("status"),
        "entity": resolution.get("entity"),
        "scope": resolution.get("scope"),
        "selected_authority_id": resolution.get("selected_authority_id"),
        "succession_position": resolution.get("succession_position"),
        "resolution_basis": resolution.get("resolution_basis"),
        "chain": deepcopy(resolution.get("chain", [])),
    }


def build_ledger_entry(
    package: dict,
    *,
    direction: str,
    status: str,
    recorded_at: str,
    recorded_by: str,
    local_record_id: str | None = None,
) -> dict:
    if direction not in LEDGER_DIRECTIONS:
        raise ContractError(f"unknown ledger direction: {direction}")
    if not recorded_at or not recorded_by:
        raise ContractError("ledger entry requires recorded_at and recorded_by")
    delivery = package.get("delivery", {})
    destination = delivery.get("destination_vault", {})
    origin = package.get("origin", {})
    entry = {
        "delivery_id": delivery.get("delivery_id"),
        "package_id": package.get("package_id"),
        "package_version": package.get("package_version"),
        "direction": direction,
        "status": status,
        "recorded_at": recorded_at,
        "recorded_by": recorded_by,
        "fingerprint": package.get("fingerprint"),
        "source_record_id": package.get("source_record_id"),
        "source_record_version": package.get("source_record_version"),
        "source_entity": origin.get("entity"),
        "source_vault_id": origin.get("vault_id"),
        "source_authority_id": package.get("authority_snapshot", {}).get("selected_authority_id"),
        "destination_entity": destination.get("entity"),
        "destination_vault_id": destination.get("vault_id"),
        "purpose": delivery.get("purpose"),
        "selected_chunk_ids": list(package.get("selected_chunk_ids", [])),
        "artifact_ids": list(package.get("artifact_ids", [])),
        "governance": delivery.get("governance", "accepted"),
    }
    if local_record_id:
        entry["local_record_id"] = local_record_id
    return entry


def create_delivery_package(
    record: dict,
    chunk_ids: list[str],
    destination_visibility: str,
    *,
    authority_resolution: dict,
    conciliation: dict,
    package_authority: dict,
    destination_vault: dict,
    purpose: str,
    current_use: bool = False,
    destination_accepts_multiple_perspectives: bool = False,
    entity_operation: dict | None = None,
    ledger_direction: str = "sent",
    artifact_ids: list[str] | None = None,
    recorded_at: str | None = None,
) -> dict:
    if purpose not in PACKAGE_PURPOSES:
        raise ContractError(f"unknown Package purpose: {purpose}")
    if (purpose == "current_use") != current_use:
        raise ContractError("Package purpose and current_use must agree")
    if ledger_direction not in LEDGER_DIRECTIONS:
        raise ContractError(f"unknown ledger direction: {ledger_direction}")
    if authority_resolution.get("status") != "resolved" or not authority_resolution.get("selected_authority_id"):
        raise ContractError("Package assembly requires resolved source authority")
    if authority_resolution.get("entity") != record.get("entity") or authority_resolution.get("scope") != record.get("scope"):
        raise ContractError("authority resolution does not match source Record")
    normalized_conciliation = classify_conciliation(
        conciliation.get("state", ""),
        conciliation.get("sources", []),
        authoritative_source_id=conciliation.get("authoritative_source_id"),
    )
    conflict = normalized_conciliation["state"] in {"unresolved_conflict", "irreconcilable_perspectives"}
    if current_use and normalized_conciliation["state"] == "unresolved_conflict":
        raise ContractError("current-use Package is blocked by unresolved conflict")
    if current_use and normalized_conciliation["state"] == "irreconcilable_perspectives" and not destination_accepts_multiple_perspectives:
        raise ContractError("current-use Package requires explicit destination acceptance of multiple perspectives")
    if current_use and record.get("maturity", "curated") != "curated":
        raise ContractError("current-use Package requires curated maturity")
    destination = validate_vault_contract(destination_vault)
    package_auth = _validate_package_authority(package_authority)
    package = create_package(
        record,
        chunk_ids,
        destination_visibility,
        current_use=current_use,
        entity_operation=entity_operation,
        artifact_ids=artifact_ids,
    )
    package["origin"] = {
        "entity": record.get("entity"),
        "vault_id": record.get("vault", {}).get("vault_id"),
        "record_id": record.get("record_id"),
        "record_version": record.get("record_version"),
        "scope": record.get("scope"),
        "source": deepcopy(record.get("source", {})),
    }
    package["authority_snapshot"] = _authority_snapshot(authority_resolution)
    delivery_id = _delivery_id(package["package_id"], package["package_version"], package["origin"]["vault_id"], destination["vault_id"])
    package["delivery"] = {
        "delivery_id": delivery_id,
        "purpose": purpose,
        "authority_resolution": deepcopy(authority_resolution),
        "conciliation": normalized_conciliation,
        "destination_accepts_multiple_perspectives": destination_accepts_multiple_perspectives,
        "destination_vault": destination,
        "package_authority": package_auth,
        "conflict_bearing": conflict,
        "ledger_direction": ledger_direction,
        "governance": "accepted" if purpose != "discussion" else "review_only",
        "recorded_at": recorded_at,
        "recorded_by": package_auth["generator_id"],
    }
    package["ledger_entry"] = build_ledger_entry(
        package,
        direction=ledger_direction,
        status="sent" if ledger_direction == "sent" else "received",
        recorded_at=recorded_at or "",
        recorded_by=package_auth["generator_id"],
    )
    return package


def receive_package(
    package: dict,
    destination_vault: dict,
    *,
    local_record_id: str,
    acceptance: str = "received",
    received_at: str | None = None,
    received_by: str | None = None,
) -> dict:
    if acceptance not in RECEIPT_STATES:
        raise ContractError(f"unknown Package receipt state: {acceptance}")
    destination = validate_vault_contract(destination_vault)
    declared = package.get("delivery", {}).get("destination_vault", {})
    if declared.get("vault_id") != destination["vault_id"] or declared.get("entity") != destination["entity"]:
        raise ContractError("received Package destination does not match local vault")
    local_record = {
        "record_id": local_record_id,
        "record_version": 1,
        "physical_path": f"records/received/{local_record_id}.md",
        "status": "active" if acceptance != "rejected" else "archived",
        "visibility": package.get("effective_visibility", "internal"),
        "staleness": package.get("effective_staleness", "current"),
        "maturity": "new",
        "processing_state": "new",
        "curation_status": "pending_rem",
        "entity": destination["entity"],
        "scope": package.get("origin", {}).get("scope", "received-package"),
        "source": deepcopy(package.get("origin", {}).get("source", {})),
        "vault": destination,
        "origin_record_id": package.get("source_record_id"),
        "origin_vault_id": package.get("origin", {}).get("vault_id"),
        "received_via": {
            "delivery_id": package.get("delivery", {}).get("delivery_id"),
            "package_id": package.get("package_id"),
            "package_version": package.get("package_version"),
            "fingerprint": package.get("fingerprint"),
        },
        "chunks": deepcopy(package.get("selected_chunks", [])),
        "artifacts": deepcopy(package.get("selected_artifacts", [])),
    }
    for chunk in local_record["chunks"]:
        source_chunk_id = chunk.get("chunk_id")
        chunk["chunk_id"] = f"{local_record_id}--{source_chunk_id}"
        chunk["source_chunk_id"] = source_chunk_id
        chunk["parent_record_id"] = local_record_id
        chunk["source_record_id"] = package.get("source_record_id")
    return {
        "package_id": package.get("package_id"),
        "acceptance": acceptance,
        "local_record": local_record,
        "ledger_entry": build_ledger_entry(
            package,
            direction="received",
            status=acceptance,
            recorded_at=received_at or "",
            recorded_by=received_by or destination["vault_id"],
            local_record_id=local_record_id,
        ),
    }


def revalidate_package(
    package: dict,
    record: dict,
    authority_resolution: dict,
    conciliation: dict,
    *,
    destination_vault: dict | None = None,
) -> dict:
    delivery = package.get("delivery", {})
    if package.get("source_record_id") != record.get("record_id") or package.get("source_record_version") != record.get("record_version"):
        raise ContractError("revalidation Record identity or version does not match Package")
    if record.get("staleness", "current") in {"stale", "revalidation_required"}:
        raise ContractError("Package requires revalidation because its source is stale")
    if authority_resolution.get("status") == "revoked":
        raise ContractError("Package authority has been revoked")
    if authority_resolution.get("status") not in {"resolved", "unavailable"}:
        raise ContractError("Package authority resolution is unavailable")
    expected_authority = package.get("authority_snapshot", {}).get("selected_authority_id")
    if authority_resolution.get("selected_authority_id") != expected_authority:
        raise ContractError("Package source authority resolution changed")
    current = classify_conciliation(
        conciliation.get("state", ""),
        conciliation.get("sources", []),
        authoritative_source_id=conciliation.get("authoritative_source_id"),
    )
    if current["state"] != delivery.get("conciliation", {}).get("state") or current["source_ids"] != delivery.get("conciliation", {}).get("source_ids"):
        raise ContractError("Package conciliation changed and requires reassembly")
    if destination_vault is not None:
        destination = validate_vault_contract(destination_vault)
        if destination["vault_id"] != delivery.get("destination_vault", {}).get("vault_id"):
            raise ContractError("Package destination changed and requires reassembly")
    expected_fingerprint = package_fingerprint(
        record,
        package.get("selected_chunk_ids", []),
        package.get("artifact_ids", []),
        package.get("effective_visibility", "internal"),
        current_use=delivery.get("purpose") == "current_use",
        entity_operation=package.get("assembly_entity_operation"),
    )
    if expected_fingerprint != package.get("fingerprint"):
        raise ContractError("Package fingerprint no longer matches its assembly")
    return {
        "status": "valid",
        "package_id": package.get("package_id"),
        "checked_authority_id": authority_resolution["selected_authority_id"],
        "authority_access": authority_resolution.get("status"),
    }
