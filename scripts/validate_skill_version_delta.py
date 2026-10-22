#!/usr/bin/env python3
"""Require a new independent skill version when bundled skill bytes change."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

import yaml

from v3_channel import parse_version


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True,
        encoding="utf-8", check=False,
    )
    if result.returncode:
        raise ValueError(result.stderr.strip() or "git command failed")
    return result.stdout


def _manifest_version(root: Path, ref: str) -> str:
    document = yaml.safe_load(_git(root, "show", f"{ref}:skill/manifest.yaml"))
    if not isinstance(document, dict) or not isinstance(document.get("skill"), dict):
        raise ValueError(f"{ref}: skill manifest is invalid")
    version = document["skill"].get("version")
    if not isinstance(version, str) or parse_version(version) is None:
        raise ValueError(f"{ref}: skill version is invalid")
    return version


def _prerelease_cmp(left: tuple[str, ...], right: tuple[str, ...]) -> int:
    if not left:
        return 0 if not right else 1
    if not right:
        return -1
    for a, b in zip(left, right):
        if a == b:
            continue
        if a.isdigit() and b.isdigit():
            return (int(a) > int(b)) - (int(a) < int(b))
        if a.isdigit():
            return -1
        if b.isdigit():
            return 1
        return (a > b) - (a < b)
    return (len(left) > len(right)) - (len(left) < len(right))


def _version_increases(previous: str, current: str) -> bool:
    old = parse_version(previous)
    new = parse_version(current)
    if old is None or new is None:
        return False
    if new[0] != old[0]:
        return new[0] > old[0]
    return _prerelease_cmp(new[1], old[1]) > 0


def validate_delta(changed_paths: list[str], previous: str, current: str) -> list[str]:
    bundled = sorted(path for path in changed_paths
                     if path.startswith("skill/") and path != "skill/package-lock.yaml")
    if not bundled:
        return []
    if not _version_increases(previous, current):
        return [f"bundled skill files changed ({', '.join(bundled)}), but "
                f"skill version did not increase: {previous} -> {current}"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    try:
        paths = _git(root, "diff", "--name-only", "--no-renames",
                     args.base, args.head, "--", "skill").splitlines()
        if not any(path.startswith("skill/") and path != "skill/package-lock.yaml"
                   for path in paths):
            print("validate_skill_version_delta: OK — no bundled skill change")
            return 0
        errors = validate_delta(paths, _manifest_version(root, args.base),
                                _manifest_version(root, args.head))
    except (ValueError, yaml.YAMLError) as exc:
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(f"  [FAIL] {error}")
        print("validate_skill_version_delta: FAILED")
        return 1
    print("validate_skill_version_delta: OK — bundled skill version increased")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
