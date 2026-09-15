#!/usr/bin/env python3
"""Local read-only V3 Search & Progressive Disclosure primitives."""
from __future__ import annotations

from copy import deepcopy
import re

from v3_crud_engine import ContractError, RecordCrud


LEVELS = ("L0", "L1", "L2", "L3", "L4")
LEVEL_RANK = {level: index for index, level in enumerate(LEVELS)}
PRESENTATIONS = {"prose-default", "structured-on-request"}


class SearchContractError(ValueError):
    """Raised when a search request cannot satisfy the read-side contract."""


def _lower_level(left: str, right: str) -> str:
    return LEVELS[min(LEVEL_RANK[left], LEVEL_RANK[right])]


def _validate_request(request: dict) -> dict:
    required = {
        "request_id", "query", "entity", "vault_scope", "authorized_vault_ids",
        "knowledge_scope", "requested_disclosure",
    }
    missing = required - request.keys()
    if missing:
        raise SearchContractError(f"missing request fields: {sorted(missing)}")
    if not isinstance(request["request_id"], str) or not request["request_id"].strip():
        raise SearchContractError("request_id must be non-empty")
    if not isinstance(request["query"], str) or not request["query"].strip():
        raise SearchContractError("query must be non-empty")
    if not isinstance(request["entity"], str) or not request["entity"].strip():
        raise SearchContractError("entity must be non-empty")
    for field in ("vault_scope", "authorized_vault_ids"):
        if not isinstance(request[field], list) or not request[field] or any(not isinstance(item, str) or not item.strip() for item in request[field]):
            raise SearchContractError(f"{field} must be a non-empty list of strings")
    if not set(request["vault_scope"]).issubset(set(request["authorized_vault_ids"])):
        raise SearchContractError("vault_scope must be contained in authorized_vault_ids")
    if not isinstance(request["knowledge_scope"], str) or not request["knowledge_scope"].strip():
        raise SearchContractError("knowledge_scope must be non-empty")
    requested = request["requested_disclosure"]
    if requested not in LEVEL_RANK:
        raise SearchContractError(f"unknown disclosure level: {requested}")
    presentation = request.get("presentation", "prose-default")
    if presentation not in PRESENTATIONS:
        raise SearchContractError(f"unknown presentation mode: {presentation}")
    if presentation == "structured-on-request" and request.get("explicit_structured_request") is not True:
        raise SearchContractError("structured presentation requires an explicit request")
    if not isinstance(request.get("explicit_expansion_authorization", False), bool):
        raise SearchContractError("explicit_expansion_authorization must be boolean")
    return deepcopy(request)


def _terms(query: str) -> list[str]:
    return re.findall(r"[\w-]+", query.casefold())


def _record_text(record: dict) -> str:
    parts = [str(record.get("title", "")), str(record.get("text", ""))]
    for chunk in record.get("chunks", []):
        parts.extend([str(chunk.get("text_ref", "")), str(chunk.get("text", ""))])
    return " ".join(parts).casefold()


def _relevance(record: dict, terms: list[str]) -> float:
    haystack = _record_text(record)
    if not terms:
        return 0.0
    return round(sum(term in haystack for term in set(terms)) / len(set(terms)), 3)


def _matching_chunks(record: dict, terms: list[str]) -> list[dict]:
    return [
        deepcopy(chunk)
        for chunk in record.get("chunks", [])
        if any(term in str(chunk.get("text", "")).casefold() for term in terms)
    ]


def _limits(record: dict, *, source_accessible: bool) -> list[str]:
    limits: list[str] = []
    if not source_accessible:
        limits.append("source_access_unavailable")
    if record.get("staleness") in {"stale", "revalidation_required"}:
        limits.append("source_requires_revalidation")
    if record.get("privacy") == "blocked" or record.get("visibility") == "restricted":
        limits.append("privacy_boundary_blocks_content")
    if record.get("authority_state", "unknown") in {"unknown", "conflicting"}:
        limits.append("authority_requires_contextual_review")
    return limits


def _result_envelope(record: dict, request: dict, *, relevance: float, chunks: list[dict], source_accessible: bool) -> dict:
    requested = request["requested_disclosure"]
    explicit = request.get("explicit_expansion_authorization", False)
    limits = _limits(record, source_accessible=source_accessible)
    disposition = "accepted"
    returned = requested
    if not source_accessible:
        returned = "L0"
        disposition = "blocked"
    elif record.get("privacy") == "blocked" or record.get("visibility") == "restricted":
        returned = "L1"
        disposition = "blocked"
    elif requested == "L4" and not explicit:
        returned = "L0"
        disposition = "blocked"
        limits.append("expanded_disclosure_requires_explicit_authorization")
    elif LEVEL_RANK[requested] > LEVEL_RANK["L2"] and not explicit:
        returned = "L2"
        disposition = "partial"
        limits.append("requested_content_level_requires_explicit_authorization")
    elif record.get("staleness") in {"stale", "revalidation_required"}:
        returned = _lower_level(requested, "L2")
        disposition = "partial"

    source = record.get("source", {})
    envelope = {
        "record_ref": record["record_id"],
        "relevance": relevance,
        "authority": record.get("authority_state", "unknown"),
        "privacy": "redacted" if record.get("privacy") == "redacted" else "allowed",
        "epistemic_status": record.get("epistemic_status", "unknown"),
        "disclosure_level": returned,
        "evidence": [source.get("source_id", "source-unavailable")],
        "limits": sorted(set(limits)),
        "retrieval_path": f"record:{record['record_id']}" if returned == "L0" else f"record:{record['record_id']}/bounded",
        "mutation": "none",
        "disposition": disposition,
    }
    if LEVEL_RANK[returned] >= LEVEL_RANK["L1"]:
        envelope["metadata"] = {
            "record_id": record["record_id"],
            "record_version": record.get("record_version"),
            "entity": record.get("entity"),
            "vault_id": record.get("vault", {}).get("vault_id"),
        }
    if LEVEL_RANK[returned] >= LEVEL_RANK["L2"]:
        envelope["record_envelope"] = {
            "scope": record.get("scope"),
            "status": record.get("status"),
            "staleness": record.get("staleness"),
            "source_kind": source.get("source_kind"),
            "governance": deepcopy(record.get("governance", {})),
        }
    if LEVEL_RANK[returned] >= LEVEL_RANK["L3"]:
        envelope["selected_chunks"] = [
            {"chunk_id": chunk.get("chunk_id"), "text": chunk.get("text", "")}
            for chunk in chunks
        ]
    if returned == "L4":
        envelope["expanded_content"] = [
            {"chunk_id": chunk.get("chunk_id"), "text": chunk.get("text", "")}
            for chunk in record.get("chunks", [])
        ]
    return envelope


def _prose(envelopes: list[dict], request: dict) -> str:
    if not envelopes:
        return f"Não encontrei material dentro do escopo autorizado para '{request['query']}'. Limite: nenhum resultado recuperável."
    parts: list[str] = []
    for item in envelopes:
        limit_text = "; ".join(item["limits"]) if item["limits"] else "sem limitações adicionais identificadas"
        parts.append(
            f"Encontrei {item['record_ref']} com relevância {item['relevance']:.3f}; "
            f"a autoridade está {item['authority']}, a divulgação ficou em {item['disclosure_level']} "
            f"e o limite observado é {limit_text}."
        )
    return " ".join(parts)


def search(crud: RecordCrud, request: dict) -> dict:
    """Run a local read-only search through the canonical CRUD read boundary."""
    if not isinstance(crud, RecordCrud):
        raise SearchContractError("search requires the canonical RecordCrud gateway")
    validated = _validate_request(request)
    before = crud.records
    before_events = len(crud.events)
    terms = _terms(validated["query"])
    envelopes: list[dict] = []
    inaccessible = False
    for record_id, snapshot in before.items():
        if snapshot.get("entity") != validated["entity"]:
            continue
        if snapshot.get("vault", {}).get("vault_id") not in validated["vault_scope"]:
            continue
        if snapshot.get("scope") != validated["knowledge_scope"]:
            continue
        relevance = _relevance(snapshot, terms)
        if relevance <= 0:
            continue
        source_accessible = snapshot.get("source_accessible", True)
        if not source_accessible:
            inaccessible = True
        try:
            read = crud.apply({
                "operation": "read",
                "record_id": record_id,
                "actor": {"authorized_vault_ids": validated["authorized_vault_ids"]},
            })
            record = read["record"]
        except ContractError as exc:
            inaccessible = True
            record = deepcopy(snapshot)
            record["source_accessible"] = False
            record["read_error"] = str(exc)
        envelopes.append(_result_envelope(
            record,
            validated,
            relevance=relevance,
            chunks=_matching_chunks(record, terms),
            source_accessible=source_accessible and "read_error" not in record,
        ))
    envelopes.sort(key=lambda item: (-item["relevance"], item["record_ref"]))
    if any(item["disposition"] == "blocked" for item in envelopes):
        disposition = "blocked"
    elif any(item["disposition"] == "partial" for item in envelopes) or inaccessible:
        disposition = "partial"
    else:
        disposition = "accepted" if envelopes else "partial"
    returned_level = min((LEVEL_RANK[item["disclosure_level"]] for item in envelopes), default=0)
    limits = sorted({limit for item in envelopes for limit in item["limits"]})
    trail = {
        "request_id": validated["request_id"],
        "entity": validated["entity"],
        "vault_scope": sorted(validated["vault_scope"]),
        "returned_level": LEVELS[returned_level],
        "disposition": disposition,
        "retrieval_path": "redacted-local-crud-read",
        "limits": limits,
    }
    if validated.get("presentation", "prose-default") == "structured-on-request":
        presentation = {"mode": "structured-on-request", "results": deepcopy(envelopes)}
    else:
        presentation = {"mode": "prose-default", "text": _prose(envelopes, validated)}
    after = crud.records
    if before != after or len(crud.events) != before_events:
        raise SearchContractError("search mutated the CRUD state")
    return {
        "status": disposition,
        "presentation": presentation,
        "results": deepcopy(envelopes),
        "trail": trail,
        "mutation": "none",
    }
