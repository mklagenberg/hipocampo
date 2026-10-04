#!/usr/bin/env python3
"""Execute new synthetic V3 coverage-gap scenarios and validate review envelopes.

Six deterministic scenarios exercise local V3 components or explicit test
adapters. Three semantic scenarios are checked for a complete review envelope
and an explicit pending or confirmed human disposition; this script does not
decide semantic truth.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import os
from pathlib import Path
import shutil
import stat
import subprocess
from typing import Callable
import uuid

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
        "DET-MIGRATION-INTERRUPT-001": ("migration.interrupted_branch_isolated_until_validation", "v3-coverage-gap-scenarios", "migration_interruption"),
        "DET-SKILL-CAPABILITY-001": ("skill.capability_authorization_gate_fails_closed_before_io", "v3-coverage-gap-scenarios", "missing_skill_capability"),
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
    if (
        case["expected"]["target_promoted"] is not False
        or case["expected"]["runtime_resume_tested"] is not False
        or case["expected"].get("partial_change_on_task_branch") is not True
        or case["expected"].get("main_sha_unchanged") is not True
        or case["expected"].get("premature_merge") is not False
    ):
        errors.append("scenario must state that runtime resume remains untested")

    # Exercise the declared Git recovery boundary without touching this checkout
    # or any vault: a partial migration commit stays on its dedicated branch.
    git_env = os.environ.copy()
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR", "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES"):
        git_env.pop(key, None)
    git_env.update({
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_AUTHOR_DATE": "2026-10-04T12:00:00+00:00",
        "GIT_COMMITTER_DATE": "2026-10-04T12:00:00+00:00",
    })

    def git(repo: Path, *args: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            text=True,
            check=False,
            env=git_env,
        )
        if result.returncode:
            raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
        return result.stdout.strip()

    try:
        temp_root = root / ".tmp"
        temp_root.mkdir(exist_ok=True)
        repo = temp_root / f"synthetic-migration-{uuid.uuid4().hex}"
        repo.mkdir()
        try:
            git(repo, "init", "--quiet", "--initial-branch=main")
            git(repo, "config", "user.name", "Hipocampo Synthetic Test")
            git(repo, "config", "user.email", "synthetic@example.invalid")
            git(repo, "config", "core.autocrlf", "false")
            source_path = repo / "source.md"
            source_path.write_text("version: 2.2.0\nrecords: [r1, r2, r3, r4, r5]\n", encoding="utf-8")
            git(repo, "add", "source.md")
            git(repo, "commit", "--quiet", "-m", "synthetic baseline")
            main_sha = git(repo, "rev-parse", "HEAD")
            git(repo, "switch", "--quiet", "-c", "migration/test")
            partial_path = repo / "partial-migration.yaml"
            partial_path.write_text("mapped_records: [r1, r2]\nstate: interrupted\n", encoding="utf-8")
            git(repo, "add", "partial-migration.yaml")
            git(repo, "commit", "--quiet", "-m", "synthetic partial migration")
            partial_sha = git(repo, "rev-parse", "HEAD")
            if git(repo, "branch", "--show-current") != "migration/test":
                errors.append("partial migration did not remain on its dedicated branch")
            git(repo, "switch", "--quiet", "main")
            if git(repo, "rev-parse", "HEAD") != main_sha:
                errors.append("main advanced before migration validation")
            if _git_object_exists(repo, "main:partial-migration.yaml", git_env):
                errors.append("partial migration file is present on main before validation")
            git(repo, "switch", "--quiet", "migration/test")
            if git(repo, "rev-parse", "HEAD") != partial_sha or not partial_path.is_file():
                errors.append("partial migration was not preserved on the task branch")
            if "main" in git(repo, "branch", "--contains", partial_sha).splitlines():
                errors.append("partial migration commit is reachable from main before validation")
            if git(repo, "rev-parse", "main") != main_sha:
                errors.append("main changed while preserving the interrupted migration branch")
            if not errors:
                print(f"    synthetic Git baseline={main_sha}; partial={partial_sha}; main unchanged; no merge")
        finally:
            if repo.exists():
                shutil.rmtree(repo, onerror=_remove_readonly)
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        errors.append(f"synthetic Git branch isolation check failed: {exc}")
    return errors


def _remove_readonly(function, path, exc_info) -> None:
    """Git object files can be read-only on Windows; clean only our temp repo."""
    del exc_info
    os.chmod(path, stat.S_IWRITE)
    function(path)


def _git_object_exists(repo: Path, object_name: str, env: dict[str, str]) -> bool:
    result = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "-e", object_name],
        capture_output=True,
        check=False,
        env=env,
    )
    return result.returncode == 0


def test_missing_skill_capability(case: dict, root: Path) -> list[str]:
    errors: list[str] = []
    operation = (root / "candidates/skill-v3/references/v3-operation.md").read_text(encoding="utf-8")
    scenario = case["input"]
    if "mark that operation unavailable and stop" not in operation:
        errors.append("candidate skill does not direct the unavailable-capability stop")
    if "Do not simulate a governed read by scanning vault files directly" not in operation:
        errors.append("candidate skill does not prohibit direct filesystem fallback")

    class SyntheticHostAdapter:
        """Test double for host capability and authorization; never a real host."""
        def __init__(self, capability: str, auth: str, crud: RecordCrud):
            self.capability = capability
            self.auth = auth
            self.crud = crud
            self.snapshot_reads = 0
            self.canonical_reads = 0
            self.writes = 0

        def dispatch(self) -> dict:
            if self.capability != "proven":
                disposition = "authorization_required" if self.capability == "authorization_required" else "unavailable"
                return {"disposition": disposition, "results": [], "read_performed": False, "write_performed": False}
            if self.auth != "valid":
                return {"disposition": "authorization_required", "results": [], "read_performed": False, "write_performed": False}
            adapter = self

            class CountingCrud(RecordCrud):
                @property
                def records(self):
                    adapter.snapshot_reads += 1
                    return super().records

                def apply(self, request: dict) -> dict:
                    if request.get("operation") == "read":
                        adapter.canonical_reads += 1
                    else:
                        adapter.writes += 1
                    return super().apply(request)

            wrapped = CountingCrud(self.crud.active_collections, self.crud.records)
            result = search(wrapped, search_request(query="alpha"))
            return {
                "disposition": result["status"],
                "results": result["results"],
                "read_performed": self.canonical_reads > 0,
                "write_performed": self.writes > 0,
            }

    record = runtime_record("rec-capability", text="alpha synthetic-capability-body")
    base_crud = RecordCrud({"collection-a": {"collection_id": "collection-a", "active": True}}, {record["record_id"]: record})
    expected_matrix = case["expected"].get("capability_matrix", [])
    if not expected_matrix:
        errors.append("scenario does not declare its synthetic capability/auth matrix")
    for expected_case in expected_matrix:
        capability = expected_case["capability"]
        auth = expected_case["authorization_context"]
        expected_disposition = expected_case["disposition"]
        expect_read = expected_case["read_performed"]
        adapter = SyntheticHostAdapter(capability, auth, base_crud)
        result = adapter.dispatch()
        if result["disposition"] != expected_disposition:
            errors.append(f"{capability}/{auth}: expected {expected_disposition}, got {result['disposition']}")
        if result["read_performed"] != expect_read or result["write_performed"]:
            errors.append(f"{capability}/{auth}: incorrect canonical Read/Write activity")
        if not expect_read and (result["results"] or adapter.snapshot_reads or adapter.canonical_reads):
            errors.append(f"{capability}/{auth}: denied request accessed or returned Record content")
        if adapter.canonical_reads != expected_case.get("canonical_reads", 0):
            errors.append("authorized request must perform exactly one canonical CRUD Read")
        if not errors and expect_read:
            print(f"    capability={capability}, authorization={auth}, canonical_reads={adapter.canonical_reads}, writes={adapter.writes}")
    revoked_case = {"expected": case["expected"].get("revocation_after_snapshot", {})}
    errors.extend(test_authorization_revocation(revoked_case, root))
    if scenario.get("capability_available") is not False or scenario.get("authorization_context") != "missing":
        errors.append("fixture must retain the original unavailable-capability, missing-authorization case")
    if any(case["expected"].get(key) != value for key, value in {
        "disposition": "unavailable", "read_performed": False, "write_performed": False,
    }.items()):
        errors.append("scenario contract must retain fail-closed behavior without Read or Write")
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
    human_confirmation = policy.get("human_confirmation")
    human_review = review.get("human_review", {}) if isinstance(review, dict) else {}
    if policy.get("record_mutations") != "none":
        errors.append("semantic review must preserve the zero-mutation boundary")
    if human_confirmation == "pending":
        if policy.get("status") != "ai-assessed-human-confirmation-pending":
            errors.append("pending semantic review must disclose its AI-assessed, human-pending status")
        if human_review.get("status") != "pending" or human_review.get("decision") is not None:
            errors.append("pending semantic review must not contain a human decision")
    elif human_confirmation == "confirmed":
        if policy.get("status") != "ai-assessed-human-confirmed":
            errors.append("confirmed semantic review must preserve its AI-assessment and human-confirmation status")
        if human_review.get("status") != "confirmed" or not isinstance(human_review.get("decision"), str) or not human_review["decision"].strip():
            errors.append("human confirmation must record a non-empty decision")
        if not human_review.get("confirmed_at") or not human_review.get("reviewer"):
            errors.append("human confirmation must record reviewer and confirmation date")
    else:
        errors.append("human_confirmation must be pending or confirmed")
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
        if human_confirmation == "confirmed" and case.get("human_disposition") != case.get("primary_disposition"):
            errors.append(f"{case.get('id')}: human disposition must explicitly confirm the reviewed primary disposition")
        if human_confirmation == "pending" and "human_disposition" in case:
            errors.append(f"{case.get('id')}: pending review must not contain a human disposition")
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


def run(root: Path) -> tuple[list[str], int, int, str, list[tuple[str, bool]]]:
    errors: list[str] = []
    try:
        data = yaml.safe_load((root / SCENARIO_FILE).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [f"cannot read scenario file: {exc}"], 0, 0, "unknown", []
    if not isinstance(data, dict) or data.get("schema_version") != "1.0":
        return ["scenario file must be a schema_version 1.0 mapping"], 0, 0, "unknown", []
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
    scenario_results: list[tuple[str, bool]] = []
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
        case_errors = handler(case, root)
        errors.extend(case_errors)
        scenario_results.append((case["id"], not case_errors))
        executed += 1
    validate_semantic_envelope(root, semantic, errors)
    try:
        review = yaml.safe_load((root / REVIEW_FILE).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        human_confirmation = "unknown"
    else:
        human_confirmation = review.get("review_policy", {}).get("human_confirmation", "unknown") if isinstance(review, dict) else "unknown"
    return errors, executed, len(semantic), human_confirmation, scenario_results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors, executed, semantic_count, human_confirmation, scenario_results = run(root)
    for case_id, passed in scenario_results:
        print(f"  [{'PASS' if passed else 'FAIL'}] {case_id}")
    if errors:
        print(f"validate_v3_coverage_gap_scenarios: FAILED — {len(errors)} error(s), {executed} deterministic scenario(s) executed")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print(
        "validate_v3_coverage_gap_scenarios: OK — "
        f"{executed} deterministic scenarios executed; {semantic_count} semantic assessments are complete; human confirmation: {human_confirmation}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
