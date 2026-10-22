#!/usr/bin/env python3
"""Exercise target-scoped access, classification and profile eligibility rules."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys

import yaml
from v3_access_runtime import diagnose, discover_without_anchor, initial_representative, read_eligibility, write_eligibility
from v3_ingress_engine import IngressError, read_findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    data = yaml.safe_load((root / "docs" / "access-ingress-fixtures.yaml").read_text(encoding="utf-8"))
    fixtures = {fixture["id"]: fixture for fixture in data["fixtures"]}
    errors = []
    vault = {"vault_id": "vault-a", "entity": "entity-a", "repository": "https://github.com/org/entity-vault.git"}
    for fixture in data["fixtures"]:
        ident, expected = fixture["id"], fixture["expected"]
        if ident.startswith("internal-read") or ident.startswith("no-target") or ident.startswith("restricted") or ident.startswith("mixed-content"):
            result = read_eligibility(target=fixture["target"], repo_read=fixture["repo_read"], vault=vault,
                                      classification=fixture["classification"], secure_filtering=fixture.get("secure_filtering", False),
                                      host_proof_verifier=lambda proof: proof.get("signature") == "fixture-verified")
            actual = result["reason"]
        elif ident in {"caller-dict-without-authenticated-host-binding", "filtering-capability-not-proven-by-default"}:
            result = read_eligibility(target=fixture["target"], repo_read=fixture["repo_read"], vault=vault,
                classification=fixture["classification"], secure_filtering=fixture.get("secure_filtering", False),
                host_proof_verifier=lambda proof: proof.get("signature") == "fixture-verified")
            actual = result["reason"]
        elif ident.startswith("entity-") or ident.startswith("personal-"):
            target = "org/entity-vault"
            operation = fixture["operation"]
            proof = {"status": "allow", "target": target, "operation": "read", "authenticated": True,
                "host": "github", "account_id": "acct-1", "session_id": "session-1",
                "proof_source": "authenticated-host-read", "nonce": "read-nonce", "head_sha": "abc123",
                "evidence": "observed-read", "observed_at": "2026-10-21T12:00:00Z", "signature": "host-verified"}
            repo_write = {"status": "allow", "target": target, "operation": operation, "authenticated": True,
                "host": "github", "account_id": "acct-1", "session_id": "session-1",
                "proof_source": "authenticated-host-write", "nonce": "write-nonce", "head_sha": "abc123",
                "evidence": "observed-write", "observed_at": "2026-10-21T12:00:00Z", "signature": "host-verified"}
            if fixture.get("provider_write_spoofed"):
                repo_write = {"status": "allow", "target": target, "operation": operation, "evidence": "caller-claimed"}
            if ident == "personal-read-only-is-eligible-not-executable":
                repo_write = {"status": "unknown", "target": target, "operation": operation}
            grant = None
            if fixture.get("grant_present"):
                grant = {"vault_id": fixture.get("grant_vault_id", "vault-a"), "entity": "entity-a",
                    "account_id": fixture.get("grant_account_id", "acct-1"), "scope": fixture.get("grant_scope", "scope-a"),
                    "actions": [operation], "valid_from": "2026-01-01T00:00:00Z"}
                if not fixture.get("grant_omit_valid_until"):
                    grant["valid_until"] = fixture.get("grant_valid_until", "2027-01-01T00:00:00Z")
                if ident == "entity-grant-current-and-technical-pass":
                    canonical_fields = {"vault_id", "entity", "account_id", "scope", "actions", "valid_from", "valid_until"}
                    if set(grant) != canonical_fields or any(key in grant for key in ("status", "target", "scopes", "revoked_at")):
                        errors.append("fixture grant did not match the scaffold manifest schema")
            result = write_eligibility(profile=fixture["profile"], operation=operation, target=target,
                vault_id="vault-a", entity="entity-a", scope="scope-a", actor_account_id="acct-1", actor_session_id="session-1",
                repo_read=proof, repo_write=repo_write, grant=grant,
                host_proof_verifier=lambda item: item.get("signature") == "host-verified",
                grant_state_verifier=((lambda item, context: fixture.get("grant_state_current", True)
                    and context.get("target") == fixture.get("grant_state_target", target)
                    and context.get("vault_id") == "vault-a" and context.get("account_id") == "acct-1")
                    if fixture.get("grant_verifier_available", True) else None),
                mcp_available=fixture.get("mcp_available", False), crud_available=fixture.get("crud_available", False),
                now=datetime(2026, 10, 21, 12, tzinfo=timezone.utc))
            actual = result["reason"]
        elif ident.startswith("new-vault"):
            result = initial_representative(target="org/new-vault", vault_id="vault-new", entity="entity-a", actor_account_id=fixture["actor_account_id"],
                human_creator_confirmed=True, account_observed=True, scope="operator-confirmed-scope",
                recorded_at="2026-10-21T12:00:00Z", basis="explicit-creation-authorization")
            actual = result["scope"]
            event = result.get("event", {})
            required_event = {"event_id", "event_type", "actor_account_id", "subject_account_id", "vault_id", "entity",
                "actions", "scope", "occurred_at", "commit_ref", "basis"}
            if result.get("status") != "proposed_not_persisted" or event.get("vault_id") != "vault-new" or not required_event.issubset(event) or event.get("event_type") != "granted":
                errors.append("initial representative was presented as persisted or omitted immutable vault ID")
            if (event.get("scope") != "operator-confirmed-scope" or event.get("commit_ref") is not None
                    or result.get("manifest_grant", {}).get("valid_until", "missing") is not None):
                errors.append("initial representative proposal did not follow canonical event/manifest scope fields")
        elif ident.startswith("no-anchor"):
            result = discover_without_anchor(explicit_target=None, candidates=fixture.get("candidates", []))
            actual = ("target_revalidation_required" if result["candidates"] else "absence_not_proven")
        elif ident == "operation-layer-diagnostic":
            obs = {"status": "allow", "target": "org/entity-vault", "operation": "read", "evidence": "observed", "observed_at": "2026-10-21T12:00:00Z"}
            result = diagnose(operation="read", target="org/entity-vault", method_policy=obs, mcp=obs, provider=obs)
            actual = "five_independent_layers" if len(result["layers"]) == 5 and not result["effect_confirmed"] else "invalid"
        elif ident == "ingress-read-findings-verified-context":
            target = "org/entity-vault"
            proof = {"status": "allow", "target": target, "operation": "read", "authenticated": True, "host": "github",
                "account_id": "account-1", "session_id": "session-1", "proof_source": "authenticated-host-read",
                "nonce": "nonce-1", "head_sha": "abc123", "evidence": "observed-read",
                "observed_at": "2026-10-21T12:00:00Z", "signature": "fixture-verified"}
            context = read_eligibility(target=target, repo_read=proof, secure_filtering=True,
                host_proof_verifier=lambda item: item.get("signature") == "fixture-verified",
                vault={"repository": target, "vault_id": "vault-a", "entity": "entity-a"}, classification="internal")["context"]
            checker = lambda _: {"repo_read": {**proof, "nonce": "nonce-2"}, "secure_filtering": True,
                "vault": {"repository": target, "vault_id": "vault-a", "entity": "entity-a"}}
            result = read_findings(record={"destination_vault_id": "vault-a", "entity": "entity-a", "semantic_findings": ["review"]},
                verified_read_context=context, read_context_checker=checker,
                host_proof_verifier=lambda item: item.get("signature") == "fixture-verified")
            actual = "read_only_findings" if result.get("write_performed") is False else "invalid"
            try:
                read_findings(record={"destination_vault_id": "vault-b", "entity": "entity-a"}, verified_read_context=context,
                    read_context_checker=checker, host_proof_verifier=lambda item: item.get("signature") == "fixture-verified")
                errors.append("ingress accepted verified read context for a different vault")
            except IngressError:
                pass
            try:
                read_findings(record={"destination_vault_id": "vault-a", "entity": "entity-a"}, verified_read_context=context,
                    read_context_checker=lambda _: {"repo_read": proof, "secure_filtering": True,
                        "vault": {"repository": target, "vault_id": "vault-a", "entity": "entity-a"}},
                    host_proof_verifier=lambda item: item.get("signature") == "fixture-verified")
                errors.append("ingress accepted a replayed read proof with the old nonce")
            except IngressError:
                pass
            try:
                read_findings(record={"destination_vault_id": "vault-a", "entity": "entity-a"}, verified_read_context=context,
                    read_context_checker=lambda _: {"repo_read": {**proof, "status": "deny"}, "secure_filtering": True,
                        "vault": {"repository": target, "vault_id": "vault-a", "entity": "entity-a"}},
                    host_proof_verifier=lambda item: item.get("signature") == "fixture-verified")
                errors.append("ingress accepted findings after a fresh host recheck reported revocation")
            except IngressError:
                pass
        else:
            actual = "unhandled"
        if actual != expected:
            errors.append(f"{ident}: expected {expected}, got {actual}")

    # Unknown classification fails closed; mismatched target evidence cannot be reused.
    mismatch = read_eligibility(target="org/entity-vault", repo_read={"status": "allow", "target": "org/other", "operation": "read", "evidence": "old", "observed_at": "t"}, secure_filtering=True, host_proof_verifier=lambda _: True, vault=vault, classification="internal")
    if mismatch["reason"] != "target_read_access_unproven":
        errors.append("target-mismatched read proof was reused")
    wrong_host_manifest = read_eligibility(target="org/entity-vault", repo_read={"status": "allow", "target": "org/entity-vault", "operation": "read", "authenticated": True,
        "host": "github", "account_id": "a", "session_id": "s", "proof_source": "host", "nonce": "n", "head_sha": "sha", "evidence": "proof", "observed_at": "t"}, secure_filtering=True,
        host_proof_verifier=lambda _: True, vault={"vault_id": "vault-a", "entity": "entity-a", "repository": "https://github.evil.example/org/entity-vault"},
        classification="internal")
    if wrong_host_manifest["reason"] != "manifest_context_unavailable":
        errors.append("non-GitHub manifest URL was accepted as the proven repository")
    unknown = read_eligibility(target="org/entity-vault", repo_read={"status": "allow", "target": "org/entity-vault", "operation": "read", "authenticated": True, "host": "github", "account_id": "a", "session_id": "s", "proof_source": "host", "nonce": "n", "head_sha": "sha", "evidence": "observed", "observed_at": "t"}, secure_filtering=True, host_proof_verifier=lambda _: True, vault=vault, classification="top-secret")
    if unknown["reason"] != "unknown_classification":
        errors.append("unknown classification did not fail closed")
    structured_claim = {"status": "allow", "target": "org/entity-vault", "operation": "read", "authenticated": True,
        "host": "github", "account_id": "a", "session_id": "s", "proof_source": "host", "nonce": "n",
        "head_sha": "sha", "evidence": "caller-claim", "observed_at": "2026-10-21T12:00:00Z", "signature": "fixture-verified"}
    if read_eligibility(target="org/entity-vault", repo_read=structured_claim, secure_filtering=True,
                        vault=vault, classification="internal")["eligible"]:
        errors.append("caller-supplied structured proof minted context without host verifier")
    # Compatible V3 manifests may lack vault_id. Only authenticated manifest and
    # registry metadata from the same remote HEAD may supply that context.
    legacy_vault = {"repository": "https://github.com/org/entity-vault", "entity": "entity-a"}
    legacy_registry = {"schema": "hipocampo-v3-collection-registry/v1", "vault_id": "vault-a", "entity": "entity-a"}
    metadata_proof = {"status": "allow", "authenticated": True,
        "target": "org/entity-vault", "head_sha": "sha",
        "account_id": "a", "session_id": "s", "manifest_path": "hipocampo.yaml",
        "registry_path": "meta/v3-collections.json", "manifest_blob_sha": "manifest-blob",
        "registry_blob_sha": "registry-blob", "signature": "metadata-fixture-verified"}
    metadata_verifier = lambda proof, manifest, registry: (proof.get("signature") == "metadata-fixture-verified"
        and manifest == legacy_vault and registry == legacy_registry)
    legacy_kwargs = {"target": "org/entity-vault", "repo_read": structured_claim,
        "vault": legacy_vault, "classification": "internal", "secure_filtering": True,
        "host_proof_verifier": lambda proof: proof.get("signature") == "fixture-verified",
        "legacy_registry": legacy_registry, "metadata_proof": metadata_proof,
        "metadata_proof_verifier": metadata_verifier}
    resolved = read_eligibility(**legacy_kwargs)
    if (not resolved.get("eligible") or resolved.get("context", {}).get("vault_id") != "vault-a"
            or resolved.get("context", {}).get("context_source") != "same_head_registry"
            or resolved.get("warning") != "legacy_manifest_vault_id_missing"):
        errors.append("verified same-HEAD legacy registry did not resolve vault identity")
    for label, override in (
        ("missing metadata verifier", {"metadata_proof_verifier": None}),
        ("unauthenticated metadata", {"metadata_proof": {**metadata_proof, "authenticated": False}}),
        ("different HEAD", {"metadata_proof": {**metadata_proof, "head_sha": "other"}}),
        ("different account", {"metadata_proof": {**metadata_proof, "account_id": "other"}}),
        ("different entity", {"legacy_registry": {**legacy_registry, "entity": "other"}}),
        ("untrusted registry", {"metadata_proof": {**metadata_proof, "signature": "untrusted"}}),
    ):
        if read_eligibility(**{**legacy_kwargs, **override}).get("reason") != "manifest_context_unavailable":
            errors.append(f"legacy registry accepted {label}")
    if resolved.get("eligible"):
        fresh_proof = {**structured_claim, "nonce": "next-nonce"}
        fresh_metadata = {**metadata_proof}
        findings = read_findings(record={"destination_vault_id": "vault-a", "entity": "entity-a"},
            verified_read_context=resolved["context"],
            read_context_checker=lambda _: {"repo_read": fresh_proof, "vault": legacy_vault,
                "legacy_registry": legacy_registry, "metadata_proof": fresh_metadata,
                "secure_filtering": True},
            host_proof_verifier=legacy_kwargs["host_proof_verifier"],
            metadata_proof_verifier=metadata_verifier)
        if findings.get("write_performed") is not False:
            errors.append("legacy registry context did not preserve READ-only findings")
    unrelated = diagnose(operation="read", target="org/entity-vault", method_policy={"status": "allow", "target": "org/entity-vault", "operation": "read", "evidence": "m", "observed_at": "t"},
                         mcp={"status": "allow", "target": "org/other", "operation": "read", "evidence": "other-target", "observed_at": "t"},
                         provider={"status": "allow", "target": "org/entity-vault", "operation": "read", "evidence": "p", "observed_at": "t"})
    if unrelated["layers"]["mcp_capability"]["status"] != "unknown" or unrelated["preconditions_satisfied"]:
        errors.append("capability evidence from another target was reused")
    try:
        initial_representative(target="org/old-vault", vault_id="vault-old", entity="entity-a", actor_account_id="typed-login", human_creator_confirmed=False, account_observed=False, scope="scope-a")
        errors.append("unverified creator became representative")
    except ValueError:
        pass
    if errors:
        print(f"validate_v3_access_runtime: FAILED ({len(errors)})")
        print("\n".join(f"  [FAIL] {error}" for error in errors))
        return 1
    print(f"validate_v3_access_runtime: OK ({len(fixtures)} fixtures plus fail-closed edge cases)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
