#!/usr/bin/env python3
"""Retroactive use-case inventory, contradiction, and route-evidence gate."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import sys

import yaml


DISPOSITIONS = {"preserved", "updated-by-decision", "repaired", "blocked"}
ROUTE_MODES = {"dual", "semantic-only", "deterministic-only"}
FIXTURE_SOURCES = (
    "v3-crud-use-case-fixtures.yaml",
    "v3-crud-fixtures.yaml",
    "v3-semantic-fixtures.yaml",
    "bootstrap-invitation-fixtures.yaml",
    "access-ingress-fixtures.yaml",
    "v3-ingress-fixtures.yaml",
    "v3-profile-fixtures.yaml",
    "v3-search-progressive-disclosure-fixtures.yaml",
)


def same_disposition(left: object, right: object) -> bool:
    """Accept legacy hyphen/underscore spellings as the same disposition."""
    if isinstance(left, str) and isinstance(right, str):
        return left.replace("-", "_").casefold() == right.replace("-", "_").casefold()
    return left == right


def contradictions(cases: list[dict]) -> list[tuple[str, str]]:
    groups: dict[str, list[dict]] = {}
    for case in cases:
        vector = case.get("vector")
        if isinstance(vector, dict):
            key = json.dumps(vector, sort_keys=True, separators=(",", ":"))
            groups.setdefault(key, []).append(case)
    conflicts = []
    for group in groups.values():
        for index, left in enumerate(group):
            for right in group[index + 1:]:
                if left.get("expected") == right.get("expected"):
                    continue
                same_resolution = (left.get("resolution_ref") and
                                   left.get("resolution_ref") == right.get("resolution_ref"))
                if not same_resolution:
                    conflicts.append((str(left.get("id")), str(right.get("id"))))
    return conflicts


def fixture_case(root: Path, reference: str) -> dict:
    filename, separator, case_id = reference.partition("#")
    if not separator or not case_id or "/" in filename or ".." in filename:
        raise ValueError(f"invalid fixture reference: {reference}")
    data = yaml.safe_load((root / "docs" / filename).read_text(encoding="utf-8"))
    cases = data.get("cases", data.get("fixtures", []))
    for case in cases:
        if case.get("id") == case_id:
            return case
    raise ValueError(f"fixture case not found: {reference}")


def fixture_expectation(case: dict) -> object:
    for key in ("expected_disposition", "expected", "status", "action"):
        if key in case:
            return {key: case[key]}
    return {key: value for key, value in case.items() if key != "id"}


def fixture_vector(case: dict) -> dict | None:
    # Only compare cases whose actual input is explicit. Generic fixture
    # metadata such as operation/fixture ID is not enough to establish that
    # two cases exercise the same vector.
    for key in ("vector", "input", "request"):
        value = case.get(key)
        if isinstance(value, dict) and value:
            return {key: value}
    return None


def expected_portfolio(matrix: dict, bindings: list[dict], root: Path) -> dict[str, dict]:
    result: dict[str, dict] = {}
    binding_map = {(item.get("engine"), item.get("id")): item for item in bindings}
    for engine in matrix.get("engines", []):
        engine_id = engine.get("id")
        for case_id in engine.get("deterministic_cases", []):
            key = f"matrix:{engine_id}/{case_id}"
            binding = binding_map.get((engine_id, case_id), {})
            command_index = binding.get("command_index")
            commands = engine.get("deterministic_commands", [])
            result[key] = {
                "key": key, "kind": "deterministic", "engine": engine_id, "case_id": case_id,
                "command": commands[command_index] if isinstance(command_index, int) and 0 <= command_index < len(commands) else None,
                "assertion_id": binding.get("assertion_id"), "disposition": "preserved",
                "evidence": "docs/engines/test-matrix.yaml",
            }
        for case in engine.get("semantic_cases", []):
            case_id = case.get("id")
            key = f"matrix:{engine_id}/{case_id}"
            result[key] = {
                "key": key, "kind": "semantic", "engine": engine_id, "case_id": case_id,
                "fixture_ref": case.get("fixture_ref"), "expected": case.get("expected_disposition"),
                "disposition": "preserved", "evidence": case.get("fixture_ref"),
            }
    for filename in FIXTURE_SOURCES:
        source = yaml.safe_load((root / "docs" / filename).read_text(encoding="utf-8"))
        cases = source.get("cases", source.get("fixtures", []))
        for case in cases:
            case_id = case.get("id")
            key = f"fixture:{filename}#{case_id}"
            result[key] = {"key": key, "kind": "source-fixture", "fixture_ref": f"{filename}#{case_id}",
                           "expected": fixture_expectation(case), "disposition": "preserved",
                           "evidence": f"docs/{filename}", "vector": fixture_vector(case)}
    return result


def execute_deterministic_commands(matrix: dict, root: Path) -> tuple[dict[str, dict], list[str]]:
    commands: dict[str, dict] = {}
    errors: list[str] = []
    unique = []
    for engine in matrix.get("engines", []):
        for command in engine.get("deterministic_commands", []):
            if command not in unique:
                unique.append(command)
    # Supplemental validators are part of the matrix-level evidence too. This
    # gate is itself listed there, so omit only the recursive self-invocation.
    for command in matrix.get("policy", {}).get("supplemental_deterministic_commands", []):
        if "validate_v3_quality_gates.py" in command:
            continue
        if command not in unique:
            unique.append(command)
    for command in unique:
        try:
            argv = shlex.split(command)
            if not argv:
                raise ValueError("empty command")
            if argv[0] in {"python", "python3"}:
                argv[0] = sys.executable
            if len(argv) > 1 and Path(argv[1]).name == "validate_compatibility.py":
                argv.extend(["--channel", "stable"])
            completed = subprocess.run(argv, cwd=root, capture_output=True, text=True, encoding="utf-8",
                                       errors="replace", timeout=300, check=False)
            output = (completed.stdout + completed.stderr).strip()
            commands[command] = {"passed": completed.returncode == 0, "exit_code": completed.returncode,
                                 "output_sha256": hashlib.sha256(output.encode("utf-8")).hexdigest(),
                                 "output": output[:500]}
            if completed.returncode:
                errors.append(f"deterministic command failed ({completed.returncode}): {command}: {output[:500]}")
        except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
            commands[command] = {"passed": False, "error": str(exc)}
            errors.append(f"deterministic command could not run: {command}: {exc}")
    return commands, errors


def validate(gate: dict, portfolio: dict[str, dict], source_uc_cases: list[dict],
             root: Path, matrix: dict, bindings: list[dict], basis: dict,
             command_results: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    use_cases = gate.get("cases", [])
    use_case_ids = [case.get("id") for case in use_cases]
    source_uc_ids = [case.get("id") for case in source_uc_cases]
    if len(use_case_ids) != len(set(use_case_ids)):
        errors.append("CRUD use-case quality catalog has duplicate IDs")
    if set(use_case_ids) != set(source_uc_ids):
        errors.append("CRUD use-case catalog does not cover its source fixture exactly")
    source_uc_map = {case.get("id"): case for case in source_uc_cases}
    for case in use_cases:
        case_id = case.get("id")
        if case_id not in source_uc_map:
            continue
        if case.get("expected") != source_uc_map[case_id].get("expected"):
            errors.append(f"{case_id}: catalog expectation differs from source fixture")
        if case.get("disposition") not in DISPOSITIONS:
            errors.append(f"{case_id}: missing valid retroactive disposition")
        evidence = case.get("evidence")
        if not isinstance(evidence, str) or not (root / evidence).is_file():
            errors.append(f"{case_id}: evidence path is missing")
    for left, right in contradictions(use_cases):
        errors.append(f"contradictory expectations without disposition: {left} / {right}")

    declared_portfolio = gate.get("portfolio_cases", [])
    declared_map = {item.get("key"): item for item in declared_portfolio if isinstance(item, dict)}
    expected_map = expected_portfolio(matrix, bindings, root)
    if set(declared_map) != set(expected_map):
        missing = sorted(set(expected_map) - set(declared_map))
        extra = sorted(set(declared_map) - set(expected_map))
        errors.append(f"retroactive portfolio case coverage mismatch: missing={missing[:8]}, extra={extra[:8]}")
    basis_map = {item.get("case_id"): item for item in basis.get("cases", []) if isinstance(item, dict)}
    semantic_refs: dict[str, tuple[str, dict]] = {}
    binding_map = {(item.get("engine"), item.get("id")): item for item in bindings}
    for key, expected in expected_map.items():
        entry = declared_map.get(key)
        if entry is None:
            continue
        if entry.get("disposition") not in DISPOSITIONS:
            errors.append(f"{key}: missing valid retroactive disposition")
        if entry.get("evidence") != expected.get("evidence"):
            errors.append(f"{key}: evidence reference differs from source")
        if entry.get("kind") != expected.get("kind") or entry.get("expected") != expected.get("expected"):
            errors.append(f"{key}: case kind or expected disposition differs from source")
        if entry.get("disposition") == "updated-by-decision" and not entry.get("resolution_ref"):
            errors.append(f"{key}: changed expectation lacks a decision reference")
        if expected["kind"] == "deterministic":
            binding = binding_map.get((expected["engine"], expected["case_id"]))
            if not binding:
                errors.append(f"{key}: missing deterministic binding")
                continue
            if entry.get("command") != binding.get("command") or entry.get("assertion_id") != binding.get("assertion_id"):
                errors.append(f"{key}: deterministic command/assertion differs from its binding")
            evidence_result = command_results.get(expected.get("command"), {})
            if not evidence_result.get("passed"):
                errors.append(f"{key}: deterministic command lacks successful current-run evidence")
        elif expected["kind"] == "semantic":
            ref = expected.get("fixture_ref")
            try:
                case_fixture = fixture_case(root, ref)
            except (OSError, yaml.YAMLError, ValueError) as exc:
                errors.append(f"{key}: {exc}")
                continue
            fixture_outcome = case_fixture.get("expected_disposition", case_fixture.get("expected"))
            if (entry.get("fixture_ref") != ref or
                    (fixture_outcome is not None and not same_disposition(entry.get("expected"), fixture_outcome))):
                errors.append(f"{key}: semantic expectation differs from referenced fixture")
            if fixture_outcome is None and not case_fixture.get("review_boundary"):
                errors.append(f"{key}: semantic fixture lacks an explicit review boundary")
            basis_case = basis_map.get(expected["case_id"])
            if not basis_case or basis_case.get("expected_disposition") != expected.get("expected"):
                errors.append(f"{key}: semantic expectation differs from constitutional basis")
            semantic_refs[ref] = (expected["case_id"], case_fixture)
        else:
            try:
                source_case = fixture_case(root, expected["fixture_ref"])
            except (OSError, yaml.YAMLError, ValueError) as exc:
                errors.append(f"{key}: {exc}")
                continue
            if entry.get("expected") != fixture_expectation(source_case):
                errors.append(f"{key}: source fixture outcome differs from disposition catalog")

    all_cases = list(use_cases)
    all_cases.extend({"id": key, "vector": entry.get("vector"), "expected": entry.get("expected"),
                      "resolution_ref": entry.get("resolution_ref")}
                     for key, entry in declared_map.items() if entry.get("vector"))
    for left, right in contradictions(all_cases):
        errors.append(f"contradictory expectations across case portfolio without disposition: {left} / {right}")

    for capability in gate.get("dual_capabilities", []):
        mode = capability.get("mode", "dual")
        if mode not in ROUTE_MODES:
            errors.append(f"{capability.get('id')}: invalid route mode")
            continue
        if mode != "dual":
            if not capability.get("rationale"):
                errors.append(f"{capability.get('id')}: single-route capability needs rationale")
            continue
        if not capability.get("invariants") or not capability.get("vectors"):
            errors.append(f"{capability.get('id')}: dual capability lacks invariants or common vectors")
            continue
        for vector in capability["vectors"]:
            semantic_ref = vector.get("semantic_fixture_ref")
            deterministic_key = vector.get("deterministic_case_key")
            deterministic_case = declared_map.get(deterministic_key)
            if semantic_ref not in semantic_refs:
                try:
                    sem_case = fixture_case(root, semantic_ref)
                    sem_outcome = sem_case.get("expected_disposition", sem_case.get("expected"))
                except (OSError, yaml.YAMLError, ValueError, TypeError) as exc:
                    errors.append(f"{capability.get('id')}/{vector.get('id')}: semantic route evidence invalid: {exc}")
                    continue
            else:
                sem_case = semantic_refs[semantic_ref][1]
                sem_outcome = sem_case.get("expected_disposition", sem_case.get("expected"))
            if not deterministic_case or deterministic_case.get("kind") != "deterministic":
                errors.append(f"{capability.get('id')}/{vector.get('id')}: missing bound deterministic case")
                continue
            if not command_results.get(deterministic_case.get("command"), {}).get("passed"):
                errors.append(f"{capability.get('id')}/{vector.get('id')}: deterministic route was not executed successfully")
            deterministic_outcome = vector.get("deterministic_expected")
            if not sem_outcome or not deterministic_outcome:
                errors.append(f"{capability.get('id')}/{vector.get('id')}: missing route expectation")
            elif sem_outcome != deterministic_outcome and not vector.get("justified_difference"):
                errors.append(f"{capability.get('id')}/{vector.get('id')}: route outcomes diverge without disposition")
            if vector.get("semantic_expected") != sem_outcome:
                errors.append(f"{capability.get('id')}/{vector.get('id')}: semantic expectation differs from its fixture")
        if not capability.get("justified_differences"):
            errors.append(f"{capability.get('id')}: semantic/deterministic limits are not described")

    return errors


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    gate = yaml.safe_load((root / "docs/v3-quality-gate-fixtures.yaml").read_text(encoding="utf-8"))
    uc_source = yaml.safe_load((root / "docs/v3-crud-use-case-fixtures.yaml").read_text(encoding="utf-8"))
    matrix = yaml.safe_load((root / "docs/engines/test-matrix.yaml").read_text(encoding="utf-8"))
    bindings = yaml.safe_load((root / "docs/engines/deterministic-case-bindings.yaml").read_text(encoding="utf-8"))
    basis = yaml.safe_load((root / "docs/v3-constitutional-test-basis.yaml").read_text(encoding="utf-8"))
    command_results, command_errors = execute_deterministic_commands(matrix, root)
    errors = command_errors + validate(gate, gate.get("portfolio_cases", []), uc_source.get("cases", []),
                                       root, matrix, bindings.get("cases", []), basis, command_results)
    probe = [{"id": "probe-a", "vector": {"operation": "read", "auth": "same"}, "expected": "allow"},
             {"id": "probe-b", "vector": {"operation": "read", "auth": "same"}, "expected": "block"}]
    if len(contradictions(probe)) != 1:
        errors.append("contradiction detector failed its negative probe")
    altered = yaml.safe_load(yaml.safe_dump(gate))
    dual = next((item for item in altered.get("dual_capabilities", []) if item.get("mode", "dual") == "dual"), None)
    if dual and dual.get("vectors"):
        dual["vectors"][0]["deterministic_expected"] = "synthetic-unilateral-change"
        if not any("route outcomes diverge" in item or "route expectation" in item
                   for item in validate(altered, altered.get("portfolio_cases", []), uc_source.get("cases", []),
                                        root, matrix, bindings.get("cases", []), basis, command_results)):
            errors.append("dual-route parity gate failed its unilateral-mutation probe")
    else:
        errors.append("quality gate has no dual-route capability to exercise its negative probe")
    if errors:
        print(f"validate_v3_quality_gates: FAILED - {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print(f"validate_v3_quality_gates: OK - {len(gate.get('cases', []))} CRUD UCs, "
          f"{len(gate.get('portfolio_cases', []))} engine/fixture cases, "
          f"{len(command_results)} deterministic commands executed, contradiction and dual-route probes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
