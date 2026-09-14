#!/usr/bin/env python3
"""Execute the logical V3 engine matrix and validate semantic references."""
from __future__ import annotations

import argparse
import shlex
import subprocess
from pathlib import Path

import yaml


ALLOWED_BOUNDARIES = {
    "human-semantic-review", "explicit-human-decision", "REM-or-human-review",
    "host-or-human-review", "research-or-human-review",
}


def load_fixture(root: Path, reference: str) -> dict:
    filename, separator, case_id = reference.partition("#")
    if not separator or not case_id:
        raise ValueError(f"semantic fixture reference must use file#case-id: {reference}")
    data = yaml.safe_load((root / "docs" / filename).read_text(encoding="utf-8"))
    for case in data.get("cases", []):
        if case.get("id") == case_id:
            return case
    raise ValueError(f"semantic fixture case not found: {reference}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    matrix_path = root / "docs/engines/test-matrix.yaml"
    matrix = yaml.safe_load(matrix_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    command_count = 0
    deterministic_case_count = 0
    semantic_case_count = 0

    for engine in matrix.get("engines", []):
        engine_id = engine["id"]
        deterministic_cases = engine.get("deterministic_cases", [])
        deterministic_case_count += len(deterministic_cases)
        semantic_cases = engine.get("semantic_cases", [])
        semantic_case_count += len(semantic_cases)
        for command in engine.get("deterministic_commands", []):
            command_count += 1
            try:
                argv = shlex.split(command)
                result = subprocess.run(argv, cwd=root, capture_output=True, text=True, check=False)
            except (OSError, ValueError) as exc:
                errors.append(f"{engine_id}: could not execute {command!r}: {exc}")
                continue
            if result.returncode != 0:
                output = (result.stdout + result.stderr).strip().replace("\n", " | ")
                errors.append(f"{engine_id}: command failed: {command} ({output})")
        for case in semantic_cases:
            if case.get("review_boundary") not in ALLOWED_BOUNDARIES:
                errors.append(f"{engine_id}: invalid semantic review boundary")
            try:
                fixture = load_fixture(root, case["fixture_ref"])
            except (OSError, yaml.YAMLError, ValueError, KeyError) as exc:
                errors.append(f"{engine_id}/{case.get('id')}: {exc}")
                continue
            if not fixture.get("review_boundary"):
                errors.append(f"{engine_id}/{case.get('id')}: fixture has no review boundary")

    if errors:
        print(f"validate_v3_engine_suite: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print(
        "validate_v3_engine_suite: OK — "
        f"{command_count} deterministic commands executed, "
        f"{deterministic_case_count} deterministic cases assigned, "
        f"{semantic_case_count} semantic cases review-bound"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
