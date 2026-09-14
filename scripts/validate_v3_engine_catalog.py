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
    errors: list[str] = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"validate_v3_engine_catalog: FAILED — {exc}")
        return 1
    if not isinstance(data, dict) or data.get("policy", {}).get("privacy") != "sanitized-no-real-content":
        errors.append("catalog policy must declare sanitized-no-real-content")
    engines = data.get("engines", []) if isinstance(data, dict) else []
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
    if ids != EXPECTED_ENGINES:
        errors.append(f"engine set mismatch: expected {sorted(EXPECTED_ENGINES)}, got {sorted(ids)}")
    if errors:
        print(f"validate_v3_engine_catalog: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print(f"validate_v3_engine_catalog: OK — {len(engines)} logical engines with deterministic and semantic cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
