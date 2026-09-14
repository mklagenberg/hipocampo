#!/usr/bin/env python3
"""Adversarial L4R exercise for three anonymized entity-bound vault flows."""
from __future__ import annotations

from copy import deepcopy

from v3_audit_engine import audit_delivery_graph, pair_ledger_entries
from v3_package_engine import classify_conciliation, create_delivery_package, receive_package, resolve_authority

from validate_v3_package_delivery import delivery_record, source_context  # type: ignore


def operation(record: dict, destination_vault: dict, source_entity: str, authority_id: str) -> dict:
    return {
        "operation": "send",
        "actor": {"actor_id": f"curator-{source_entity}", "roles": ["curator"]},
        "source": record["source"],
        "source_vault": record["vault"],
        "destination_vault": destination_vault,
        "entity": source_entity,
        "scope": record["scope"],
        "authority": {"authority_id": authority_id, "entity": source_entity, "scope": record["scope"]},
        "destination_accepted": True,
        "owner_approved": True,
        "minimized": True,
    }


def main() -> int:
    errors: list[str] = []
    personal_record = delivery_record()
    personal_authority = resolve_authority(
        "personal-entity", "liferay", [{"authority_id": "personal-liferay", "entity": "personal-entity", "scope": "liferay"}], None
    )
    company_vault = {"vault_id": "company-entity-vault", "entity": "company-entity", "profile": "entity", "role": "anchor"}
    client_vault = {"vault_id": "client-team-liferay", "entity": "client-entity", "profile": "team", "role": "additional", "scope_description": "Liferay client project"}
    personal_package = create_delivery_package(
        personal_record,
        ["chk-liferay-public"],
        "internal",
        authority_resolution=personal_authority,
        conciliation=classify_conciliation(
            "equivalent", [source_context("source-liferay", "personal-entity", "personal-vault", "liferay")], authoritative_source_id="source-liferay"
        ),
        package_authority={"generator_id": "curator-personal", "generator_vault_id": "personal-vault", "vault": personal_record["vault"]},
        destination_vault=company_vault,
        purpose="current_use",
        current_use=True,
        entity_operation=operation(personal_record, company_vault, "personal-entity", "personal-liferay"),
        artifact_ids=["art-liferay-guide"],
        recorded_at="2026-09-09T10:00:00Z",
    )
    company_received = receive_package(
        personal_package,
        company_vault,
        local_record_id="rec-company-liferay-001",
        acceptance="accepted",
        received_at="2026-09-09T10:01:00Z",
        received_by="company-curator",
    )
    company_record = deepcopy(company_received["local_record"])
    company_record.update({
        "record_id": "rec-company-liferay-001",
        "record_version": 1,
        "maturity": "curated",
        "processing_state": "consolidated",
        "curation_status": "curated",
        "entity": "company-entity",
        "source": {"source_id": "source-company-liferay", "source_kind": "company-curation", "entity": "company-entity"},
        "vault": company_vault,
        "collection_ids": ["col-company-liferay"],
    })
    for chunk in company_record["chunks"]:
        chunk["parent_record_id"] = company_record["record_id"]
    company_chunk_id = company_record["chunks"][0]["chunk_id"]
    company_authority = resolve_authority("company-entity", "liferay", [{"authority_id": "company-liferay", "entity": "company-entity", "scope": "liferay"}], None)
    company_package = create_delivery_package(
        company_record,
        [company_chunk_id],
        "internal",
        authority_resolution=company_authority,
        conciliation=classify_conciliation(
            "update", [source_context("source-company-liferay", "company-entity", "company-entity-vault", "liferay")], authoritative_source_id="source-company-liferay"
        ),
        package_authority={"generator_id": "curator-company", "generator_vault_id": "company-entity-vault", "vault": company_vault},
        destination_vault=client_vault,
        purpose="review",
        entity_operation=operation(company_record, client_vault, "company-entity", "company-liferay"),
        artifact_ids=["art-liferay-guide"],
        recorded_at="2026-09-09T11:00:00Z",
    )
    client_received = receive_package(
        company_package,
        client_vault,
        local_record_id="rec-client-liferay-001",
        acceptance="accepted",
        received_at="2026-09-09T11:01:00Z",
        received_by="client-curator",
    )
    client_record = client_received["local_record"]

    vaults = [
        {
            "vault_id": "personal-vault",
            "entity": "personal-entity",
            "accessible": False,
            "records": [personal_record],
            "packages_sent": [personal_package["ledger_entry"]],
            "packages_received": [],
        },
        {
            "vault_id": "company-entity-vault",
            "entity": "company-entity",
            "accessible": True,
            "records": [company_record],
            "packages_sent": [company_package["ledger_entry"]],
            "packages_received": [company_received["ledger_entry"]],
        },
        {
            "vault_id": "client-team-liferay",
            "entity": "client-entity",
            "accessible": True,
            "records": [client_record],
            "packages_sent": [],
            "packages_received": [client_received["ledger_entry"]],
        },
    ]
    partial = audit_delivery_graph(vaults, start_vault_id="client-team-liferay", start_record_id="rec-client-liferay-001")
    if partial["coverage"] != "partial" or partial["integrity"] != "valid" or partial["circulation"] != "confirmed":
        errors.append(f"inaccessible origin produced the wrong audit result: {partial}")

    complete_vaults = deepcopy(vaults)
    complete_vaults[0]["accessible"] = True
    complete = audit_delivery_graph(complete_vaults, start_vault_id="client-team-liferay", start_record_id="rec-client-liferay-001")
    if complete["coverage"] != "complete" or complete["integrity"] != "valid":
        errors.append(f"complete bilateral chain did not audit successfully: {complete}")

    unconfirmed_vaults = deepcopy(complete_vaults)
    unconfirmed_vaults[2]["packages_received"] = []
    unconfirmed = audit_delivery_graph(unconfirmed_vaults, start_vault_id="company-entity-vault", start_record_id="rec-company-liferay-001")
    if unconfirmed["circulation"] != "sent_unconfirmed":
        errors.append(f"missing received ledger was not classified as an alert: {unconfirmed}")

    mismatch_vaults = deepcopy(complete_vaults)
    mismatch_vaults[2]["packages_received"][0]["fingerprint"] = "sha256:tampered"
    mismatch = audit_delivery_graph(mismatch_vaults, start_vault_id="company-entity-vault", start_record_id="rec-company-liferay-001")
    if mismatch["integrity"] != "mismatch":
        errors.append(f"fingerprint mismatch did not fail deterministically: {mismatch}")

    orphan = pair_ledger_entries(None, client_received["ledger_entry"])
    if orphan["circulation"] != "received_orphan" or orphan["integrity"] != "broken":
        errors.append(f"orphan receipt classification was wrong: {orphan}")

    if errors:
        print(f"validate_v3_l4r_closure: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_v3_l4r_closure: OK — bilateral audit, inaccessible frontier, alerts, mismatch blocking and three-entity chain")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
