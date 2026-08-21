#!/usr/bin/env python3
"""Verify the canonical skill package lock without hashing the lock itself."""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

import yaml


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    lock_path = root / "skill/package-lock.yaml"
    errors: list[str] = []
    try:
        lock = yaml.safe_load(lock_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"validate_skill_package: FAILED — cannot read lock ({exc})")
        return 1
    package = lock.get("package", {}) if isinstance(lock, dict) else {}
    files = package.get("files", []) if isinstance(package, dict) else []
    if package.get("version") != "1.2.0":
        errors.append("package-lock: package.version must be 1.2.0")
    if package.get("hash_algorithm") != "sha256":
        errors.append("package-lock: package.hash_algorithm must be sha256")
    expected: dict[str, str] = {}
    for item in files:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str) or not isinstance(item.get("sha256"), str):
            errors.append("package-lock: every files entry needs path and sha256")
            continue
        expected[item["path"]] = item["sha256"]
    actual = {
        path.relative_to(root / "skill").as_posix(): digest(path)
        for path in (root / "skill").rglob("*")
        if path.is_file() and path.name != "package-lock.yaml"
    }
    if set(expected) != set(actual):
        errors.append("package-lock: file set differs from skill package")
    for relative, value in actual.items():
        if expected.get(relative) != value:
            errors.append(f"package-lock: hash mismatch for {relative}")
    if errors:
        print(f"validate_skill_package: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_skill_package: OK — package files and hashes match")
    return 0


if __name__ == "__main__":
    sys.exit(main())
