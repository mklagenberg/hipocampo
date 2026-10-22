#!/usr/bin/env python3
"""Target-scoped access, ingress, presentation and profile eligibility rules."""
from __future__ import annotations
from collections.abc import Callable
from datetime import datetime, timezone
import hashlib
import re
from urllib.parse import urlsplit

VISIBILITY = {"public": 0, "internal": 1, "confidential": 2, "restricted": 3}
OPERATIONS = {"read", "search", "create", "update", "archive", "branch", "commit", "push", "pull", "PR", "merge"}


def _repository_identity(value: object) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if "://" in text:
        try:
            parsed = urlsplit(text)
            port = parsed.port
        except ValueError:
            return None
        if parsed.scheme != "https" or parsed.hostname != "github.com" or port or parsed.username or parsed.password or parsed.query or parsed.fragment:
            return None
        path = parsed.path.strip("/")
        if path.endswith(".git"):
            path = path[:-4]
        text = path
    parts = text.split("/")
    if len(parts) != 2 or any(not re.fullmatch(r"[A-Za-z0-9_.-]+", part) for part in parts):
        return None
    return f"{parts[0]}/{parts[1]}"


def diagnose(*, operation: str, target: str, method_policy: dict, mcp: dict,
             provider: dict, attempt: dict | None = None, effect: dict | None = None) -> dict:
    """Return independent evidence layers; declarations never imply effects."""
    if operation not in OPERATIONS or not target or "/" not in target:
        raise ValueError("exact owner/repo target and supported operation required")
    layers = {
        "method_policy": _layer(method_policy, target, operation),
        "mcp_capability": _layer(mcp, target, operation),
        "provider_permission": _layer(provider, target, operation),
        "attempt": _layer(attempt or {}, target, operation, absent="unknown"),
        "confirmed_effect": _layer(effect or {}, target, operation, absent="unknown"),
    }
    # Provider proof and capability are independent; this does not authorize an attempt.
    eligible = all(layers[name]["status"] == "allow" for name in ("method_policy", "mcp_capability", "provider_permission"))
    return {"target": target, "operation": operation, "layers": layers,
            "preconditions_satisfied": eligible,
            "effect_confirmed": layers["confirmed_effect"]["status"] == "allow"}


def _layer(evidence: dict, target: str, operation: str, absent: str = "unknown") -> dict:
    status = evidence.get("status", absent)
    if status not in {"allow", "deny", "unknown"}:
        status = "unknown"
    if evidence.get("target") != target or evidence.get("operation") != operation:
        status = "unknown"
    if status == "allow" and (not evidence.get("evidence") or not evidence.get("observed_at")):
        status = "unknown"
    return {"status": status, "target": target, "operation": operation,
            "evidence": evidence.get("evidence") if status != "unknown" else None,
            "observed_at": evidence.get("observed_at") if status != "unknown" else None}


def read_eligibility(*, target: str, repo_read: dict, vault: dict, classification: str,
                     secure_filtering: bool = False,
                     host_proof_verifier: Callable[[dict], bool] | None = None,
                     legacy_registry: dict | None = None,
                     metadata_proof: dict | None = None,
                     metadata_proof_verifier: Callable[[dict, dict, dict], bool] | None = None) -> dict:
    """Derive context only from host-authenticated, operation-fresh proof.

    The verifier is the trust boundary: adapters must bind this payload to their
    authenticated session and recheck current repository access immediately
    before calling this function. A caller-provided mapping alone is not proof.
    """
    proof_fields = ("host", "account_id", "session_id", "proof_source", "nonce", "head_sha", "evidence", "observed_at")
    proof_complete = all(isinstance(repo_read.get(key), str) and repo_read.get(key).strip() for key in proof_fields)
    verified = False
    if host_proof_verifier is not None and proof_complete:
        try:
            verified = host_proof_verifier(repo_read) is True
        except Exception:
            verified = False
    if (not target or repo_read.get("target") != target or repo_read.get("operation") != "read"
            or repo_read.get("status") != "allow" or repo_read.get("authenticated") is not True
            or not proof_complete or not verified):
        return {"eligible": False, "reason": "target_read_access_unproven", "content": None}
    if (not isinstance(vault, dict) or not vault.get("entity")
            or _repository_identity(vault.get("repository")) != target):
        return {"eligible": False, "reason": "manifest_context_unavailable", "content": None}
    vault_id = vault.get("vault_id")
    context_source = "manifest"
    if not vault_id:
        proof = metadata_proof if isinstance(metadata_proof, dict) else {}
        registry = legacy_registry if isinstance(legacy_registry, dict) else {}
        same_head = (proof.get("status") == "allow" and proof.get("authenticated") is True
            and proof.get("target") == target
            and proof.get("head_sha") == repo_read.get("head_sha")
            and proof.get("account_id") == repo_read.get("account_id")
            and proof.get("session_id") == repo_read.get("session_id")
            and proof.get("manifest_path") == "hipocampo.yaml"
            and proof.get("registry_path") == "meta/v3-collections.json"
            and proof.get("manifest_blob_sha") and proof.get("registry_blob_sha")
            and registry.get("schema") == "hipocampo-v3-collection-registry/v1"
            and registry.get("entity") == vault.get("entity")
            and isinstance(registry.get("vault_id"), str) and registry["vault_id"].strip())
        metadata_verified = False
        if same_head and metadata_proof_verifier is not None:
            try:
                metadata_verified = metadata_proof_verifier(proof, vault, registry) is True
            except Exception:
                metadata_verified = False
        if not metadata_verified:
            return {"eligible": False, "reason": "manifest_context_unavailable", "content": None}
        vault_id = registry["vault_id"]
        context_source = "same_head_registry"
    rank = VISIBILITY.get(classification)
    if rank is None:
        return {"eligible": False, "reason": "unknown_classification", "content": None}
    if rank > VISIBILITY["internal"]:
        return {"eligible": False, "reason": "clearance_required", "content": None}
    if not secure_filtering:
        return {"eligible": False, "reason": "host_cannot_filter_safely", "content": None}
    return {"eligible": True, "reason": "proven_repository_read", "context": {
        "target": target, "vault_id": vault_id, "entity": vault["entity"],
        "access_basis": "observed_target_read", "classification": classification,
        "account_id": repo_read["account_id"], "proof": dict(repo_read),
        "context_source": context_source},
        **({"warning": "legacy_manifest_vault_id_missing"} if context_source == "same_head_registry" else {})}


def _verified_provider_proof(proof: dict, *, target: str, operation: str, account_id: str,
                             session_id: str, verifier: Callable[[dict], bool] | None) -> bool:
    required = ("host", "proof_source", "nonce", "head_sha", "evidence", "observed_at")
    if (proof.get("status") != "allow" or proof.get("target") != target or proof.get("operation") != operation
            or proof.get("authenticated") is not True or proof.get("account_id") != account_id
            or proof.get("session_id") != session_id
            or any(not isinstance(proof.get(field), str) or not proof[field].strip() for field in required)
            or verifier is None):
        return False
    try:
        return verifier(proof) is True
    except Exception:
        return False


def _instant(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.astimezone(timezone.utc) if parsed.tzinfo is not None else None
    except (ValueError, OverflowError):
        return None


def write_eligibility(*, profile: str, operation: str, repo_read: dict, repo_write: dict,
                      target: str, vault_id: str, entity: str, scope: str,
                      actor_account_id: str, actor_session_id: str,
                      grant: dict | None = None,
                      host_proof_verifier: Callable[[dict], bool] | None = None,
                      grant_state_verifier: Callable[[dict, dict], bool] | None = None,
                      mcp_available: bool = False, crud_available: bool = False,
                      now: datetime | None = None) -> dict:
    """Separate current method eligibility from provider/MCP/CRUD executability.

    Host and grant verifiers are trusted adapter callbacks. Caller-provided
    status mappings alone cannot establish permission or current grant state.
    """
    if operation not in {"create", "update", "archive"}:
        return {"policy_eligible": False, "eligible": False, "technical_executable": False, "executable": False, "reason": "unsupported_governed_write"}
    if not target or not vault_id or not entity or not scope or not actor_account_id or not actor_session_id:
        return {"policy_eligible": False, "eligible": False, "technical_executable": False, "executable": False, "reason": "write_context_incomplete"}
    if not _verified_provider_proof(repo_read, target=target, operation="read", account_id=actor_account_id,
                                    session_id=actor_session_id, verifier=host_proof_verifier):
        return {"policy_eligible": False, "eligible": False, "technical_executable": False, "executable": False, "reason": "target_read_access_unproven"}
    if profile in {"personal", "team"}:
        method = True
    elif profile == "entity":
        current = now or datetime.now(timezone.utc)
        if current.tzinfo is None:
            return {"policy_eligible": False, "eligible": False, "technical_executable": False, "executable": False, "reason": "evaluation_time_invalid"}
        start = _instant(grant.get("valid_from")) if isinstance(grant, dict) else None
        end = _instant(grant.get("valid_until")) if isinstance(grant, dict) else None
        expiry_declared = isinstance(grant, dict) and "valid_until" in grant
        expiry_valid = bool(expiry_declared and (grant.get("valid_until") is None or end is not None and current.astimezone(timezone.utc) < end))
        grant_shape_valid = bool(grant and grant.get("vault_id") == vault_id and grant.get("entity") == entity
            and grant.get("account_id") == actor_account_id
            and grant.get("scope") == scope
            and operation in grant.get("actions", [])
            and start is not None and expiry_valid and start <= current.astimezone(timezone.utc))
        grant_current = False
        if grant_shape_valid and grant_state_verifier is not None:
            try:
                grant_current = grant_state_verifier(grant, {"target": target, "vault_id": vault_id,
                    "entity": entity, "account_id": actor_account_id, "scope": scope,
                    "operation": operation, "evaluated_at": current.astimezone(timezone.utc).isoformat()}) is True
            except Exception:
                grant_current = False
        method = grant_shape_valid and grant_current
    else:
        return {"policy_eligible": False, "eligible": False, "technical_executable": False, "executable": False, "reason": "unknown_profile"}
    if not method:
        return {"policy_eligible": False, "eligible": False, "technical_executable": False, "executable": False, "reason": "entity_grant_required_or_not_current"}
    provider_write = _verified_provider_proof(repo_write, target=target, operation=operation,
        account_id=actor_account_id, session_id=actor_session_id, verifier=host_proof_verifier)
    if not provider_write:
        return {"policy_eligible": True, "eligible": True, "technical_executable": False, "executable": False, "reason": "provider_write_unproven"}
    executable = bool(mcp_available and crud_available)
    return {"policy_eligible": True, "eligible": True, "technical_executable": executable, "executable": executable,
            "reason": "method_provider_mcp_and_crud_proven" if executable else "mcp_or_crud_unproven"}


def initial_representative(*, target: str, vault_id: str, entity: str, actor_account_id: str,
                           human_creator_confirmed: bool, account_observed: bool,
                           scope: str, recorded_at: str = "", basis: str = "") -> dict:
    if (not human_creator_confirmed or not account_observed or not actor_account_id or not target or not vault_id
            or not entity or not scope or not _instant(recorded_at) or not basis):
        raise ValueError("new-vault representative requires confirmed human creator bound to observed account")
    event_id = hashlib.sha256(f"{target}\0{vault_id}\0{actor_account_id}\0{recorded_at}".encode("utf-8")).hexdigest()[:24]
    return {"status": "proposed_not_persisted", "target": target, "vault_id": vault_id,
            "entity": entity, "account_id": actor_account_id, "role": "initial_representative",
            "scope": "new_vault_only", "event": {"event_id": event_id, "event_type": "granted",
            "actor_account_id": actor_account_id, "subject_account_id": actor_account_id,
            "vault_id": vault_id, "entity": entity, "scope": scope,
            "actions": ["create", "update", "archive", "manage_representatives"],
            "occurred_at": recorded_at, "commit_ref": None, "basis": basis},
            "manifest_grant": {"account_id": actor_account_id, "vault_id": vault_id, "entity": entity,
            "actions": ["create", "update", "archive", "manage_representatives"], "scope": scope,
            "valid_from": recorded_at, "valid_until": None}}


def discover_without_anchor(*, explicit_target: str | None, candidates: list[str] | None,
                            enumeration_complete: bool = False) -> dict:
    """Discovery suggestions are not permissions; a partial listing proves no absence."""
    supplied = [explicit_target] if explicit_target else []
    suggestions = list(dict.fromkeys(supplied + (candidates or [])))
    return {"anchor_required": False, "candidates": suggestions,
            "inventory_complete": bool(enumeration_complete),
            "absence_proven": bool(enumeration_complete and not suggestions),
            "target_revalidation_required": True}
