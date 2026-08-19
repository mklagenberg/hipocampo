#!/usr/bin/env python3
"""Validate Hipocampo Change Sets (`changes/<id>/impact.yaml`) against their
own schema and, on a PR, against the actual diff.

Hipocampo adopted MODA's Change Set mechanism *adapted*, not copied
(decisions/0031-change-set-mechanism.md) -- the real `impact.yaml` schema in
use across every existing Change Set is:

    change_set:
      id: str            # must match the changes/<id>/ directory name
      class: editorial | operational | normative
      semver: major | minor | patch | none
      status: proposed | accepted | implemented | superseded
      backfill: bool
      decisions: [str]   # paths, must exist

    impact:
      - artifact: str    # free-text description, sometimes several paths
        status: updated | reviewed | not-applicable
        note: str        # non-empty; required for every status

    validation:
      commands: [str]    # non-empty
      evidence: [str]
      notes: str

This is NOT MODA's own `{change, git, triggers, affected, validation}`
schema -- see decisions/0031 for why the trigger table and top-level shape
were deliberately adapted rather than copied. A validator built against
MODA's literal schema would reject every real Hipocampo Change Set.

Two things are checked:

  1. Structural validity of every impact.yaml under changes/ -- required
     keys, valid enums, id/directory match, decisions/evidence paths exist,
     sibling proposal.md exists, every impact[] entry has a non-empty note.

  2. Diff coverage (PR mode only, --base/--head): docs/change-management.md
     already documents that "No deterministic validation compares this
     against the actual diff yet" -- this is that check. Every changed file
     under a protected prefix (SPEC.md, decisions/, skill/, scaffold/,
     docs/, CHANGELOG.md, UPGRADE.md, MIGRATIONS.md, moda.yaml,
     conformance/) must be covered by an `updated` entry in at least one
     changes/*/impact.yaml touched by the same diff. Coverage is matched
     heuristically -- each `artifact` string is scanned for path-like
     tokens (Hipocampo's schema keeps `artifact` as free text, sometimes
     several comma-separated paths in one string, unlike MODA's structured
     `paths: [...]` list) -- this is looser than MODA's own check by
     construction, not an oversight; tightening it would mean changing the
     schema itself, a separate decision.

Requires PyYAML (this is the one script in scripts/ that does; the nested
list-of-mappings shape of impact.yaml is not realistically regex-parseable
the way scripts/validate_hipocampo.py's flat markdown checks are).

A handful of `changes/*/impact.yaml` predate this validator and predate the
schema above converging on its current shape (decisions/0031 describes
iterative adoption, not one atomic cutover), or are pt-BR/EN redirect
stubs for a renamed directory (comment-only YAML, same "a document is never
physically deleted" convention SPEC.md section 8 states for other document
types). Rewriting them to fit today's schema would violate
docs/change-management.md's own rule -- "Accepted Change Sets remain as
traceability evidence -- never edited after acceptance, only superseded" --
so GRANDFATHERED below exempts them from structural validation instead
(their proposal.md/decisions/enum shape is frozen as accepted history). Any
new Change Set is NOT eligible for this list; full validation applies to
everything created after this validator's introduction (0050).

Usage:
    python3 scripts/validate_change.py --root . [--base REF --head REF]
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import yaml

CLASSES = {"editorial", "operational", "normative"}
SEMVER = {"major", "minor", "patch", "none"}
STATUSES = {"proposed", "accepted", "implemented", "superseded"}
IMPACT_STATUSES = {"updated", "reviewed", "not-applicable"}

PROTECTED_PREFIXES = (
    "SPEC.md", "CHANGELOG.md", "UPGRADE.md", "MIGRATIONS.md", "moda.yaml",
    "decisions/", "skill/", "scaffold/", "docs/", "conformance/",
)

PATH_TOKEN_RE = re.compile(r"[\w.\-]+(?:/[\w.\-]+)+|[\w.\-]+\.(?:md|yaml|yml|py)")

# Change Sets that already existed when this validator (0050) was introduced,
# predating the schema's current shape or kept as pt-BR/EN redirect stubs for a
# renamed directory. See the module docstring for why these are grandfathered
# rather than rewritten. This list is intentionally frozen -- do not add to it
# for a Change Set created after 0050; those get full validation.
GRANDFATHERED = frozenset({
    "0026-0028-fact-account-opinion-memory-taxonomy-and-cross-repo-lifecycle",
    "0026-0028-taxonomia-fato-relato-opiniao-e-ciclo-de-vida",
    "0032-0033-scaffolding-and-vault-manifest",
    "0032-0033-scaffolding-e-manifesto-vault",
    "0034-repository-and-vault-language-policy",
    "0035-controlled-vocabulary-dictionary",
})


def path_matches(changed: str, prefix: str) -> bool:
    return changed == prefix or (prefix.endswith("/") and changed.startswith(prefix))


def load_impact(path: Path, errors: list[str]) -> dict:
    rel = str(path)
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        errors.append(f"{rel}: invalid YAML ({exc})")
        return {}
    if not isinstance(data, dict):
        errors.append(f"{rel}: root must be a mapping")
        return {}
    return data


def load_impact_lenient(path: Path) -> dict:
    """Best-effort load for a grandfathered impact.yaml -- no errors raised.

    Comment-only redirect stubs parse to None (not a mapping); pre-0050
    schemas parse fine but wouldn't pass validate_structure's checks. Either
    way this is only used for diff-coverage token matching if a grandfathered
    file is ever touched again, not for pass/fail structural validation.
    """
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def validate_structure(root: Path, impact_path: Path, errors: list[str]) -> dict:
    rel = impact_path.relative_to(root).as_posix()
    data = load_impact(impact_path, errors)
    if not data:
        return {}

    if set(data) != {"change_set", "impact", "validation"}:
        errors.append(
            f"{rel}: top-level keys must be exactly change_set/impact/validation, "
            f"got {sorted(data)}"
        )

    if not (impact_path.parent / "proposal.md").is_file():
        errors.append(f"{rel}: missing sibling proposal.md")

    cs = data.get("change_set", {})
    if not isinstance(cs, dict):
        errors.append(f"{rel}: change_set must be a mapping")
        cs = {}
    required_cs = {"id", "class", "semver", "status", "backfill", "decisions"}
    for key in sorted(required_cs - cs.keys()):
        errors.append(f"{rel}: change_set.{key} is missing")
    if cs.get("id") != impact_path.parent.name:
        errors.append(
            f"{rel}: change_set.id ({cs.get('id')!r}) must match its directory "
            f"name ({impact_path.parent.name!r})"
        )
    if cs.get("class") not in CLASSES:
        errors.append(f"{rel}: change_set.class {cs.get('class')!r} not in {sorted(CLASSES)}")
    if cs.get("semver") not in SEMVER:
        errors.append(f"{rel}: change_set.semver {cs.get('semver')!r} not in {sorted(SEMVER)}")
    if cs.get("status") not in STATUSES:
        errors.append(f"{rel}: change_set.status {cs.get('status')!r} not in {sorted(STATUSES)}")
    if not isinstance(cs.get("backfill"), bool):
        errors.append(f"{rel}: change_set.backfill must be a boolean")
    decisions = cs.get("decisions")
    if not isinstance(decisions, list) or not decisions:
        errors.append(f"{rel}: change_set.decisions must be a non-empty list")
    else:
        for d in decisions:
            if not isinstance(d, str) or not (root / d).is_file():
                errors.append(f"{rel}: change_set.decisions entry {d!r} does not exist")

    impact_list = data.get("impact")
    if not isinstance(impact_list, list) or not impact_list:
        errors.append(f"{rel}: impact must be a non-empty list")
        impact_list = []
    for i, item in enumerate(impact_list):
        loc = f"{rel}: impact[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{loc} must be a mapping")
            continue
        if set(item) != {"artifact", "status", "note"}:
            errors.append(f"{loc}: keys must be exactly artifact/status/note, got {sorted(item)}")
        if not isinstance(item.get("artifact"), str) or not item["artifact"].strip():
            errors.append(f"{loc}: artifact must be a non-empty string")
        if item.get("status") not in IMPACT_STATUSES:
            errors.append(f"{loc}: status {item.get('status')!r} not in {sorted(IMPACT_STATUSES)}")
        if not isinstance(item.get("note"), str) or not item["note"].strip():
            errors.append(f"{loc}: note must be a non-empty string")

    validation = data.get("validation")
    if not isinstance(validation, dict):
        errors.append(f"{rel}: validation must be a mapping")
        validation = {}
    commands = validation.get("commands")
    if not isinstance(commands, list) or not commands or any(
        not isinstance(c, str) or not c.strip() for c in commands
    ):
        errors.append(f"{rel}: validation.commands must be a non-empty list of non-empty strings")
    evidence = validation.get("evidence")
    if not isinstance(evidence, list) or any(not isinstance(e, str) for e in evidence):
        errors.append(f"{rel}: validation.evidence must be a list of strings")
    if not isinstance(validation.get("notes"), str) or not validation["notes"].strip():
        errors.append(f"{rel}: validation.notes must be a non-empty string")

    return data


def find_all_impacts(root: Path) -> list[Path]:
    changes_dir = root / "changes"
    if not changes_dir.is_dir():
        return []
    return sorted(changes_dir.glob("*/impact.yaml"))


def git_changed_files(root: Path, base: str, head: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", base, head],
        cwd=root, check=False, capture_output=True, text=True,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "git diff failed")
    return [line for line in result.stdout.splitlines() if line]


def extract_path_tokens(text: str) -> set[str]:
    return set(PATH_TOKEN_RE.findall(text))


def check_diff_coverage(
    root: Path, changed: list[str], all_data: dict[Path, dict], errors: list[str]
) -> None:
    changed_impacts = [
        p for p in all_data
        if p.relative_to(root).as_posix() in changed
    ]
    protected_changed = [
        c for c in changed
        if not c.startswith("changes/") and any(path_matches(c, p) for p in PROTECTED_PREFIXES)
    ]
    if not protected_changed:
        return
    if not changed_impacts:
        errors.append(
            "diff touches protected paths ("
            + ", ".join(sorted(protected_changed))
            + ") but no changes/*/impact.yaml is part of this diff -- missing Change Set"
        )
        return

    covered_tokens: set[str] = set()
    for path, data in all_data.items():
        if path not in changed_impacts:
            continue
        for item in data.get("impact", []):
            if isinstance(item, dict) and item.get("status") == "updated":
                covered_tokens |= extract_path_tokens(str(item.get("artifact", "")))

    for c in sorted(protected_changed):
        if not any(path_matches(c, token) or c == token for token in covered_tokens):
            errors.append(
                f"'{c}' changed but is not covered by an 'updated' impact[] entry in any "
                f"Change Set touched by this diff"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument("--base", help="base ref for diff coverage (PR mode)")
    parser.add_argument("--head", default="HEAD", help="head ref for diff coverage")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors: list[str] = []

    impacts = find_all_impacts(root)
    all_data: dict[Path, dict] = {}
    for impact_path in impacts:
        if impact_path.parent.name in GRANDFATHERED:
            all_data[impact_path] = load_impact_lenient(impact_path)
        else:
            all_data[impact_path] = validate_structure(root, impact_path, errors)

    if args.base:
        try:
            changed = git_changed_files(root, args.base, args.head)
        except RuntimeError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        check_diff_coverage(root, changed, all_data, errors)

    if not args.quiet or errors:
        if errors:
            print(f"ERRORS ({len(errors)}):")
            for e in errors:
                print(f"  [FAIL] {e}")
            print()

    if errors:
        print(f"validate_change: FAILED — {len(errors)} error(s)")
        return 1

    print(f"validate_change: OK — {len(impacts)} Change Set(s) checked, 0 errors")
    return 0


if __name__ == "__main__":
    sys.exit(main())
