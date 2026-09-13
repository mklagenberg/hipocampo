#!/usr/bin/env python3
"""Exercise the corrected V3 Package, authority and REM-receipt contract."""
from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path

import yaml

from v3_crud_engine import ContractError
from v3_package_engine import (
    classify_conciliation,
    create_delivery_package,
    receive_package,
    revalidate_package,
    resolve_authority,
)


def expect_block(callback, label: str, errors: list[str]) -> None:
    try:
        callback()
    except ContractError:
        return
    errors.append(f"{label}: expected contract block")


def delivery_record() -> dict:
    return {
        "record_id": "rec-personal-liferay-001",
        "record_version": 1,
        "physical_path": "records/liferay/personal-source.md",
        "status": "active",
        "visibility": "internal",
        "staleness": "current",
        "maturity": "curated",
        "processing_state": "consolidated",
        "entity": "personal-entity",
        "scope": "liferay",
        "source": {"source_id": "source-liferay", "source_kind": "curated-knowledge", "entity": "personal-entity"},
        "vault": {"vault_id": "personal-vault", "entity": "personal-entity", "profile": "personal", "role": "anchor"},
        "collection_ids": ["col-liferay"],
        "chunks": [
            {"chunk_id": "chk-liferay-public", "parent_record_id": "rec-personal-liferay-001", "text_ref": "public-technical-knowledge"},
            {"chunk_id": "chk-liferay-private", "parent_record_id": "rec-personal-liferay-001", "text_ref": "private-opinion"},
        ],
        "artifacts": [
            {"artifact_id": "art-liferay-guide", "reference": "artifacts/liferay-guide.md", "visibility": "internal", "version": 1},
            {"artifact_id": "art-private-note", "reference": "artifacts/private-note.md", "visibility": "restricted", "version": 1},
        ],
    }


def source_context(source_id: str, entity: str, vault_id: str, scope: str) -> dict:
    return {
        "source_id": source_id,
        "entity": entity,
        "vault_id": vault_id,
        "scope": scope,
        "provenance": "record-and-curation",
        "epistemic_nature": "curated",
        "version": 1,
        "staleness": "current",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    fixture = yaml.safe_load((root / "docs/v3-package-fixtures.yaml").read_text(encoding="utf-8"))
    errors: list[str] = []
    if len(fixture.get("cases", [])) != 12:
        errors.append("expected twelve Package delivery fixtures")

    record = delivery_record()
    chain = [
        {"authority_id": "personal-primary", "entity": "personal-entity", "scope": "liferay"},
        {"authority_id": "personal-successor", "entity": "personal-entity", "scope": "liferay"},
    ]
    successor_resolved = resolve_authority("personal-entity", "liferay", chain, {"personal-successor"})
    if successor_resolved["status"] != "resolved" or successor_resolved["selected_authority_id"] != "personal-successor":
        errors.append("logical hereditary resolution did not select the accessible successor")
    resolved = resolve_authority("personal-entity", "liferay", chain, {"personal-primary"})
    unavailable = resolve_authority("personal-entity", "liferay", chain, set())
    if unavailable["status"] != "unavailable" or unavailable["selected_authority_id"] != "personal-primary":
        errors.append("inaccessible origin was not represented as an audit frontier")
    revoked = resolve_authority(
        "personal-entity", "liferay", [{"authority_id": "personal-primary", "entity": "personal-entity", "scope": "liferay", "status": "revoked"}], None
    )
    if revoked["status"] != "revoked":
        errors.append("revoked logical authority did not block resolution")
    expect_block(
        lambda: resolve_authority("personal-entity", "liferay", [{**chain[0], "active": True}], None),
        "physical active authority state",
        errors,
    )

    destination = {"vault_id": "company-entity-vault", "entity": "company-entity", "profile": "entity", "role": "anchor"}
    package_authority = {
        "generator_id": "curator-personal",
        "generator_vault_id": "personal-vault",
        "vault": record["vault"],
    }
    operation = {
        "operation": "send",
        "actor": {"actor_id": "curator-personal", "roles": ["curator"]},
        "source": record["source"],
        "source_vault": record["vault"],
        "destination_vault": destination,
        "entity": "personal-entity",
        "scope": "liferay",
        "authority": {"authority_id": resolved["selected_authority_id"], "entity": "personal-entity", "scope": "liferay"},
        "destination_accepted": True,
        "owner_approved": True,
        "minimized": True,
    }
    conciliation = classify_conciliation(
        "equivalent",
        [source_context("source-liferay", "personal-entity", "personal-vault", "liferay")],
        authoritative_source_id="source-liferay",
    )
    expect_block(
        lambda: create_delivery_package(
            record, ["chk-liferay-public"], "internal", authority_resolution=resolved, conciliation=conciliation,
            package_authority=package_authority, destination_vault=destination, purpose="review", current_use=True,
            entity_operation=operation,
        ),
        "purpose/current_use mismatch",
        errors,
    )
    package = create_delivery_package(
        record,
        ["chk-liferay-public"],
        "internal",
        authority_resolution=resolved,
        conciliation=conciliation,
        package_authority=package_authority,
        destination_vault=destination,
        purpose="current_use",
        current_use=True,
        entity_operation=operation,
        artifact_ids=["art-liferay-guide"],
        recorded_at="2026-09-09T10:00:00Z",
    )
    if package["artifact_ids"] != ["art-liferay-guide"] or not package["package_id"].startswith("pkg-rec-personal-liferay-001-v1-"):
        errors.append("Package did not preserve explicit Artifact selection and deterministic identity")
    if package["delivery"]["package_authority"]["generator_vault_id"] != "personal-vault":
        errors.append("Package authority was not bound to the generating vault")
    expect_block(
        lambda: create_delivery_package(
            record, ["chk-liferay-public"], "internal", authority_resolution=resolved, conciliation=conciliation,
            package_authority={**package_authority, "generator_vault_id": "company-entity-vault"}, destination_vault=destination,
            purpose="review", entity_operation=operation,
        ),
        "unbound Package generator vault",
        errors,
    )

    received = receive_package(
        package,
        destination,
        local_record_id="rec-company-liferay-001",
        acceptance="accepted",
        received_at="2026-09-09T10:01:00Z",
        received_by="company-curator",
    )
    local = received["local_record"]
    if local["processing_state"] != "new" or local["curation_status"] != "pending_rem":
        errors.append("received representation was not held for REM")
    if received["ledger_entry"]["direction"] != "received" or received["ledger_entry"]["delivery_id"] != package["delivery"]["delivery_id"]:
        errors.append("received ledger entry was not paired with sent Package")

    checked = revalidate_package(package, record, unavailable, conciliation, destination_vault=destination)
    if checked["status"] != "valid" or checked["authority_access"] != "unavailable":
        errors.append("accepted Package did not revalidate through an inaccessible origin frontier")
    tampered = deepcopy(package)
    tampered["selected_chunk_ids"] = ["chk-liferay-private"]
    expect_block(lambda: revalidate_package(tampered, record, resolved, conciliation), "tampered Package fingerprint", errors)
    expect_block(
        lambda: revalidate_package(package, record, revoked, conciliation),
        "revoked Package authority",
        errors,
    )

    conflict = classify_conciliation(
        "unresolved_conflict",
        [
            source_context("source-liferay", "personal-entity", "personal-vault", "liferay"),
            source_context("source-company", "company-entity", "company-entity-vault", "liferay"),
        ],
        authoritative_source_id="source-liferay",
    )
    expect_block(
        lambda: create_delivery_package(
            record, ["chk-liferay-public"], "internal", authority_resolution=resolved, conciliation=conflict,
            package_authority=package_authority, destination_vault=destination, purpose="current_use", current_use=True,
            entity_operation=operation,
        ),
        "current-use unresolved conflict",
        errors,
    )
    discussion = create_delivery_package(
        record, ["chk-liferay-public"], "internal", authority_resolution=resolved, conciliation=conflict,
        package_authority=package_authority, destination_vault=destination, purpose="discussion", entity_operation=operation,
        artifact_ids=["art-liferay-guide"],
        recorded_at="2026-09-09T10:02:00Z",
    )
    if not discussion["delivery"]["conflict_bearing"]:
        errors.append("discussion Package lost explicit conflict state")

    if errors:
        print(f"validate_v3_package_delivery: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_v3_package_delivery: OK — logical authority, Package snapshot, REM receipt, conflict gates and revalidation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
