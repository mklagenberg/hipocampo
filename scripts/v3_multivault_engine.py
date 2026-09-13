#!/usr/bin/env python3
"""Typed, privacy-bounded multivault graph resolution for V3 X4.2."""
from __future__ import annotations


class MultivaultError(ValueError):
    pass


RELATION_TYPES = {"same_entity_delivery", "cross_entity_delivery", "reference", "successor", "split", "copy"}


def validate_graph(vaults: list[dict], relations: list[dict]) -> dict:
    ids = [vault.get("vault_id") for vault in vaults]
    if any(not value for value in ids) or len(ids) != len(set(ids)):
        raise MultivaultError("vault IDs must be unique and non-empty")
    known = set(ids)
    errors: list[str] = []
    for relation in relations:
        if relation.get("relation_id") in {None, ""}:
            errors.append("relation_missing_id")
        if relation.get("kind") not in RELATION_TYPES:
            errors.append("relation_unknown_type")
        if relation.get("from_vault_id") not in known or relation.get("to_vault_id") not in known:
            errors.append("relation_unknown_vault")
        if not relation.get("scope"):
            errors.append("relation_missing_scope")
    return {"valid": not errors, "errors": errors, "vault_count": len(vaults), "relation_count": len(relations)}


def detect_successor_cycles(relations: list[dict]) -> list[list[str]]:
    graph: dict[str, list[str]] = {}
    for relation in relations:
        if relation.get("kind") == "successor":
            graph.setdefault(relation.get("from_vault_id"), []).append(relation.get("to_vault_id"))
    cycles: list[list[str]] = []
    def visit(node: str, path: list[str]) -> None:
        if node in path:
            cycles.append(path[path.index(node):] + [node])
            return
        for target in graph.get(node, []):
            visit(target, path + [node])
    for node in graph:
        visit(node, [])
    return cycles


def detect_authority_collisions(authorities: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str], list[dict]] = {}
    for authority in authorities:
        key = (authority.get("entity", ""), authority.get("scope", ""))
        if authority.get("status", "active") != "revoked":
            grouped.setdefault(key, []).append(authority)
    return [{"entity": key[0], "scope": key[1], "authority_ids": [item.get("authority_id") for item in values]}
            for key, values in grouped.items() if len(values) > 1]


def resolve_visible_graph(*, start_vault_id: str, vaults: list[dict], relations: list[dict], accessible_vault_ids: set[str]) -> dict:
    graph_check = validate_graph(vaults, relations)
    if not graph_check["valid"]:
        raise MultivaultError("invalid vault graph: " + ", ".join(graph_check["errors"]))
    index = {vault["vault_id"]: vault for vault in vaults}
    if start_vault_id not in index:
        raise MultivaultError("unknown start vault")
    visible: set[str] = set()
    frontiers = 0
    findings: list[str] = []
    pending = [start_vault_id]
    while pending:
        current = pending.pop()
        if current in visible:
            continue
        if current not in accessible_vault_ids:
            frontiers += 1
            continue
        visible.add(current)
        for relation in relations:
            if relation.get("from_vault_id") != current:
                continue
            target = relation.get("to_vault_id")
            if target not in accessible_vault_ids:
                frontiers += 1
                continue
            pending.append(target)
    if detect_successor_cycles(relations):
        findings.append("successor_cycle")
    if detect_authority_collisions([item for vault in vaults for item in vault.get("authorities", [])]):
        findings.append("authority_collision")
    return {
        "visible_vault_ids": sorted(visible),
        "coverage": "partial" if frontiers else "complete",
        "inaccessible_frontiers": frontiers,
        "findings": findings,
        "privacy_note": "inaccessible vault identity and content were not included in the visible result",
    }
