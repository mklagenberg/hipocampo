#!/usr/bin/env python3
"""Deterministic consistency checks between skill/ router prose and the
scaffold profiles it describes.

Found during a v2.0.0 personal-skill revalidation (2026-08-19): the generic
skill's own router (`skill/SKILL.md`) and reference files
(`skill/references/*.md`) sometimes describe a file path or a schema field
in prose that does not match what `scaffold/profiles/*.yaml` (the actual
source of truth) declares. Two concrete instances motivated this script:

  1. `skill/SKILL.md` cited the scaffold-generated example output as
     `example/example-note.md`; the real profiles declare
     `example/exemplo-nota.md`.
  2. `skill/references/instantiation.md`'s own worked example still wrote
     `hipocampo.yaml` with the pre-v2.0.0 `domain:` field, superseded by
     `entity`/`role`/`scope_description` (decisions/0040, decisions/0041).

Check 1 (path consistency): every `example/...` path literal (backtick or
plain) mentioned anywhere under `skill/` must match a `path:` value actually
declared in an `outputs:` entry of `scaffold/profiles/*.yaml`.

Check 2 (superseded-field usage): no file under `skill/` may show `domain:`
as a `hipocampo.yaml` field in an example -- that field was fully superseded
in v2.0.0 (decisions/0041) and should never appear in fresh skill guidance.

No third-party dependencies -- stdlib only, consistent with
scripts/validate_hipocampo.py.

Usage:
    python3 scripts/validate_skill_docs.py [--root PATH] [--quiet]

Exit code: 0 when there are no errors; 1 when at least one error was found.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXAMPLE_PATH_RE = re.compile(r"\bexample/[\w.\-]+\.md\b")
OUTPUT_PATH_RE = re.compile(r'-\s*path:\s*"([^"]+)"')
DOMAIN_FIELD_RE = re.compile(r"`domain:\s*[^`]+`")


def collect_declared_outputs(root: Path, errors: list[str]) -> set[str]:
    profiles_dir = root / "scaffold" / "profiles"
    if not profiles_dir.is_dir():
        errors.append("scaffold/profiles/ directory not found — cannot verify example paths")
        return set()

    declared: set[str] = set()
    for path in sorted(profiles_dir.glob("*.yaml")):
        text = path.read_text(encoding="utf-8")
        declared.update(OUTPUT_PATH_RE.findall(text))
    if not declared:
        errors.append("scaffold/profiles/*.yaml: no 'outputs' paths found — profile format may have changed")
    return declared


def iter_skill_files(root: Path):
    skill_dir = root / "skill"
    if not skill_dir.is_dir():
        return
    for path in sorted(skill_dir.rglob("*.md")):
        yield path
    yaml_path = skill_dir / "manifest.yaml"
    if yaml_path.exists():
        yield yaml_path


def check_example_paths(root: Path, declared_outputs: set[str], errors: list[str]) -> None:
    example_outputs = {p for p in declared_outputs if p.startswith("example/")}
    for path in iter_skill_files(root):
        rel = path.relative_to(root)
        text = path.read_text(encoding="utf-8")
        for match in EXAMPLE_PATH_RE.finditer(text):
            literal = match.group(0)
            if example_outputs and literal not in example_outputs:
                errors.append(
                    f"{rel}: cites '{literal}', but scaffold/profiles/*.yaml's declared "
                    f"outputs use {sorted(example_outputs)} — router prose has drifted "
                    f"from the real profile"
                )


def check_superseded_domain_field(root: Path, errors: list[str]) -> None:
    for path in iter_skill_files(root):
        rel = path.relative_to(root)
        text = path.read_text(encoding="utf-8")
        for match in DOMAIN_FIELD_RE.finditer(text):
            errors.append(
                f"{rel}: example shows {match.group(0)} — 'domain' was superseded by "
                f"'entity'/'role'/'scope_description' in v2.0.0 (decisions/0041); no "
                f"skill guidance should demonstrate the pre-v2.0.0 field"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository root (default: current directory)")
    parser.add_argument("--quiet", action="store_true", help="only print output when there are errors")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors: list[str] = []

    declared_outputs = collect_declared_outputs(root, errors)
    check_example_paths(root, declared_outputs, errors)
    check_superseded_domain_field(root, errors)

    if not args.quiet or errors:
        if errors:
            print(f"ERRORS ({len(errors)}):")
            for e in errors:
                print(f"  [FAIL] {e}")
            print()

    if errors:
        print(f"validate_skill_docs: FAILED — {len(errors)} error(s)")
        return 1

    print("validate_skill_docs: OK — 0 errors")
    return 0


if __name__ == "__main__":
    sys.exit(main())
