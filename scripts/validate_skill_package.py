#!/usr/bin/env python3
"""Verify the canonical skill package lock without hashing the lock itself."""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path, PurePosixPath

import yaml


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(root: Path) -> list[str]:
    root = root.resolve()
    lock_path = root / "skill/package-lock.yaml"
    errors: list[str] = []
    try:
        lock = yaml.safe_load(lock_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [f"cannot read lock ({exc})"]
    try:
        manifest = yaml.safe_load((root / "skill/manifest.yaml").read_text(encoding="utf-8"))
        contract = yaml.safe_load((root / "COMPATIBILITY.yaml").read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [f"cannot read package tuple ({exc})"]
    if not isinstance(manifest, dict) or not isinstance(contract, dict):
        return ["manifest and compatibility contract must be mappings"]
    if not isinstance(manifest.get("skill"), dict) or not isinstance(contract.get("skill"), dict):
        return ["manifest and compatibility skill declarations must be mappings"]
    package = lock.get("package", {}) if isinstance(lock, dict) else {}
    files = package.get("files", []) if isinstance(package, dict) else []
    declared_version = manifest.get("skill", {}).get("version")
    required_version = contract.get("skill", {}).get("required_version")
    if not isinstance(declared_version, str) or not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", declared_version):
        errors.append("manifest skill.version must be a valid version")
    if package.get("version") != declared_version or declared_version != required_version:
        errors.append("package-lock, manifest and required skill versions must match")
    if manifest.get("skill", {}).get("core_path") != "skill/":
        errors.append("canonical package core_path must be skill/")
    if package.get("hash_algorithm") != "sha256":
        errors.append("package-lock: package.hash_algorithm must be sha256")
    expected: dict[str, str] = {}
    if not isinstance(files, list) or not files:
        return errors + ["package-lock: files must be a non-empty list"]
    for item in files:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str) or not isinstance(item.get("sha256"), str):
            errors.append("package-lock: every files entry needs path and sha256")
            continue
        relative = item["path"]
        if (not relative or "\\" in relative or ":" in relative
                or PurePosixPath(relative).is_absolute() or ".." in PurePosixPath(relative).parts
                or PurePosixPath(relative).as_posix() != relative or relative == "package-lock.yaml"):
            errors.append(f"package-lock: unsafe or non-canonical path {relative!r}")
            continue
        if relative in expected:
            errors.append(f"package-lock: duplicate path {relative}")
        if not re.fullmatch(r"[0-9a-f]{64}", item["sha256"]):
            errors.append(f"package-lock: invalid sha256 for {relative}")
        expected[relative] = item["sha256"]
    symlinks = [path for path in (root / "skill").rglob("*") if path.is_symlink()]
    if symlinks:
        return errors + ["skill package may not contain symlinks"]
    actual = {
        path.relative_to(root / "skill").as_posix(): digest(path)
        for path in (root / "skill").rglob("*")
        if path.is_file() and path != lock_path
    }
    if set(expected) != set(actual):
        errors.append("package-lock: file set differs from skill package")
    for relative, value in actual.items():
        if expected.get(relative) != value:
            errors.append(f"package-lock: hash mismatch for {relative}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    errors = validate(Path(args.root))
    if errors:
        print(f"validate_skill_package: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_skill_package: OK — package files and hashes match")
    return 0


if __name__ == "__main__":
    sys.exit(main())
