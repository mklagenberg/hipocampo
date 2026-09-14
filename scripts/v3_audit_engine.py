#!/usr/bin/env python3
"""Deterministic bilateral Package-ledger audit over an available vault graph."""
from __future__ import annotations

from copy import deepcopy

from v3_crud_engine import ContractError


def _key(entry: dict) -> tuple[str, int, str]:
    return (entry.get("package_id", ""), int(entry.get("package_version", 0)), entry.get("fingerprint", ""))


def _identity(entry: dict) -> tuple[str, int]:
    return (entry.get("package_id", ""), int(entry.get("package_version", 0)))


def pair_ledger_entries(sent: dict | None, received: dict | None, *, expected_fingerprint: str | None = None) -> dict:
    """Compare one source event and one destination event without semantic judgment."""
    if sent is None and received is None:
        raise ContractError("ledger pair requires at least one entry")
    if sent is None:
        return {"circulation": "received_orphan", "integrity": "broken", "findings": ["missing_sent_entry"]}
    if received is None:
        return {"circulation": "sent_unconfirmed", "integrity": "valid", "findings": ["missing_received_entry"]}
    required = {"delivery_id", "package_id", "package_version", "fingerprint", "recorded_at", "recorded_by"}
    if required - sent.keys() or required - received.keys():
        return {"circulation": "confirmed", "integrity": "broken", "findings": ["ledger_entry_missing_trace_metadata"]}
    if _key(sent) != _key(received):
        return {"circulation": "confirmed", "integrity": "mismatch", "findings": ["package_identity_or_fingerprint_mismatch"]}
    if expected_fingerprint and (sent.get("fingerprint") != expected_fingerprint or received.get("fingerprint") != expected_fingerprint):
        return {"circulation": "confirmed", "integrity": "mismatch", "findings": ["record_fingerprint_mismatch"]}
    if sent.get("source_vault_id") != received.get("source_vault_id"):
        return {"circulation": "confirmed", "integrity": "mismatch", "findings": ["source_vault_mismatch"]}
    if sent.get("destination_vault_id") != received.get("destination_vault_id"):
        return {"circulation": "confirmed", "integrity": "mismatch", "findings": ["destination_vault_mismatch"]}
    if sent.get("selected_chunk_ids") != received.get("selected_chunk_ids") or sent.get("artifact_ids") != received.get("artifact_ids"):
        return {"circulation": "confirmed", "integrity": "mismatch", "findings": ["selection_mismatch"]}
    return {"circulation": "confirmed", "integrity": "valid", "findings": []}


def _index_vaults(vaults: list[dict]) -> dict[str, dict]:
    indexed: dict[str, dict] = {}
    for vault in vaults:
        vault_id = vault.get("vault_id")
        if not vault_id or vault_id in indexed:
            raise ContractError("audit vault IDs must be unique and non-empty")
        indexed[vault_id] = {
            "vault_id": vault_id,
            "entity": vault.get("entity"),
            "accessible": bool(vault.get("accessible", True)),
            "records": {record.get("record_id"): record for record in vault.get("records", []) if record.get("record_id")},
            "sent": [entry for entry in vault.get("packages_sent", []) if entry.get("direction", "sent") == "sent"],
            "received": [entry for entry in vault.get("packages_received", []) if entry.get("direction", "received") == "received"],
        }
    return indexed


def audit_delivery_graph(vaults: list[dict], *, start_vault_id: str, start_record_id: str) -> dict:
    """Trace backward provenance and forward circulation from a local Record."""
    indexed = _index_vaults(vaults)
    if start_vault_id not in indexed:
        raise ContractError("audit start vault is unknown")
    findings: list[str] = []
    frontiers: list[dict] = []
    verified_nodes: list[dict] = []
    visited_backward: set[tuple[str, str]] = set()
    visited_forward: set[tuple[str, str]] = set()
    integrity = "valid"
    circulation = "confirmed"

    def add_frontier(vault_id: str, reason: str, record_id: str | None = None) -> None:
        item = {"vault_id": vault_id, "reason": reason}
        if record_id:
            item["record_id"] = record_id
        if item not in frontiers:
            frontiers.append(item)

    def check_pair(package_id: str, package_version: int, fingerprint: str, source_vault_id: str, destination_vault_id: str) -> None:
        nonlocal integrity, circulation
        source = indexed.get(source_vault_id)
        destination = indexed.get(destination_vault_id)
        sent = None
        received = None
        if source and source["accessible"]:
            sent = next((entry for entry in source["sent"] if _identity(entry) == (package_id, package_version)), None)
        elif source:
            add_frontier(source_vault_id, "source_vault_inaccessible")
        if destination and destination["accessible"]:
            received = next((entry for entry in destination["received"] if _identity(entry) == (package_id, package_version)), None)
        elif destination:
            add_frontier(destination_vault_id, "destination_vault_inaccessible")
        if (source and not source["accessible"]) or (destination and not destination["accessible"]):
            if "counterpart_unavailable" not in findings:
                findings.append("counterpart_unavailable")
            return
        result = pair_ledger_entries(sent, received, expected_fingerprint=fingerprint)
        if result["integrity"] != "valid":
            integrity = result["integrity"]
        if result["circulation"] != "confirmed":
            circulation = result["circulation"]
        findings.extend(item for item in result["findings"] if item not in findings)

    def backward(vault_id: str, record_id: str) -> None:
        key = (vault_id, record_id)
        if key in visited_backward:
            return
        visited_backward.add(key)
        vault = indexed[vault_id]
        if not vault["accessible"]:
            add_frontier(vault_id, "vault_inaccessible", record_id)
            return
        record = vault["records"].get(record_id)
        if record is None:
            findings.append("broken_record_reference")
            return
        verified_nodes.append({"direction": "backward", "vault_id": vault_id, "record_id": record_id})
        received = record.get("received_via", {})
        if not received.get("package_id"):
            return
        source_vault_id = record.get("origin_vault_id")
        if not source_vault_id:
            findings.append("missing_origin_vault_reference")
            return
        check_pair(
            received["package_id"],
            received.get("package_version", 0),
            received.get("fingerprint", ""),
            source_vault_id,
            vault_id,
        )
        source = indexed.get(source_vault_id)
        if source is None:
            add_frontier(source_vault_id, "vault_not_registered", record.get("origin_record_id"))
        elif not source["accessible"]:
            add_frontier(source_vault_id, "vault_inaccessible", record.get("origin_record_id"))
        else:
            backward(source_vault_id, record.get("origin_record_id", ""))

    def forward(vault_id: str, record_id: str) -> None:
        key = (vault_id, record_id)
        if key in visited_forward:
            return
        visited_forward.add(key)
        vault = indexed[vault_id]
        if not vault["accessible"]:
            add_frontier(vault_id, "vault_inaccessible", record_id)
            return
        for sent in vault["sent"]:
            if sent.get("source_record_id") != record_id:
                continue
            destination_vault_id = sent.get("destination_vault_id")
            package_id = sent.get("package_id")
            package_version = sent.get("package_version", 0)
            fingerprint = sent.get("fingerprint", "")
            if not destination_vault_id:
                findings.append("missing_destination_vault_reference")
                continue
            check_pair(package_id, package_version, fingerprint, vault_id, destination_vault_id)
            destination = indexed.get(destination_vault_id)
            if destination is None:
                add_frontier(destination_vault_id, "vault_not_registered")
            elif not destination["accessible"]:
                add_frontier(destination_vault_id, "vault_inaccessible")
            else:
                received = next((entry for entry in destination["received"] if _identity(entry) == _identity(sent)), None)
                if received and received.get("local_record_id"):
                    forward(destination_vault_id, received["local_record_id"])

    backward(start_vault_id, start_record_id)
    forward(start_vault_id, start_record_id)
    coverage = "partial" if frontiers else "complete"
    return {
        "coverage": coverage,
        "integrity": integrity,
        "circulation": circulation,
        "governance": "accepted",
        "start": {"vault_id": start_vault_id, "record_id": start_record_id},
        "verified_nodes": verified_nodes,
        "frontiers": frontiers,
        "findings": findings,
    }
