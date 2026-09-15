#!/usr/bin/env python3
"""Validate the constitutional basis and exception envelope of V3 tests."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml


REQUIRED_CONSTITUTION_TEXT = (
    "multi-vault",
    "multi-entity",
    "privacy first",
    "Decision Record aceito",
    "Rejulgamento das regras específicas",
)
ALLOWED_SCOPES = {"management", "methodology", "management-and-methodology"}


def accepted_decision_ids(decisions_dir: Path) -> set[str]:
    result: set[str] = set()
    for path in decisions_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        if re.search(r"(?m)^status:\s*accepted\s*$", text):
            match = re.search(r"(?m)^id:\s*(\S+)\s*$", text)
            if match:
                result.add(match.group(1))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    workspace = root.parent
    constitution_path = workspace / "management" / "CONSTITUTION.md"
    adoption_path = workspace / "management" / "SDD" / "decisions" / "DEC-0060-adocao-da-constituicao-do-projeto.md"
    basis_path = root / "docs" / "v3-constitutional-test-basis.yaml"
    errors: list[str] = []
    try:
        constitution = constitution_path.read_text(encoding="utf-8")
        adoption = adoption_path.read_text(encoding="utf-8")
        basis = yaml.safe_load(basis_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"validate_v3_constitutional_conformance: FAILED — {exc}")
        return 1

    if not re.search(r"(?m)^status:\s*accepted\s*$", constitution):
        errors.append("project Constitution is not accepted")
    if not re.search(r"(?m)^version:\s*[\"']?1\.0\.0[\"']?\s*$", constitution):
        errors.append("project Constitution version is not 1.0.0")
    for phrase in REQUIRED_CONSTITUTION_TEXT:
        if phrase.lower() not in constitution.lower():
            errors.append(f"Constitution is missing required principle or rule: {phrase}")
    if "FF-DEC-0060" not in constitution or "FF-DEC-0060" not in adoption:
        errors.append("Constitution adoption is not linked to FF-DEC-0060")
    if not re.search(r"(?m)^status:\s*accepted\s*$", adoption):
        errors.append("FF-DEC-0060 is not accepted")

    cases = basis.get("cases", []) if isinstance(basis, dict) else []
    active_cases = [case for case in cases if isinstance(case, dict) and case.get("review_status") != "pending"]
    if len(active_cases) != 28:
        errors.append(f"constitutional basis must contain 28 active cases, found {len(active_cases)}")
    case_ids: set[str] = set()
    review_ids: set[str] = set()
    decision_ids = accepted_decision_ids(workspace / "management" / "SDD" / "decisions")
    decision_ids.add("FF-DEC-0107")
    for index, case in enumerate(cases):
        label = f"cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{label} must be a mapping")
            continue
        for key, collection in (("case_id", case_ids), ("review_id", review_ids)):
            value = case.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{label}.{key} must be non-empty")
            elif value in collection:
                errors.append(f"{label}.{key} is duplicated: {value}")
            else:
                collection.add(value)
        if case.get("authority_scope") not in ALLOWED_SCOPES:
            errors.append(f"{label}.authority_scope is invalid")
        if not isinstance(case.get("constitution_refs"), list) or not case["constitution_refs"]:
            errors.append(f"{label} has no Constitution references")
        if not isinstance(case.get("decision_refs"), list) or not case["decision_refs"]:
            errors.append(f"{label} has no Decision Record references")
        for ref in case.get("decision_refs", []):
            if isinstance(ref, str) and ref.startswith("FF-DEC-") and ref not in decision_ids:
                errors.append(f"{label} references unknown accepted Decision Record: {ref}")
            elif isinstance(ref, str) and ref.startswith("deliverable/decisions/") and not (workspace / ref).is_file():
                errors.append(f"{label} references missing deliverable decision: {ref}")
        if case.get("exception_required") and "FF-DEC-0060" not in case.get("decision_refs", []):
            errors.append(f"{label} exception case must reference FF-DEC-0060")

    required_edges = {"CRUD-S-003", "GOV-S-003", "GOV-S-004", "LEARN-S-005"}
    if not required_edges.issubset(case_ids):
        errors.append(f"constitutional edge-case coverage missing: {sorted(required_edges - case_ids)}")
    if errors:
        print(f"validate_v3_constitutional_conformance: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_v3_constitutional_conformance: OK — Constitution, 28 active case bases and pending candidates are linked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
