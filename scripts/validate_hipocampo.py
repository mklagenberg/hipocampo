#!/usr/bin/env python3
"""Deterministic structural validation for the Hipocampo methodology repository.

Implements the four checks scoped by the MODA self-audit
(`audits/moda/2026-08-17-v1.0.0-self-audit.md`, "Onda 3 — Validacao
deterministica") and `decisions/0036-deterministic-validation-and-release-gate.md`:

  1. Every file in `decisions/` follows the Decision Record template, or is a
     valid bilingual redirect stub pointing at an existing target.
  2. Every internal (repo-relative) markdown link resolves to a real file,
     and, when it points at a heading anchor, the anchor matches a real
     heading in the target (computed with GitHub's own slug algorithm).
  3. The version declared in `README.md` ("Current version: **X.Y.Z**")
     matches the latest formally released section in `CHANGELOG.md`
     ("## [X.Y.Z]" — the first version heading, `[Unreleased]` skipped).
  4. Coverage report only, never a failure: every top-level field declared
     in `SPEC.md` section 2's frontmatter schema is checked for at least one
     mention across `decisions/*.md` (canonical, English files only).

No third-party dependencies — stdlib only, so this runs on a bare
`python3` in CI with no install step.

Usage:
    python3 scripts/validate_hipocampo.py [--root PATH] [--quiet]

Exit code: 0 when there are no errors (warnings/coverage notes never fail
the build); 1 when at least one error was found.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# Shared helpers
# --------------------------------------------------------------------------

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.MULTILINE)
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE_RE = re.compile(r"^```", re.MULTILINE)

# Root-relative directories never worth scanning for markdown files.
SKIP_DIRS = {".git", "node_modules"}


def slugify(heading: str) -> str:
    """GitHub's heading-anchor algorithm: lowercase, strip anything that
    isn't a word char / space / hyphen, collapse whitespace to hyphens."""
    text = heading.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", "-", text)
    return text


def strip_code_fences(text: str) -> str:
    """Blank out fenced code-block bodies so headings/links inside example
    YAML or shell snippets are never mistaken for real repo structure."""
    lines = text.split("\n")
    out = []
    in_fence = False
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


def iter_markdown_files(root: Path):
    for path in sorted(root.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def heading_slugs(text: str) -> set[str]:
    slugs = set()
    for _, title in HEADING_RE.findall(strip_code_fences(text)):
        slugs.add(slugify(title))
    return slugs


# --------------------------------------------------------------------------
# Check 1 — Decision Record template compliance
# --------------------------------------------------------------------------

DR_TITLE_RE = re.compile(r"^# (\d{4}) — (.+)$")
DR_STATUS_RE = re.compile(r"^\*\*Status:\*\*\s*(\S.*)$", re.MULTILINE)
REQUIRED_DR_HEADINGS = ["## Context", "## Decision", "## Rationale", "## Discarded alternatives"]
REDIRECT_RE = re.compile(
    r"^> \*\*Movido / Moved:\*\*.*?`(decisions/[\w.-]+\.md)`.*$",
    re.MULTILINE,
)


def check_decision_records(root: Path, errors: list[str], warnings: list[str]) -> None:
    decisions_dir = root / "decisions"
    if not decisions_dir.is_dir():
        errors.append("decisions/ directory not found")
        return

    existing = {p.name for p in decisions_dir.glob("*.md")}

    for path in sorted(decisions_dir.glob("*.md")):
        rel = path.relative_to(root)
        text = path.read_text(encoding="utf-8")
        heading_count = len(re.findall(r"^## ", text, re.MULTILINE))

        if heading_count == 0:
            # Expected to be a bilingual redirect stub.
            m = REDIRECT_RE.search(text)
            if not m:
                errors.append(
                    f"{rel}: no '## ' headings and doesn't match the redirect-stub "
                    f"template (expected a '> **Movido / Moved:** ... `decisions/<target>.md`' line)"
                )
                continue
            target = m.group(1)
            if target.split("/", 1)[-1] not in existing:
                errors.append(f"{rel}: redirect target `{target}` does not exist in decisions/")
            continue

        # Expected to be a canonical Decision Record.
        first_line = text.split("\n", 1)[0]
        title_match = DR_TITLE_RE.match(first_line)
        if not title_match:
            errors.append(
                f"{rel}: first line doesn't match the DR title template "
                f"'# NNNN — Title' (got: {first_line!r})"
            )
        else:
            fn_number = rel.name[:4]
            if title_match.group(1) != fn_number:
                errors.append(
                    f"{rel}: title number ({title_match.group(1)}) doesn't match "
                    f"filename number ({fn_number})"
                )

        if not DR_STATUS_RE.search(text):
            errors.append(f"{rel}: missing a non-empty '**Status:** ...' line")

        positions = []
        ok = True
        for heading in REQUIRED_DR_HEADINGS:
            m = re.search(rf"^{re.escape(heading)}$", text, re.MULTILINE)
            if not m:
                errors.append(f"{rel}: missing required heading '{heading}'")
                ok = False
            else:
                positions.append(m.start())
        if ok and positions != sorted(positions):
            errors.append(
                f"{rel}: required headings are present but out of order "
                f"(expected {REQUIRED_DR_HEADINGS})"
            )


# --------------------------------------------------------------------------
# Check 2 — internal markdown link resolution
# --------------------------------------------------------------------------

def check_internal_links(root: Path, errors: list[str], warnings: list[str]) -> None:
    md_files = list(iter_markdown_files(root))
    slug_cache: dict[Path, set[str]] = {}

    def slugs_for(path: Path) -> set[str]:
        if path not in slug_cache:
            try:
                slug_cache[path] = heading_slugs(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError):
                slug_cache[path] = set()
        return slug_cache[path]

    for path in md_files:
        rel = path.relative_to(root)
        text = strip_code_fences(path.read_text(encoding="utf-8"))
        for match in LINK_RE.finditer(text):
            target = match.group(1)

            if target.startswith(("http://", "https://", "mailto:", "#")) is False and "://" in target:
                continue  # some other URI scheme (rare) — not our concern
            if target.startswith(("http://", "https://", "mailto:")):
                continue

            file_part, _, anchor = target.partition("#")

            if file_part == "":
                # Same-file anchor link.
                if anchor and anchor not in slugs_for(path):
                    errors.append(
                        f"{rel}: link '{target}' anchor '#{anchor}' not found "
                        f"among this file's own headings"
                    )
                continue

            target_path = (path.parent / file_part).resolve()
            try:
                target_path.relative_to(root.resolve())
            except ValueError:
                warnings.append(f"{rel}: link '{target}' resolves outside the repository, skipped")
                continue

            if not target_path.exists():
                errors.append(f"{rel}: link '{target}' -> target does not exist")
                continue

            if anchor and target_path.suffix == ".md":
                if anchor not in slugs_for(target_path):
                    errors.append(
                        f"{rel}: link '{target}' anchor '#{anchor}' not found "
                        f"among headings of {target_path.relative_to(root)}"
                    )


# --------------------------------------------------------------------------
# Check 3 — README <-> CHANGELOG version consistency
# --------------------------------------------------------------------------

README_VERSION_RE = re.compile(r"Current version:\s*\*\*([0-9]+\.[0-9]+\.[0-9]+)\*\*")
CHANGELOG_VERSION_RE = re.compile(r"^## \[([0-9]+\.[0-9]+\.[0-9]+)\]", re.MULTILINE)


def check_version_consistency(root: Path, errors: list[str], warnings: list[str]) -> None:
    readme_path = root / "README.md"
    changelog_path = root / "CHANGELOG.md"
    if not readme_path.exists() or not changelog_path.exists():
        errors.append("README.md and/or CHANGELOG.md not found")
        return

    readme_text = readme_path.read_text(encoding="utf-8")
    changelog_text = changelog_path.read_text(encoding="utf-8")

    readme_match = README_VERSION_RE.search(readme_text)
    if not readme_match:
        errors.append("README.md: no 'Current version: **X.Y.Z**' line found")
        return
    readme_version = readme_match.group(1)

    changelog_match = CHANGELOG_VERSION_RE.search(changelog_text)
    if not changelog_match:
        errors.append("CHANGELOG.md: no '## [X.Y.Z]' released-version heading found")
        return
    changelog_version = changelog_match.group(1)

    if readme_version != changelog_version:
        errors.append(
            f"version mismatch: README.md declares {readme_version}, but "
            f"CHANGELOG.md's latest released section is [{changelog_version}]"
        )


# --------------------------------------------------------------------------
# Check 4 — schema field -> Decision Record coverage (report only)
# --------------------------------------------------------------------------

def check_schema_field_coverage(root: Path, notes: list[str]) -> None:
    spec_path = root / "SPEC.md"
    if not spec_path.exists():
        notes.append("SPEC.md not found, coverage report skipped")
        return

    spec_text = spec_path.read_text(encoding="utf-8")
    m = re.search(r"^## 2\. Frontmatter.*?```yaml\n(.*?)\n```", spec_text, re.MULTILINE | re.DOTALL)
    if not m:
        notes.append("could not locate the section 2 frontmatter YAML block in SPEC.md")
        return

    block = m.group(1)
    fields = []
    for line in block.split("\n"):
        line = line.strip()
        if not line or line in ("---",) or line.startswith("#"):
            continue
        field_match = re.match(r"([A-Za-z_]+):", line)
        if field_match:
            fields.append(field_match.group(1))

    decisions_dir = root / "decisions"
    canonical_texts = []
    for path in sorted(decisions_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if re.search(r"^## Context$", text, re.MULTILINE):
            canonical_texts.append(text)
    corpus = "\n".join(canonical_texts)

    uncited = []
    for field in fields:
        if not re.search(rf"[`_]?\b{re.escape(field)}\b", corpus):
            uncited.append(field)

    notes.append(
        f"schema field coverage: {len(fields) - len(uncited)}/{len(fields)} fields "
        f"from SPEC.md section 2 have at least one mention in a canonical Decision Record"
    )
    if uncited:
        notes.append(
            "fields with no direct DR citation found (informational only — a field can be "
            "legitimately covered by prose in SPEC.md itself without a dedicated DR): "
            + ", ".join(uncited)
        )


# --------------------------------------------------------------------------
# Runner
# --------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository root (default: current directory)")
    parser.add_argument("--quiet", action="store_true", help="only print output when there are errors")
    args = parser.parse_args()

    root = Path(args.root).resolve()

    errors: list[str] = []
    warnings: list[str] = []
    notes: list[str] = []

    check_decision_records(root, errors, warnings)
    check_internal_links(root, errors, warnings)
    check_version_consistency(root, errors, warnings)
    check_schema_field_coverage(root, notes)

    if not args.quiet or errors or warnings:
        if errors:
            print(f"ERRORS ({len(errors)}):")
            for e in errors:
                print(f"  [FAIL] {e}")
            print()
        if warnings:
            print(f"WARNINGS ({len(warnings)}):")
            for w in warnings:
                print(f"  [WARN] {w}")
            print()
        if notes:
            print("COVERAGE (informational, never fails the build):")
            for n in notes:
                print(f"  [INFO] {n}")
            print()

    if errors:
        print(f"validate_hipocampo: FAILED — {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"validate_hipocampo: OK — 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
