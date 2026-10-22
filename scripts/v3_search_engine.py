#!/usr/bin/env python3
"""Local read-only V3 Search & Progressive Disclosure primitives."""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import re
from collections.abc import Callable

from v3_crud_engine import ContractError, RecordCrud, VISIBILITY_RANK, effective_visibility
from v3_access_runtime import read_eligibility


LEVELS = ("L0", "L1", "L2", "L3", "L4")
LEVEL_RANK = {level: index for index, level in enumerate(LEVELS)}
PRESENTATIONS = {"prose-default", "structured-on-request"}


class SearchContractError(ValueError):
    """Raised when a search request cannot satisfy the read-side contract."""


def _lower_level(left: str, right: str) -> str:
    return LEVELS[min(LEVEL_RANK[left], LEVEL_RANK[right])]


def _validate_request(request: dict) -> dict:
    required = {
        "request_id", "query", "entity", "vault_scope",
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
    for field in ("vault_scope",):
        if not isinstance(request[field], list) or not request[field] or any(not isinstance(item, str) or not item.strip() for item in request[field]):
            raise SearchContractError(f"{field} must be a non-empty list of strings")
    explicit_ids = request.get("authorized_vault_ids", [])
    if not isinstance(explicit_ids, list) or any(not isinstance(item, str) or not item.strip() for item in explicit_ids):
        raise SearchContractError("authorized_vault_ids must be a list of strings when supplied")
    contexts = request.get("verified_read_contexts", [])
    if not isinstance(contexts, list) or any(not isinstance(item, dict) for item in contexts):
        raise SearchContractError("verified_read_contexts must be a list of verified context mappings")
    context_ids = set()
    for context in contexts:
        proof = context.get("proof", {})
        target = context.get("target")
        if (context.get("access_basis") != "observed_target_read" or context.get("entity") != request["entity"]
                or not context.get("vault_id") or context.get("classification") not in {"public", "internal"}
                or not isinstance(target, str) or "/" not in target
                or proof.get("status") != "allow" or proof.get("target") != target or proof.get("operation") != "read"
                or proof.get("authenticated") is not True or not proof.get("host")
                or proof.get("account_id") != context.get("account_id") or not proof.get("session_id")
                or not proof.get("proof_source") or not proof.get("nonce") or not proof.get("head_sha")
                or not proof.get("evidence") or not proof.get("observed_at")):
            raise SearchContractError("verified read context lacks exact-target observed GitHub read proof")
        context_ids.add(context["vault_id"])
    if not explicit_ids and not context_ids:
        raise SearchContractError("search requires explicit authorized_vault_ids or verified_read_contexts")
    if not set(request["vault_scope"]).issubset(set(explicit_ids) | context_ids):
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


def _verified_context_for(record: dict, contexts: list[dict], entity: str) -> dict | None:
    vault_id = record.get("vault", {}).get("vault_id")
    return next((item for item in contexts if item.get("vault_id") == vault_id and item.get("entity") == entity), None)


def _terms(query: str) -> list[str]:
    return re.findall(r"[\w-]+", query.casefold())


def _chunk_content_allowed(record: dict, chunk: dict) -> bool:
    """Keep a more-restricted Chunk out of ranking and all disclosure levels."""
    return (
        effective_visibility([record, chunk]) != "restricted"
        and chunk.get("privacy") not in {"blocked", "restricted"}
    )


def _within_clearance(record: dict, chunk: dict, clearance: str | None) -> bool:
    if clearance is None:
        return True
    visibility = effective_visibility([record, chunk])
    rank = VISIBILITY_RANK.get(visibility)
    return rank is not None and rank <= VISIBILITY_RANK[clearance]


def _record_text(record: dict, clearance: str | None = None) -> str:
    parts = [str(record.get("title", "")), str(record.get("text", ""))]
    for chunk in record.get("chunks", []):
        if not _chunk_content_allowed(record, chunk) or not _within_clearance(record, chunk, clearance):
            continue
        parts.extend([str(chunk.get("text_ref", "")), str(chunk.get("text", ""))])
    return " ".join(parts).casefold()


def _relevance(record: dict, terms: list[str], clearance: str | None = None) -> float:
    haystack = _record_text(record, clearance)
    if not terms:
        return 0.0
    return round(sum(term in haystack for term in set(terms)) / len(set(terms)), 3)


def _matching_chunks(record: dict, terms: list[str], clearance: str | None = None) -> list[dict]:
    return [
        deepcopy(chunk)
        for chunk in record.get("chunks", [])
        if _chunk_content_allowed(record, chunk)
        and _within_clearance(record, chunk, clearance)
        and any(term in str(chunk.get("text", "")).casefold() for term in terms)
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
    visibility_clearance: str | None = None,
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
            if _chunk_content_allowed(record, chunk) and _within_clearance(record, chunk, visibility_clearance)
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


def search(crud: RecordCrud, request: dict, *,
           read_context_checker: Callable[[dict], dict | None] | None = None,
           host_proof_verifier: Callable[[dict], bool] | None = None) -> dict:
    """Run a local read-only search through the canonical CRUD read boundary."""
    if not isinstance(crud, RecordCrud):
        raise SearchContractError("search requires the canonical RecordCrud gateway")
    validated = _validate_request(request)
    if validated.get("verified_read_contexts"):
        if read_context_checker is None or host_proof_verifier is None:
            raise SearchContractError("verified Search context requires fresh authenticated host recheck and proof verifier")
        refreshed = []
        for hint in validated["verified_read_contexts"]:
            try:
                current = read_context_checker(deepcopy(hint))
            except Exception as exc:
                raise SearchContractError("GitHub read recheck failed; Search is blocked") from exc
            if not isinstance(current, dict):
                raise SearchContractError("GitHub read access was not freshly revalidated for this Search")
            target = hint["target"]
            current_proof = current.get("repo_read", {})
            if current_proof.get("nonce") == hint.get("proof", {}).get("nonce"):
                raise SearchContractError("GitHub read recheck reused a prior nonce; Search is blocked")
            eligibility = read_eligibility(
                target=target, repo_read=current_proof, vault=current.get("vault", {}),
                classification=hint["classification"], secure_filtering=current.get("secure_filtering") is True,
                host_proof_verifier=host_proof_verifier)
            context = eligibility.get("context")
            if (not eligibility.get("eligible") or not isinstance(context, dict)
                    or context.get("vault_id") != hint.get("vault_id")
                    or context.get("entity") != hint.get("entity")
                    or context.get("target") != target
                    or context.get("account_id") != hint.get("account_id")):
                raise SearchContractError("fresh GitHub read proof did not authorize this Search target")
            refreshed.append(context)
        validated["verified_read_contexts"] = refreshed
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
        verified_context = _verified_context_for(snapshot, validated.get("verified_read_contexts", []), validated["entity"])
        if verified_context is not None:
            # Apply the verified context's classification cap before ranking, so
            # even hit presence, titles and snippets cannot reveal higher classes.
            visibility = effective_visibility([snapshot])
            rank = VISIBILITY_RANK.get(visibility)
            clearance = VISIBILITY_RANK[verified_context["classification"]]
            if rank is None or rank > clearance or snapshot.get("privacy") == "blocked":
                continue
        clearance = verified_context["classification"] if verified_context is not None else None
        relevance = _relevance(snapshot, terms, clearance)
        if relevance <= 0:
            continue
        artifact_accessible = _artifact_accessible(snapshot)
        record_readable = True
        try:
            vault_id = snapshot.get("vault", {}).get("vault_id")
            if vault_id in validated.get("authorized_vault_ids", []):
                actor = {"authorized_vault_ids": validated["authorized_vault_ids"]}
            else:
                actor = {"authorized_vault_ids": [vault_id]}
            read = crud.apply({
                "operation": "read",
                "record_id": record_id,
                "actor": actor,
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
            chunks=_matching_chunks(record, terms, clearance),
            artifact_accessible=artifact_accessible,
            record_readable=record_readable,
            visibility_clearance=clearance,
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
        "retrieval_path": "verified-github-read-context+local-crud-read" if validated.get("verified_read_contexts") else "explicit-authorized-local-crud-read",
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
