#!/usr/bin/env python3
"""Validate the declared boundary registry for deterministic checks."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED = (
    "Deterministic coverage",
    "Outside the validator",
    "Current mechanism",
    "A missing barrier is reported as a",
    "not have a universal runtime enforcement layer",
    "verification-boundaries.yaml",
    "Every new verification declares its input boundary",
)
SCRIPTS = (
    "validate_hipocampo.py",
    "validate_contracts.py",
    "validate_skill_package.py",
    "validate_compatibility.py",
    "validate_change.py",
    "validate_skill_docs.py",
    "validate_verification_boundaries.py",
    "validate_validation_loop.py",
    "validate_enforcement_policy.py",
    "validate_nominal_citations.py",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    text = (root / "docs" / "verification-boundaries.md").read_text(encoding="utf-8")
    errors = [f"registry missing {snippet!r}" for snippet in REQUIRED if snippet not in text]
    errors.extend(
        f"registry names missing script {script!r}"
        for script in SCRIPTS
        if script not in text or not (root / "scripts" / script).is_file()
    )
    if errors:
        print(f"validate_boundaries: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_boundaries: OK — declared coverage and limits are present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
