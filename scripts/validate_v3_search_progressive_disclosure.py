#!/usr/bin/env python3
"""Validate the deterministic envelope of the unreleased V3 search contract.

This validates contract shape and sanitized fixtures only. It does not prove
relevance, authority, privacy permission or semantic truth.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from v3_crud_engine import ContractError, RecordCrud
from v3_search_engine import SearchContractError, search
from v3_access_runtime import read_eligibility


LEVELS = ["L0", "L1", "L2", "L3", "L4"]
EXPECTED = {
    "reject-unauthorized-expansion": ("blocked", "L0"),
    "preserve-independent-dimensions": ("needs_review", "L2"),
    "prose-default": ("partial", "L2"),
    "structured-only-on-request": ("accepted", "L2"),
    "require-bounded-request-context": ("blocked", "L0"),
    "search-verified-read-without-registry": ("partial", "L2"),
    "block-unauthorized-vault-scope": ("blocked", "L0"),
    "preserve-authorized-expansion": ("accepted", "L4"),
    "preserve-authorized-conflict-at-L4": ("accepted", "L4"),
    "limit-stale-source": ("partial", "L2"),
    "block-restricted-content": ("blocked", "L1"),
    "preserve-record-prose-with-inaccessible-artifact": ("partial", "L3"),
    "block-inaccessible-record-content": ("blocked", "L0"),
    "keep-scope-collision-candidates-separate": ("needs_review", "L2"),
}


def runtime_record(
    record_id: str,
    *,
    text: str,
    staleness: str = "current",
    visibility: str = "internal",
    artifact_accessibility: str = "available",
    artifact_observed_at: str | None = None,
    entity: str = "entity-a",
    vault_id: str = "vault-a",
    scope: str = "scope-a",
) -> dict:
    artifact = {"artifact_id": f"artifact-{record_id}", "role": "supporting", "version": 1, "reference": "sanitized/ref", "visibility": visibility, "accessibility": artifact_accessibility}
    if artifact_observed_at is not None:
        artifact["observed_at"] = artifact_observed_at
    return {
        "record_id": record_id,
        "record_version": 1,
        "physical_path": f"records/{record_id}.md",
        "status": "active",
        "visibility": visibility,
        "staleness": staleness,
        "entity": entity,
        "scope": scope,
        "source": {"source_id": f"source-{record_id}", "source_kind": "conversation", "entity": entity},
        "vault": {"vault_id": vault_id, "entity": entity, "profile": "entity", "role": "anchor"},
        "governance": {"owner": "owner-a", "authority": "authority-a"},
        "maturity": "curated",
        "collection_ids": ["collection-a"],
        "chunks": [{
            "chunk_id": f"{record_id}-chunk-1",
            "parent_record_id": record_id,
            "text_ref": "section-1",
            "text": text,
            "visibility": visibility,
            "staleness": staleness,
        }],
        "artifacts": [artifact],
        "title": "Alpha result",
        "content": f"Prose content for {record_id}: {text}",
        "authority_state": "unknown",
        "epistemic_status": "unresolved-conflict",
    }


def run_runtime_cases(errors: list[str]) -> None:
    class SpyCrud(RecordCrud):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.read_calls = 0

        def apply(self, request: dict) -> dict:
            if request.get("operation") == "read":
                self.read_calls += 1
            return super().apply(request)

    crud = SpyCrud(
        {"collection-a": {"collection_id": "collection-a", "active": True}},
        {"rec-search": runtime_record("rec-search", text="alpha context")},
    )
    base = {
        "request_id": "search-test-001",
        "intent": "find alpha context",
        "query": "alpha",
        "entity": "entity-a",
        "vault_scope": ["vault-a"],
        "authorized_vault_ids": ["vault-a"],
        "knowledge_scope": "scope-a",
        "requested_disclosure": "L2",
    }

    # A target-scoped provider read can supply Search context without an internal
    # vault registry entry. The access result is created by the runtime gate.
    manifest = {"vault_id": "vault-a", "entity": "entity-a", "repository": "org/entity-vault"}
    proof = {"status": "allow", "target": "org/entity-vault", "operation": "read", "authenticated": True,
        "host": "github", "account_id": "account-1", "session_id": "session-1",
        "proof_source": "authenticated-host-read", "nonce": "nonce-fresh-1", "head_sha": "abc123",
        "evidence": "observed-github-read", "observed_at": "2026-10-21T12:00:00Z", "signature": "fixture-verified"}
    verifier = lambda item: item.get("signature") == "fixture-verified"
    access = read_eligibility(target="org/entity-vault", repo_read=proof, vault=manifest, classification="internal",
                              secure_filtering=True, host_proof_verifier=verifier)
    if not access.get("eligible"):
        errors.append("target-scoped observed GitHub read did not produce a Search context")
    else:
        private_records = {
            "rec-internal": runtime_record("rec-internal", text="alpha approved", visibility="internal"),
            "rec-confidential": runtime_record("rec-confidential", text="alpha secret", visibility="confidential"),
        }
        private_records["rec-internal"]["chunks"].append({"chunk_id": "rec-internal-private", "parent_record_id": "rec-internal",
            "text_ref": "private-section", "text": "vault-secret", "visibility": "confidential", "staleness": "current"})
        context_crud = RecordCrud({"collection-a": {"collection_id": "collection-a", "active": True}}, private_records)
        context_request = {key: value for key, value in base.items() if key != "authorized_vault_ids"}
        context_request.update({"request_id": "search-verified-read", "vault_scope": ["vault-a"],
                                "verified_read_contexts": [access["context"]]})
        rechecks = []
        def fresh_checker(context):
            rechecks.append(context["target"])
            return {"repo_read": {**proof, "nonce": f"nonce-fresh-{len(rechecks) + 1}", "observed_at": "2026-10-21T12:01:00Z"},
                    "vault": manifest, "secure_filtering": True}
        try:
            context_result = search(context_crud, context_request, read_context_checker=fresh_checker, host_proof_verifier=verifier)
            refs = [item["record_ref"] for item in context_result["results"]]
            if refs != ["rec-internal"] or context_result["trail"]["retrieval_path"] != "verified-github-read-context+local-crud-read":
                errors.append("verified GitHub read did not enable bounded internal Search or leaked a higher-class result")
            expanded_context = search(context_crud, {**context_request, "request_id": "search-verified-read-expansion",
                "requested_disclosure": "L4", "explicit_expansion_authorization": True},
                read_context_checker=fresh_checker, host_proof_verifier=verifier)
            if any("vault-secret" in str(item) for item in expanded_context["results"]):
                errors.append("verified internal context exposed a confidential Chunk through expansion")
            if len(rechecks) != 2:
                errors.append("Search reused prior host access proof instead of rechecking each operation")
        except SearchContractError as exc:
            errors.append(f"verified GitHub read Search path failed: {exc}")
        try:
            search(context_crud, context_request)
            errors.append("Search trusted a supplied context without fresh host verification")
        except SearchContractError:
            pass
        try:
            search(context_crud, context_request, read_context_checker=lambda _: {"repo_read": proof, "vault": manifest,
                "secure_filtering": True}, host_proof_verifier=verifier)
            errors.append("Search accepted a replayed read proof with the old nonce")
        except SearchContractError:
            pass
        try:
            switched = {**proof, "account_id": "account-2", "nonce": "nonce-switched"}
            search(context_crud, context_request, read_context_checker=lambda _: {"repo_read": switched, "vault": manifest,
                "secure_filtering": True}, host_proof_verifier=verifier)
            errors.append("Search reused access proof after authenticated account changed")
        except SearchContractError:
            pass
        try:
            search(context_crud, context_request, read_context_checker=lambda _: {"repo_read": {**proof, "status": "deny"},
                "vault": manifest, "secure_filtering": True}, host_proof_verifier=verifier)
            errors.append("Search allowed access after the fresh host recheck reported revocation")
        except SearchContractError:
            pass
        try:
            search(context_crud, {**context_request, "verified_read_contexts": [{**access["context"], "proof": {"status": "allow", "target": "org/other", "operation": "read", "authenticated": True, "host": "github", "account_id": "account-1", "session_id": "session-1", "proof_source": "host", "nonce": "n", "head_sha": "sha", "evidence": "wrong", "observed_at": "t"}}]}, read_context_checker=fresh_checker, host_proof_verifier=verifier)
            errors.append("Search accepted a verified read context for another repository")
        except SearchContractError:
            pass
    before = crud.records
    try:
        prose = search(crud, base)
        if prose["presentation"]["mode"] != "prose-default" or "text" not in prose["presentation"]:
            errors.append("runtime default did not render integrated prose")
        if "results" in prose["presentation"]:
            errors.append("runtime default exposed separated result fields")
        if prose["results"][0]["mutation"] != "none":
            errors.append("runtime result did not declare mutation none")
    except SearchContractError as exc:
        errors.append(f"runtime prose case failed: {exc}")

    try:
        partial = search(crud, {**base, "requested_disclosure": "L3"})
        item = partial["results"][0]
        if partial["status"] != "partial" or item["disclosure_level"] != "L2":
            errors.append("L3 request without expansion authorization was not reduced to L2")
        if item["relevance"] <= 0 or item["authority"] != "unknown" or item["epistemic_status"] != "unresolved-conflict":
            errors.append("relevance was not kept independent from authority and epistemic state")
    except SearchContractError as exc:
        errors.append(f"runtime independent-dimensions case failed: {exc}")

    try:
        blocked = search(crud, {**base, "requested_disclosure": "L4"})
        item = blocked["results"][0]
        if blocked["status"] != "blocked" or item["disclosure_level"] != "L0" or "record_envelope" in item:
            errors.append("unauthorized L4 expansion was not blocked at L0")
    except SearchContractError as exc:
        errors.append(f"runtime unauthorized-expansion case failed: {exc}")

    try:
        structured = search(crud, {**base, "presentation": "structured-on-request", "explicit_structured_request": True})
        if structured["presentation"]["mode"] != "structured-on-request" or "results" not in structured["presentation"]:
            errors.append("explicit structured request did not expose separated results")
    except SearchContractError as exc:
        errors.append(f"runtime structured case failed: {exc}")

    for field in ("query", "entity", "vault_scope", "knowledge_scope"):
        malformed = dict(base)
        malformed.pop(field)
        try:
            search(crud, malformed)
            errors.append(f"missing request context was accepted: {field}")
        except SearchContractError:
            pass

    try:
        expanded = search(crud, {**base, "request_id": "search-test-expanded", "requested_disclosure": "L4", "explicit_expansion_authorization": True})
        item = expanded["results"][0]
        if (
            item["disclosure_level"] != "L4"
            or "expanded_content" not in item
            or item["authority"] != "unknown"
            or item["epistemic_status"] != "unresolved-conflict"
        ):
            errors.append("explicitly authorized L4 expansion did not return L4 content")
    except SearchContractError as exc:
        errors.append(f"runtime authorized-expansion case failed: {exc}")

    conflict_records = {
        "rec-conflict-a": runtime_record("rec-conflict-a", text="alpha due September", vault_id="vault-a"),
        "rec-conflict-b": runtime_record("rec-conflict-b", text="alpha due October", vault_id="vault-b"),
    }
    conflict_records["rec-conflict-a"]["source"]["source_id"] = "source-conflict-a"
    conflict_records["rec-conflict-b"]["source"]["source_id"] = "source-conflict-b"
    conflict_crud = RecordCrud(
        {"collection-a": {"collection_id": "collection-a", "active": True}},
        conflict_records,
    )
    conflict_result = search(conflict_crud, {
        **base,
        "request_id": "search-test-authorized-conflict",
        "query": "alpha",
        "vault_scope": ["vault-a", "vault-b"],
        "authorized_vault_ids": ["vault-a", "vault-b"],
        "requested_disclosure": "L4",
        "explicit_expansion_authorization": True,
    })
    conflict_items = conflict_result["results"]
    conflict_prose = conflict_result["presentation"].get("text", "")
    if (
        conflict_result["status"] != "accepted"
        or conflict_result["interpretation_status"] != "needs_review"
        or len(conflict_items) != 2
        or [item["record_ref"] for item in conflict_items] != ["rec-conflict-a", "rec-conflict-b"]
        or any(item["disclosure_level"] != "L4" or "expanded_content" not in item for item in conflict_items)
        or any(item["epistemic_status"] != "unresolved-conflict" or item["interpretation_status"] != "needs_review" for item in conflict_items)
        or [item["evidence"] for item in conflict_items] != [["source-conflict-a"], ["source-conflict-b"]]
        or "source-conflict-a" not in conflict_prose or "source-conflict-b" not in conflict_prose
        or conflict_prose.count("nenhuma conclusão foi consolidada") != 2
    ):
        errors.append("authorized L4 disclosure converted an unresolved source conflict into one accepted conclusion or lost provenance")

    try:
        search(crud, {**base, "request_id": "search-test-unauthorized-vault", "vault_scope": ["vault-b"], "authorized_vault_ids": ["vault-a"]})
        errors.append("unauthorized vault scope was not rejected")
    except SearchContractError:
        pass

    if crud.records != before or crud.events or crud.read_calls != 5:
        errors.append("search did not preserve CRUD state while using the canonical read boundary")

    stale_crud = RecordCrud(
        {"collection-a": {"collection_id": "collection-a", "active": True}},
        {"rec-stale": runtime_record("rec-stale", text="alpha stale", staleness="stale")},
    )
    stale = search(stale_crud, {**base, "request_id": "search-test-stale", "requested_disclosure": "L3"})
    if stale["results"][0]["disclosure_level"] != "L2" or "record_requires_revalidation" not in stale["results"][0]["limits"]:
        errors.append("stale source was not limited and surfaced")

    inaccessible_record = runtime_record(
        "rec-inaccessible",
        text="alpha unavailable",
        artifact_accessibility="unavailable",
        artifact_observed_at="2026-09-20T12:00:00Z",
    )
    inaccessible_crud = RecordCrud(
        {"collection-a": {"collection_id": "collection-a", "active": True}},
        {"rec-inaccessible": inaccessible_record},
    )
    inaccessible = search(inaccessible_crud, {**base, "request_id": "search-test-inaccessible", "requested_disclosure": "L3", "explicit_expansion_authorization": True})
    if (
        inaccessible["status"] != "partial"
        or inaccessible["results"][0]["disclosure_level"] != "L3"
        or "artifact_access_unavailable" not in inaccessible["results"][0]["limits"]
        or "selected_chunks" not in inaccessible["results"][0]
        or "2026-09-20T12:00:00Z" not in inaccessible["presentation"]["text"]
        or "atualizações posteriores" not in inaccessible["presentation"]["text"]
        or "artifact_access_unavailable" in inaccessible["presentation"]["text"]
        or "indisponível" in inaccessible["presentation"]["text"]
    ):
        errors.append("inaccessible Artifact did not preserve Record prose with the bounded observation-date message")

    undated_record = runtime_record(
        "rec-undated-artifact",
        text="alpha undated",
        artifact_accessibility="unavailable",
    )
    undated_crud = RecordCrud(
        {"collection-a": {"collection_id": "collection-a", "active": True}},
        {"rec-undated-artifact": undated_record},
    )
    undated = search(undated_crud, {**base, "request_id": "search-test-undated-artifact", "requested_disclosure": "L3", "explicit_expansion_authorization": True})
    if (
        undated["status"] != "partial"
        or "data da última leitura" not in undated["presentation"]["text"]
        or "indisponível" in undated["presentation"]["text"]
    ):
        errors.append("missing observation date was fabricated or exposed as an availability message")

    malformed_date_record = runtime_record(
        "rec-malformed-date-artifact",
        text="alpha malformed date",
        artifact_accessibility="unavailable",
        artifact_observed_at="not-a-timestamp",
    )
    malformed_date_crud = RecordCrud(
        {"collection-a": {"collection_id": "collection-a", "active": True}},
        {"rec-malformed-date-artifact": malformed_date_record},
    )
    malformed_date = search(malformed_date_crud, {**base, "request_id": "search-test-malformed-date-artifact", "requested_disclosure": "L3", "explicit_expansion_authorization": True})
    if (
        "not-a-timestamp" in malformed_date["presentation"]["text"]
        or "data da última leitura" not in malformed_date["presentation"]["text"]
    ):
        errors.append("malformed observation timestamp was presented as a valid freshness boundary")

    collision_records = {
        "rec-scope-a": runtime_record("rec-scope-a", text="delta shared term alpha", vault_id="vault-a"),
        "rec-scope-b": runtime_record("rec-scope-b", text="delta shared term beta", vault_id="vault-b"),
        "rec-other-entity": runtime_record("rec-other-entity", text="delta shared term outside", entity="entity-b", vault_id="vault-c"),
        "rec-other-scope": runtime_record("rec-other-scope", text="delta shared term outside", vault_id="vault-b", scope="scope-b"),
    }
    collision_crud = RecordCrud(
        {"collection-a": {"collection_id": "collection-a", "active": True}},
        collision_records,
    )
    collision = search(collision_crud, {
        **base,
        "request_id": "search-test-scope-collision",
        "query": "delta",
        "vault_scope": ["vault-a", "vault-b"],
        "authorized_vault_ids": ["vault-a", "vault-b"],
    })
    collision_refs = [item["record_ref"] for item in collision["results"]]
    if (
        collision["status"] != "accepted"
        or collision_refs != ["rec-scope-a", "rec-scope-b"]
        or len(set(collision_refs)) != 2
        or collision["presentation"]["text"].count("Encontrei ") != 2
        or any(item["metadata"]["entity"] != "entity-a" for item in collision["results"])
        or any(item["metadata"]["vault_id"] not in {"vault-a", "vault-b"} for item in collision["results"])
    ):
        errors.append("same-term candidates were merged or crossed declared entity, vault or knowledge scope")

    class DeniedReadCrud(RecordCrud):
        def apply(self, request: dict) -> dict:
            if request.get("operation") == "read":
                raise ContractError("Record content is unavailable to this read")
            return super().apply(request)

    denied_crud = DeniedReadCrud(
        {"collection-a": {"collection_id": "collection-a", "active": True}},
        {"rec-denied": runtime_record("rec-denied", text="alpha denied")},
    )
    denied = search(denied_crud, {**base, "request_id": "search-test-record-denied", "requested_disclosure": "L3"})
    if (
        denied["status"] != "blocked"
        or denied["results"][0]["disclosure_level"] != "L0"
        or "record_content_unavailable" not in denied["results"][0]["limits"]
    ):
        errors.append("unavailable Record content was not blocked at L0")

    restricted_record = runtime_record("rec-restricted", text="alpha restricted", visibility="restricted")
    restricted_crud = RecordCrud(
        {"collection-a": {"collection_id": "collection-a", "active": True}},
        {"rec-restricted": restricted_record},
    )
    restricted = search(restricted_crud, {**base, "request_id": "search-test-restricted", "requested_disclosure": "L3", "explicit_expansion_authorization": True})
    if (
        restricted["status"] != "blocked"
        or restricted["results"][0]["disclosure_level"] != "L1"
        or restricted["results"][0]["privacy"] != "blocked"
    ):
        errors.append("restricted content was not blocked at metadata level")
    if "text" in restricted["trail"] or "secret" in str(restricted["trail"]).casefold():
        errors.append("operational trail exposed content or secret material")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    contract_path = root / "docs/v3-search-progressive-disclosure-contract.md"
    fixture_path = root / "docs/v3-search-progressive-disclosure-fixtures.yaml"
    errors: list[str] = []
    try:
        contract = contract_path.read_text(encoding="utf-8")
        fixtures = yaml.safe_load(fixture_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"validate_v3_search_progressive_disclosure: FAILED — {exc}")
        return 1

    required_sections = (
        "## Request envelope",
        "## Result envelope",
        "## Disclosure levels",
        "## Presentation policy",
        "## Guardrails and semantic boundary",
        "## CRUD and operational trail",
    )
    for section in required_sections:
        if section not in contract:
            errors.append(f"contract is missing {section}")
    for level in LEVELS:
        if f"`{level}`" not in contract:
            errors.append(f"contract does not declare {level}")
    for phrase in ("read-only", "mutation: \"none\"", "explicit authorization", "fail closed"):
        if phrase not in contract:
            errors.append(f"contract is missing guardrail text: {phrase}")

    if not isinstance(fixtures, dict):
        errors.append("fixture root must be a mapping")
        fixtures = {}
    if fixtures.get("schema_version") != "1.0":
        errors.append("fixture schema_version must be 1.0")
    policy = fixtures.get("fixture_policy", {})
    if policy.get("privacy") != "sanitized-no-real-content":
        errors.append("fixtures must declare sanitized-no-real-content")
    if policy.get("mutation") != "none":
        errors.append("fixtures must declare mutation none")
    if fixtures.get("levels") != LEVELS:
        errors.append("fixture levels must be exactly L0 through L4")

    cases = fixtures.get("cases", [])
    seen: set[str] = set()
    for index, case in enumerate(cases if isinstance(cases, list) else []):
        label = f"cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{label} must be a mapping")
            continue
        case_id = case.get("id")
        if case_id in seen:
            errors.append(f"{label} duplicates {case_id}")
        seen.add(case_id)
        if case_id not in EXPECTED:
            errors.append(f"{label} is not an assigned deterministic case")
            continue
        disposition, level = EXPECTED[case_id]
        if case.get("expected_disposition") != disposition:
            errors.append(f"{label} has unexpected disposition")
        if case.get("expected_disclosure_level") != level:
            errors.append(f"{label} has unexpected disclosure level")
        if case.get("mutation") != "none":
            errors.append(f"{label} must not mutate")
        if "content" in case or "record_body" in case:
            errors.append(f"{label} must not contain Record or Chunk body content")
    if seen != set(EXPECTED):
        errors.append(f"fixture case coverage mismatch: expected {sorted(EXPECTED)}, got {sorted(seen)}")
    expansion = next((case for case in cases if case.get("id") == "reject-unauthorized-expansion"), {})
    if expansion.get("requested_disclosure") != "L4" or expansion.get("explicit_expansion_authorization") is not False:
        errors.append("unauthorized expansion case must request L4 without authorization")
    independent = next((case for case in cases if case.get("id") == "preserve-independent-dimensions"), {})
    if independent.get("relevance") != "high" or independent.get("authority") != "unknown" or independent.get("epistemic_status") != "unresolved-conflict":
        errors.append("independent-dimensions case must keep high relevance separate from authority and epistemic state")
    run_runtime_cases(errors)

    if errors:
        print(f"validate_v3_search_progressive_disclosure: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print(f"validate_v3_search_progressive_disclosure: OK — contract envelope and {len(EXPECTED)} sanitized fixtures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
