#!/usr/bin/env python3
"""Validate the bounded connector preflight matrix and synthetic fixtures."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ALLOWED_DECISIONS = {"allow_read", "allow_after_explicit_request", "block_until_tested"}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors: list[str] = []
    try:
        matrix = yaml.safe_load((root / "docs" / "connector-preflight.yaml").read_text(encoding="utf-8"))
        fixtures = yaml.safe_load((root / "docs" / "connector-preflight-fixtures.yaml").read_text(encoding="utf-8"))["fixtures"]
    except (OSError, KeyError, yaml.YAMLError) as exc:
        print(f"validate_connector_preflight: FAILED — {exc}")
        return 1
    if matrix.get("host") != "codex-local" or matrix.get("identity") != "local-agent-session":
        errors.append("matrix must identify the bounded local host and session")
    operations = matrix.get("operations", [])
    if not operations:
        errors.append("matrix operations are empty")
    for operation in operations:
        if operation.get("decision") not in ALLOWED_DECISIONS:
            errors.append(f"{operation.get('id')}: unsupported decision")
        if operation.get("status") == "not_tested" and operation.get("decision") != "block_until_tested":
            errors.append(f"{operation.get('id')}: untested capability was not blocked")
        if operation.get("status") == "not_tested" and operation.get("evidence") is not None:
            errors.append(f"{operation.get('id')}: untested capability has evidence")
    for fixture in fixtures:
        if fixture.get("status") in {"not_tested", "unavailable", "declared_only"} and fixture.get("decision") != "block_until_tested":
            errors.append(f"fixture {fixture.get('id')}: unsafe decision for unverified state")
    if errors:
        print(f"validate_connector_preflight: FAILED — {len(errors)} error(s)")
        for error in errors: print(f"  [FAIL] {error}")
        return 1
    print(f"validate_connector_preflight: OK — {len(operations)} operations, {len(fixtures)} fixtures")
    return 0

if __name__ == "__main__":
    sys.exit(main())
