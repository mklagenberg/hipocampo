#!/usr/bin/env python3
"""Validate the deterministic envelope of the unreleased V3 search contract.

This validates contract shape and sanitized fixtures only. It does not prove
relevance, authority, privacy permission or semantic truth.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from v3_crud_engine import RecordCrud
from v3_search_engine import SearchContractError, search


LEVELS = ["L0", "L1", "L2", "L3", "L4"]
EXPECTED = {
    "reject-unauthorized-expansion": ("blocked", "L0"),
    "preserve-independent-dimensions": ("needs_review", "L2"),
    "prose-default": ("partial", "L2"),
    "structured-only-on-request": ("accepted", "L2"),
}


def runtime_record(record_id: str, *, text: str, staleness: str = "current", visibility: str = "internal") -> dict:
    return {
        "record_id": record_id,
        "record_version": 1,
        "physical_path": f"records/{record_id}.md",
        "status": "active",
        "visibility": visibility,
        "staleness": staleness,
        "entity": "entity-a",
        "scope": "scope-a",
        "source": {"source_id": f"source-{record_id}", "source_kind": "conversation", "entity": "entity-a"},
        "vault": {"vault_id": "vault-a", "entity": "entity-a", "profile": "entity", "role": "anchor"},
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
        "artifacts": [{"artifact_id": f"artifact-{record_id}", "role": "supporting", "version": 1, "reference": "sanitized/ref", "visibility": visibility}],
        "title": "Alpha result",
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

    try:
        expanded = search(crud, {**base, "request_id": "search-test-expanded", "requested_disclosure": "L4", "explicit_expansion_authorization": True})
        item = expanded["results"][0]
        if item["disclosure_level"] != "L4" or "expanded_content" not in item:
            errors.append("explicitly authorized L4 expansion did not return L4 content")
    except SearchContractError as exc:
        errors.append(f"runtime authorized-expansion case failed: {exc}")

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
    if stale["results"][0]["disclosure_level"] != "L2" or "source_requires_revalidation" not in stale["results"][0]["limits"]:
        errors.append("stale source was not limited and surfaced")

    inaccessible_record = runtime_record("rec-inaccessible", text="alpha unavailable")
    inaccessible_record["source_accessible"] = False
    inaccessible_crud = RecordCrud(
        {"collection-a": {"collection_id": "collection-a", "active": True}},
        {"rec-inaccessible": inaccessible_record},
    )
    inaccessible = search(inaccessible_crud, {**base, "request_id": "search-test-inaccessible", "requested_disclosure": "L3"})
    if inaccessible["status"] != "blocked" or inaccessible["results"][0]["disclosure_level"] != "L0" or "source_access_unavailable" not in inaccessible["results"][0]["limits"]:
        errors.append("inaccessible evidence was not blocked at L0 with a surfaced limit")

    restricted_record = runtime_record("rec-restricted", text="alpha restricted", visibility="restricted")
    restricted_crud = RecordCrud(
        {"collection-a": {"collection_id": "collection-a", "active": True}},
        {"rec-restricted": restricted_record},
    )
    restricted = search(restricted_crud, {**base, "request_id": "search-test-restricted", "requested_disclosure": "L3", "explicit_expansion_authorization": True})
    if restricted["status"] != "blocked" or restricted["results"][0]["disclosure_level"] != "L1":
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
    print("validate_v3_search_progressive_disclosure: OK — contract envelope and 4 sanitized fixtures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
