#!/usr/bin/env python3
"""Validate the logical V3 engine catalog and per-engine test assignments."""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml


EXPECTED_ENGINES = {
    "crud", "artifact-provenance", "ingress", "rem-curation", "package",
    "delivery-transfer", "governance", "operational-audit",
    "migration-compatibility", "maintenance", "learning-evolution",
    "search-progressive-disclosure",
}
REVIEW_BOUNDARIES = {
    "human-semantic-review", "explicit-human-decision", "REM-or-human-review",
    "host-or-human-review", "research-or-human-review",
}
DISPOSITIONS = {"accepted", "provisional", "needs_review", "blocked", "partial", "rework_required"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    path = root / "docs/engines/test-matrix.yaml"
    bindings_path = root / "docs/engines/deterministic-case-bindings.yaml"
    basis_path = root / "docs/v3-constitutional-test-basis.yaml"
    errors: list[str] = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        bindings_data = yaml.safe_load(bindings_path.read_text(encoding="utf-8"))
        basis_data = yaml.safe_load(basis_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"validate_v3_engine_catalog: FAILED — {exc}")
        return 1
    if not isinstance(data, dict) or data.get("policy", {}).get("privacy") != "sanitized-no-real-content":
        errors.append("catalog policy must declare sanitized-no-real-content")
    engines = data.get("engines", []) if isinstance(data, dict) else []
    bindings = bindings_data.get("cases", []) if isinstance(bindings_data, dict) else []
    binding_map: dict[tuple[str, str], dict] = {}
    for index, binding in enumerate(bindings):
        if not isinstance(binding, dict):
            errors.append(f"bindings[{index}] must be a mapping")
            continue
        key = (str(binding.get("engine")), str(binding.get("id")))
        if key in binding_map:
            errors.append(f"duplicate deterministic binding: {key[0]}/{key[1]}")
        binding_map[key] = binding
        for field in ("id", "engine", "assertion_id", "assertion"):
            if not isinstance(binding.get(field), str) or not binding[field].strip():
                errors.append(f"bindings[{index}].{field} must be non-empty")
    basis_cases = basis_data.get("cases", []) if isinstance(basis_data, dict) else []
    basis_map = {item.get("case_id"): item for item in basis_cases if isinstance(item, dict)}
    if not isinstance(engines, list):
        errors.append("engines must be a list")
        engines = []
    ids: set[str] = set()
    for index, engine in enumerate(engines):
        label = f"engines[{index}]"
        if not isinstance(engine, dict):
            errors.append(f"{label} must be a mapping")
            continue
        engine_id = engine.get("id")
        if engine_id in ids:
            errors.append(f"{label} duplicates engine id {engine_id!r}")
        ids.add(engine_id)
        for field in ("id", "name", "contract", "write_boundary"):
            if not isinstance(engine.get(field), str) or not engine[field].strip():
                errors.append(f"{label}.{field} must be non-empty")
        if not (root / str(engine.get("contract", ""))).is_file():
            errors.append(f"{label} contract does not exist: {engine.get('contract')}")
        modules = engine.get("modules")
        if not isinstance(modules, list) or not modules:
            errors.append(f"{label}.modules must be non-empty")
        else:
            for module in modules:
                if not (root / module).is_file():
                    errors.append(f"{label} module does not exist: {module}")
        commands = engine.get("deterministic_commands")
        if not isinstance(commands, list) or not commands or any(not isinstance(item, str) or not item.strip() for item in commands):
            errors.append(f"{label}.deterministic_commands must be non-empty")
        deterministic = engine.get("deterministic_cases")
        if not isinstance(deterministic, list) or len(deterministic) < 2:
            errors.append(f"{label} needs at least two deterministic cases")
        else:
            for case_id in deterministic:
                binding = binding_map.get((engine_id, str(case_id)))
                if binding is None:
                    errors.append(f"{label} deterministic case has no executable binding: {case_id}")
                elif not isinstance(binding.get("command_index"), int) or not 0 <= binding["command_index"] < len(engine.get("deterministic_commands", [])):
                    errors.append(f"{label} deterministic binding has invalid command index: {case_id}")
        semantic = engine.get("semantic_cases")
        if not isinstance(semantic, list) or len(semantic) < 2:
            errors.append(f"{label} needs at least two semantic cases")
        else:
            for case_index, case in enumerate(semantic):
                case_label = f"{label}.semantic_cases[{case_index}]"
                if not isinstance(case, dict):
                    errors.append(f"{case_label} must be a mapping")
                    continue
                for field in ("id", "fixture_ref", "expected_disposition", "review_boundary"):
                    if not isinstance(case.get(field), str) or not case[field].strip():
                        errors.append(f"{case_label}.{field} must be non-empty")
                if case.get("expected_disposition") not in DISPOSITIONS:
                    errors.append(f"{case_label} has unknown disposition")
                if case.get("review_boundary") not in REVIEW_BOUNDARIES:
                    errors.append(f"{case_label} has unknown review boundary")
                basis = basis_map.get(case.get("id"))
                if basis is None:
                    errors.append(f"{case_label} has no constitutional basis")
                else:
                    if basis.get("expected_disposition") != case.get("expected_disposition"):
                        errors.append(f"{case_label} disposition differs from constitutional basis")
                    if not isinstance(basis.get("constitution_refs"), list) or not basis["constitution_refs"]:
                        errors.append(f"{case_label} has no Constitution references")
                    if not isinstance(basis.get("decision_refs"), list) or not basis["decision_refs"]:
                        errors.append(f"{case_label} has no Decision Record references")
    if ids != EXPECTED_ENGINES:
        errors.append(f"engine set mismatch: expected {sorted(EXPECTED_ENGINES)}, got {sorted(ids)}")
    expected_binding_keys = {(engine["id"], str(case_id)) for engine in engines for case_id in engine.get("deterministic_cases", [])}
    if set(binding_map) != expected_binding_keys:
        missing = sorted(expected_binding_keys - set(binding_map))
        extra = sorted(set(binding_map) - expected_binding_keys)
        errors.append(f"deterministic binding coverage mismatch: missing={missing}, extra={extra}")
    expected_semantic_ids = {case.get("id") for engine in engines for case in engine.get("semantic_cases", []) if isinstance(case, dict)}
    if set(basis_map) != expected_semantic_ids:
        missing = sorted(expected_semantic_ids - set(basis_map))
        extra = sorted(set(basis_map) - expected_semantic_ids)
        errors.append(f"constitutional basis coverage mismatch: missing={missing}, extra={extra}")
    if errors:
        print(f"validate_v3_engine_catalog: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print(f"validate_v3_engine_catalog: OK — {len(engines)} logical engines with deterministic and semantic cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
