#!/usr/bin/env python3
"""Local read-only V3 Search & Progressive Disclosure primitives."""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime
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


def _artifact_accessible(record: dict) -> bool:
    """Return whether linked Artifacts are available for direct verification.

    Record content remains readable when this is false.  The flag only limits
    provenance/currentness checks and Artifact-dependent operations.
    """
    artifacts = record.get("artifacts", [])
    if not artifacts:
        return True
    return all(artifact.get("accessibility", "available") == "available" for artifact in artifacts)


def _limits(record: dict, *, artifact_accessible: bool, record_readable: bool) -> list[str]:
    limits: list[str] = []
    if not artifact_accessible:
        limits.append("artifact_access_unavailable")
    if not record_readable:
        limits.append("record_content_unavailable")
    if record.get("staleness") in {"stale", "revalidation_required"}:
        limits.append("record_requires_revalidation")
    if record.get("privacy") == "blocked" or record.get("visibility") == "restricted":
        limits.append("privacy_boundary_blocks_content")
    if record.get("authority_state", "unknown") in {"unknown", "conflicting"}:
        limits.append("authority_requires_contextual_review")
    return limits


def _artifact_freshness_note(record: dict, *, artifact_accessible: bool) -> str | None:
    """Describe the represented source-version boundary without exposing access state."""
    if artifact_accessible:
        return None
    artifacts = [
        artifact for artifact in record.get("artifacts", [])
        if artifact.get("accessibility", "available") != "available"
    ]
    observed_at_values: set[str] = set()
    for artifact in artifacts:
        value = artifact.get("observed_at")
        if not isinstance(value, str) or not value.strip():
            continue
        normalized = value.strip()
        try:
            parsed = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
        except ValueError:
            continue
        if parsed.tzinfo is not None and parsed.utcoffset() is not None:
            observed_at_values.add(normalized)
    observed_at = sorted(observed_at_values)
    if not observed_at:
        return (
            "A data da última leitura da versão considerada não está registrada; "
            "atualizações posteriores não foram verificadas nem consideradas nesta resposta."
        )
    if len(observed_at) == 1:
        when = observed_at[0]
    else:
        when = ", ".join(observed_at)
    return (
        f"A última leitura da versão considerada foi em {when}; atualizações posteriores "
        "não foram verificadas nem estão refletidas nesta resposta."
    )


def _result_envelope(
    record: dict,
    request: dict,
    *,
    relevance: float,
    chunks: list[dict],
    artifact_accessible: bool,
    record_readable: bool,
) -> dict:
    requested = request["requested_disclosure"]
    explicit = request.get("explicit_expansion_authorization", False)
    limits = _limits(
        record,
        artifact_accessible=artifact_accessible,
        record_readable=record_readable,
    )
    disposition = "accepted"
    returned = requested
    if not record_readable:
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
    elif not artifact_accessible:
        disposition = "partial"

    source = record.get("source", {})
    envelope = {
        "record_ref": record["record_id"],
        "relevance": relevance,
        "authority": record.get("authority_state", "unknown"),
        "privacy": (
            "blocked"
            if record.get("privacy") == "blocked" or record.get("visibility") == "restricted"
            else "redacted" if record.get("privacy") == "redacted" else "allowed"
        ),
        "epistemic_status": record.get("epistemic_status", "unknown"),
        "interpretation_status": (
            "needs_review"
            if record.get("epistemic_status") in {"unresolved-conflict", "conflicting"}
            else "not_assessed"
        ),
        "disclosure_level": returned,
        "evidence": [source.get("source_id", "source-unavailable")],
        "limits": sorted(set(limits)),
        "retrieval_path": f"record:{record['record_id']}" if returned == "L0" else f"record:{record['record_id']}/bounded",
        "mutation": "none",
        "disposition": disposition,
    }
    freshness_note = _artifact_freshness_note(record, artifact_accessible=artifact_accessible)
    if freshness_note:
        envelope["freshness_note"] = freshness_note
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
        presentation_limits = [
            item.get("freshness_note", "A atualidade da versão representada não foi verificada.")
            if limit == "artifact_access_unavailable" else limit
            for limit in item["limits"]
        ]
        limit_text = "; ".join(presentation_limits) if presentation_limits else "sem limitações adicionais identificadas"
        evidence_text = ", ".join(item.get("evidence", [])) or "origem não registrada"
        interpretation_note = (
            " A interpretação permanece pendente de revisão; nenhuma conclusão foi consolidada."
            if item.get("interpretation_status") == "needs_review" else ""
        )
        parts.append(
            f"Encontrei {item['record_ref']} com relevância {item['relevance']:.3f}; "
            f"origem: {evidence_text}; "
            f"a autoridade está {item['authority']}, a divulgação ficou em {item['disclosure_level']} "
            f"e o limite observado é {limit_text}.{interpretation_note}"
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
        artifact_accessible = _artifact_accessible(snapshot)
        record_readable = True
        try:
            read = crud.apply({
                "operation": "read",
                "record_id": record_id,
                "actor": {"authorized_vault_ids": validated["authorized_vault_ids"]},
            })
            record = read["record"]
        except ContractError as exc:
            record_readable = False
            record = deepcopy(snapshot)
            record["read_error"] = str(exc)
        envelopes.append(_result_envelope(
            record,
            validated,
            relevance=relevance,
            chunks=_matching_chunks(record, terms),
            artifact_accessible=artifact_accessible,
            record_readable=record_readable,
        ))
    envelopes.sort(key=lambda item: (-item["relevance"], item["record_ref"]))
    if any(item["disposition"] == "blocked" for item in envelopes):
        disposition = "blocked"
    elif any(item["disposition"] == "partial" for item in envelopes):
        disposition = "partial"
    else:
        disposition = "accepted" if envelopes else "partial"
    returned_level = min((LEVEL_RANK[item["disclosure_level"]] for item in envelopes), default=0)
    interpretation_status = (
        "needs_review"
        if any(item["interpretation_status"] == "needs_review" for item in envelopes)
        else "not_assessed"
    )
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
        "interpretation_status": interpretation_status,
        "presentation": presentation,
        "results": deepcopy(envelopes),
        "trail": trail,
        "mutation": "none",
    }
