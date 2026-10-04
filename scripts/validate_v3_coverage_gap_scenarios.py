#!/usr/bin/env python3
"""Execute new synthetic V3 coverage-gap scenarios and validate review envelopes.

Six deterministic scenarios exercise local V3 components or explicit test
adapters. Three semantic scenarios are checked for a complete, human-pending
assessment envelope; this script does not decide semantic truth.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path
from typing import Callable

import yaml

from v3_crud_engine import ContractError, RecordCrud
from v3_migration_engine import evaluate as evaluate_migration
from v3_search_engine import search
from v3_transfer_engine import accept_received
from v3_case_bindings import validate_binding_set


SCENARIO_FILE = "docs/v3-coverage-gap-scenarios.yaml"
REVIEW_FILE = "docs/v3-coverage-gap-semantic-review.yaml"
SEMANTIC_IDS = {
    "SEM-MIGRATION-SCOPE-001",
    "SEM-CROSS-ENGINE-001",
    "SEM-LEARNING-CORRELATED-001",
}


def runtime_record(record_id: str, *, chunks: list[dict] | None = None, text: str = "alpha visible") -> dict:
    return {
        "record_id": record_id,
        "record_version": 1,
        "physical_path": f"records/{record_id}.md",
        "content": f"Synthetic body sentinel for {record_id}",
        "status": "active",
        "visibility": "internal",
        "staleness": "current",
        "entity": "entity-a",
        "scope": "scope-a",
        "source": {"source_id": f"source-{record_id}", "source_kind": "conversation", "entity": "entity-a"},
        "vault": {"vault_id": "vault-a", "entity": "entity-a", "profile": "entity", "role": "anchor"},
        "governance": {"owner": "owner-a", "authority": "authority-a"},
        "maturity": "curated",
        "collection_ids": ["collection-a"],
        "chunks": chunks or [{
            "chunk_id": f"{record_id}-chunk-1", "parent_record_id": record_id,
            "text_ref": "section-1", "text": text, "visibility": "internal", "staleness": "current",
        }],
        "artifacts": [],
        "title": "Synthetic governed result",
        "authority_state": "unknown",
        "epistemic_status": "unresolved-conflict",
    }


def search_request(*, query: str, requested_disclosure: str = "L4") -> dict:
    return {
        "request_id": "coverage-gap-test",
        "intent": "exercise a bounded synthetic read",
        "query": query,
        "entity": "entity-a",
        "vault_scope": ["vault-a"],
        "authorized_vault_ids": ["vault-a"],
        "knowledge_scope": "scope-a",
        "requested_disclosure": requested_disclosure,
        "explicit_expansion_authorization": True,
    }


def check_binding(binding: dict) -> list[str]:
    registry = {
        "DET-BIND-001": ("coverage.binding_rejects_unknown_or_misdirected_case", "v3-coverage-gap-scenarios", "binding_mutation"),
        "DET-SEARCH-REVOCATION-001": ("search.revocation_between_snapshot_and_read_fails_closed", "v3-coverage-gap-scenarios", "authorization_revocation"),
        "DET-SEARCH-CHUNK-001": ("search.restricted_chunk_excluded_from_rank_and_disclosure", "v3-coverage-gap-scenarios", "chunk_effective_restriction"),
        "DET-TRANSFER-RETRY-001": ("transfer.replayed_acceptance_creates_one_record_and_event", "v3-coverage-gap-scenarios", "transfer_retry"),
        "DET-MIGRATION-INTERRUPT-001": ("migration.interrupted_preflight_cannot_be_ready", "v3-coverage-gap-scenarios", "migration_interruption"),
        "DET-SKILL-CAPABILITY-001": ("skill.missing_runtime_capability_stops_without_io", "v3-coverage-gap-scenarios", "missing_skill_capability"),
    }
    case_id = binding.get("id")
    expected = registry.get(case_id)
    if expected is None:
        return [f"unknown deterministic scenario id: {case_id}"]
    errors: list[str] = []
    if binding.get("assertion_id") != expected[0]:
        errors.append(f"{case_id}: assertion_id does not resolve to its executable assertion")
    if binding.get("runner") != expected[1]:
        errors.append(f"{case_id}: runner does not resolve to the V3 coverage-gap executor")
    if binding.get("handler") != expected[2]:
        errors.append(f"{case_id}: handler does not resolve to its executable scenario")
    return errors


def test_binding_mutation(case: dict, root: Path) -> list[str]:
    errors: list[str] = []
    if check_binding(case):
        errors.append("valid binding was rejected")
    unknown = {**case, "assertion_id": "coverage.unknown_assertion"}
    wrong_handler = {**case, "handler": "no_op"}
    wrong_runner = {**case, "runner": "no-op"}
    unknown_case = {**case, "id": "DET-UNKNOWN-001"}
    for label, mutated in (("unknown assertion", unknown), ("wrong runner", wrong_runner), ("wrong handler", wrong_handler), ("unknown case id", unknown_case)):
        if not check_binding(mutated):
            errors.append(f"binding mutation was not rejected: {label}")
    try:
        matrix = yaml.safe_load((root / "docs/engines/test-matrix.yaml").read_text(encoding="utf-8"))
        binding_data = yaml.safe_load((root / "docs/engines/deterministic-case-bindings.yaml").read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [f"cannot load core engine bindings for mutation test: {exc}"]
    engines = matrix.get("engines", [])
    core_bindings = binding_data.get("cases", [])
    baseline = validate_binding_set(engines, core_bindings)
    if baseline:
        errors.append(f"existing 63-case binding set is invalid: {baseline[0]}")
        return errors
    for label, field, value in (
        ("unknown core assertion id", "assertion_id", "crud.unknown_assertion"),
        ("misdirected core command index", "command_index", 1),
    ):
        mutated_bindings = deepcopy(core_bindings)
        target = next(item for item in mutated_bindings if item.get("id") == "create-valid" and item.get("engine") == "crud")
        target[field] = value
        if not validate_binding_set(engines, mutated_bindings):
            errors.append(f"core binding mutation was not rejected: {label}")
    return errors


def test_authorization_revocation(case: dict, root: Path) -> list[str]:
    del root
    errors: list[str] = []

    class RevokingCrud(RecordCrud):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.revoked = False

        @property
        def records(self) -> dict[str, dict]:
            snapshot = super().records
            self.revoked = True
            return snapshot

        def apply(self, request: dict) -> dict:
            if request.get("operation") == "read" and self.revoked:
                raise ContractError("authorization revoked before CRUD Read")
            return super().apply(request)

    crud = RevokingCrud(
        {"collection-a": {"collection_id": "collection-a", "active": True}},
        {"rec-revoked": runtime_record("rec-revoked", text="alpha sensitive-sentinel")},
    )
    result = search(crud, search_request(query="alpha"))
    expected = case["expected"]
    if result["status"] != expected["status"]:
        errors.append(f"expected {expected['status']} after revocation, got {result['status']}")
    if result["results"] and result["results"][0]["disclosure_level"] != expected["disclosure_level"]:
        errors.append("revoked search returned a disclosure level above L0")
    serialized = repr(result)
    if "sensitive-sentinel" in serialized or "selected_chunks" in serialized or "expanded_content" in serialized:
        errors.append("revoked search returned body or Chunk content")
    body_returned = "sensitive-sentinel" in serialized or "selected_chunks" in serialized or "expanded_content" in serialized
    if body_returned != expected["body_returned"]:
        errors.append("revoked search body-return result differs from the expected outcome")
    if result.get("mutation") != expected["mutation"] or crud.events:
        errors.append("revoked search mutated CRUD state")
    return errors


def test_chunk_effective_restriction(case: dict, root: Path) -> list[str]:
    del root
    errors: list[str] = []
    record = runtime_record("rec-chunk-scope", chunks=[
        {"chunk_id": "chunk-visible", "parent_record_id": "rec-chunk-scope", "text_ref": "safe", "text": "alpha visible-sentinel", "visibility": "internal", "staleness": "current"},
        {"chunk_id": "chunk-restricted", "parent_record_id": "rec-chunk-scope", "text_ref": "private", "text": "alpha restricted-sentinel", "visibility": "restricted", "staleness": "current"},
    ])
    crud = RecordCrud({"collection-a": {"collection_id": "collection-a", "active": True}}, {record["record_id"]: record})
    hidden_only = search(crud, search_request(query="restricted-sentinel"))
    expected = case["expected"]
    if bool(hidden_only["results"]) != expected["restricted_text_in_rank"]:
        errors.append("restricted Chunk influenced candidate ranking")
    for level in ("L3", "L4"):
        result = search(crud, search_request(query="alpha", requested_disclosure=level))
        serialized = repr(result)
        content_leaked = "restricted-sentinel" in serialized or "chunk-restricted" in serialized
        if level == "L3":
            selected = result["results"][0].get("selected_chunks", [])
            selected_leaked = any(chunk.get("chunk_id") == "chunk-restricted" or "restricted-sentinel" in repr(chunk) for chunk in selected)
            if selected_leaked != expected["restricted_text_in_selected_chunks"]:
                errors.append("restricted Chunk selection differs from expected outcome")
            if [chunk.get("chunk_id") for chunk in selected] != ["chunk-visible"]:
                errors.append("L3 did not return only the eligible Chunk")
        if level == "L4":
            expanded = result["results"][0].get("expanded_content", [])
            expanded_leaked = any(chunk.get("chunk_id") == "chunk-restricted" or "restricted-sentinel" in repr(chunk) for chunk in expanded)
            if expanded_leaked != expected["restricted_text_in_expanded_content"]:
                errors.append("restricted Chunk expansion differs from expected outcome")
            if [chunk.get("chunk_id") for chunk in expanded] != ["chunk-visible"]:
                errors.append("L4 did not return only the eligible Chunk")
        if level == "L4" and content_leaked != expected["restricted_text_in_expanded_content"]:
            errors.append("restricted Chunk content leak differs from expected outcome")
    if crud.events:
        errors.append("Search mutated CRUD state while filtering Chunk restrictions")
    return errors


def test_transfer_retry(case: dict, root: Path) -> list[str]:
    del root
    errors: list[str] = []
    record = runtime_record("rec-retry")
    record["current_use"] = False
    record["processing_state"] = "pending"
    record["curation_status"] = "new"
    review = {
        "review_id": "review-transfer-retry",
        "target_id": "rec-retry",
        "reviewer": "reviewer-synthetic",
        "purpose": "synthetic retry test",
        "evidence_refs": ["synthetic://receipt-001"],
        "rationale": "Sanitized receipt with explicit scope.",
        "reviewed_at": "2026-10-04T12:00:00Z",
        "decision": "accepted",
    }
    received = {"acceptance": "accepted", "local_record": record}
    crud = RecordCrud({"collection-a": {"collection_id": "collection-a", "active": True}})
    first = accept_received(received, rem_status="passed", semantic_status="accepted", crud=crud, semantic_review=review, actor="actor-synthetic")
    # Model a lost acknowledgment: the receiver accepted, but the sender retries
    # the same receipt and the caller observes only the retry result.
    retry = accept_received(received, rem_status="passed", semantic_status="accepted", crud=crud, semantic_review=review, actor="actor-synthetic")
    if first["status"] != "current" or retry["status"] != "current":
        errors.append("accepted receipt did not remain accepted after retry")
    expected = case["expected"]
    if len(crud.records) != expected["records"] or len(crud.events) != expected["crud_events"]:
        errors.append(f"retry was not exactly-once at CRUD: records={len(crud.records)}, events={len(crud.events)}")
    if retry.get("local_record", {}).get("record_id") != "rec-retry":
        errors.append("retry returned the wrong Record identity")
    return errors


def test_migration_interruption(case: dict, root: Path) -> list[str]:
    del root
    errors: list[str] = []
    source = {"source_version": "2.2.0", "record_ids": ["r1", "r2", "r3", "r4", "r5"]}
    before = deepcopy(source)
    preflight = {
        "source_version": "2.2.0",
        "target_version": "3.0.0",
        "mapping": "complete",
        "privacy": "proven",
        "rollback": "tested",
        "target_contract": "verified",
        "human_approval": "present",
        "unsafe_raw_fallback": False,
        "execution_state": case["input"]["execution_state"],
    }
    status = evaluate_migration(preflight)
    if status != case["expected"]["status"]:
        errors.append(f"interrupted migration expected {case['expected']['status']}, got {status}")
    if (source != before) != case["expected"]["source_changed"]:
        errors.append("migration preflight modified its source fixture")
    if case["expected"]["target_promoted"] is not False or case["expected"]["runtime_resume_tested"] is not False:
        errors.append("scenario must state that runtime resume remains untested")
    return errors


def test_missing_skill_capability(case: dict, root: Path) -> list[str]:
    errors: list[str] = []
    operation = (root / "candidates/skill-v3/references/v3-operation.md").read_text(encoding="utf-8")
    scenario = case["input"]
    if scenario["capability_available"] or scenario["authorization_context"] != "missing":
        errors.append("fixture must represent unavailable capability and missing authorization")
    if case["expected"] != {"disposition": "unavailable", "read_performed": False, "write_performed": False}:
        errors.append("scenario must fail closed without Read or Write")
    if "mark that operation unavailable and stop" not in operation:
        errors.append("candidate skill does not direct the unavailable-capability stop")
    if "Do not simulate a governed read by scanning vault files directly" not in operation:
        errors.append("candidate skill does not prohibit direct filesystem fallback")
    return errors


HANDLERS: dict[str, Callable[[dict, Path], list[str]]] = {
    "binding_mutation": test_binding_mutation,
    "authorization_revocation": test_authorization_revocation,
    "chunk_effective_restriction": test_chunk_effective_restriction,
    "transfer_retry": test_transfer_retry,
    "migration_interruption": test_migration_interruption,
    "missing_skill_capability": test_missing_skill_capability,
}


def validate_semantic_envelope(root: Path, cases: list[dict], errors: list[str]) -> None:
    try:
        review = yaml.safe_load((root / REVIEW_FILE).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        errors.append(f"cannot read semantic review envelope: {exc}")
        return
    policy = review.get("review_policy", {}) if isinstance(review, dict) else {}
    if policy.get("status") != "ai-assessed-human-confirmation-pending":
        errors.append("semantic review must remain AI-assessed and human-pending")
    if policy.get("human_confirmation") != "pending" or policy.get("record_mutations") != "none":
        errors.append("semantic review must preserve the human gate and zero-mutation boundary")
    if policy.get("second_pass") != "same-reviewer-adversarial-self-challenge; not an independent reviewer":
        errors.append("semantic review must disclose that the second pass is not independent")
    expected_ids = {case.get("id") for case in cases}
    review_cases = review.get("cases", []) if isinstance(review, dict) else []
    observed_ids = {case.get("id") for case in review_cases if isinstance(case, dict)}
    if observed_ids != expected_ids:
        errors.append(f"semantic review coverage mismatch: expected {sorted(expected_ids)}, got {sorted(observed_ids)}")
    for case in review_cases:
        if not isinstance(case, dict):
            continue
        for field in ("primary_disposition", "adversarial_disposition", "rationale", "countercheck"):
            if not isinstance(case.get(field), str) or not case[field].strip():
                errors.append(f"{case.get('id')}: semantic review missing {field}")
        refs = case.get("evidence_refs", [])
        if not isinstance(refs, list) or not refs:
            errors.append(f"{case.get('id')}: semantic review requires evidence references")
        else:
            for reference in refs:
                if not isinstance(reference, str) or not reference.strip():
                    errors.append(f"{case.get('id')}: evidence references must be non-empty strings")
                    continue
                relative = reference.split("#", 1)[0]
                path = Path(relative)
                if path.is_absolute() or ".." in path.parts or not (root / path).is_file():
                    errors.append(f"{case.get('id')}: evidence reference is missing or escapes the repository: {relative}")
        for field in ("constitution_refs", "decision_refs"):
            if not isinstance(case.get(field), list) or not case[field]:
                errors.append(f"{case.get('id')}: semantic review requires {field}")


def run(root: Path) -> tuple[list[str], int, int]:
    errors: list[str] = []
    try:
        data = yaml.safe_load((root / SCENARIO_FILE).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [f"cannot read scenario file: {exc}"], 0, 0
    if not isinstance(data, dict) or data.get("schema_version") != "1.0":
        return ["scenario file must be a schema_version 1.0 mapping"], 0, 0
    if data.get("privacy") != "synthetic-only" or data.get("mutation") != "none":
        errors.append("coverage-gap scenarios must be synthetic-only and non-mutating")
    deterministic = data.get("deterministic_cases", [])
    semantic = data.get("semantic_cases", [])
    actual_ids = [case.get("id") for case in deterministic if isinstance(case, dict)]
    if len(actual_ids) != len(deterministic) or len(actual_ids) != len(set(actual_ids)):
        errors.append("deterministic scenario IDs must be unique non-empty mappings")
    expected_deterministic_ids = {
        "DET-BIND-001", "DET-SEARCH-REVOCATION-001", "DET-SEARCH-CHUNK-001",
        "DET-TRANSFER-RETRY-001", "DET-MIGRATION-INTERRUPT-001", "DET-SKILL-CAPABILITY-001",
    }
    if set(actual_ids) != expected_deterministic_ids:
        errors.append(f"deterministic scenario coverage mismatch: expected {sorted(expected_deterministic_ids)}, got {sorted(actual_ids)}")
    if {case.get("id") for case in semantic if isinstance(case, dict)} != SEMANTIC_IDS:
        errors.append("semantic scenario coverage does not match the three reviewed scenarios")
    executed = 0
    for case in deterministic:
        if not isinstance(case, dict):
            continue
        binding_errors = check_binding(case)
        errors.extend(binding_errors)
        if binding_errors:
            continue
        handler = HANDLERS.get(case.get("handler"))
        if handler is None:
            errors.append(f"{case.get('id')}: executable scenario handler is unavailable")
            continue
        errors.extend(handler(case, root))
        executed += 1
    validate_semantic_envelope(root, semantic, errors)
    return errors, executed, len(semantic)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors, executed, semantic_count = run(root)
    if errors:
        print(f"validate_v3_coverage_gap_scenarios: FAILED — {len(errors)} error(s), {executed} deterministic scenario(s) executed")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print(
        "validate_v3_coverage_gap_scenarios: OK — "
        f"{executed} deterministic scenarios executed; {semantic_count} semantic assessments are complete and human-pending"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
