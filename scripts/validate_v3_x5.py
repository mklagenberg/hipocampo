#!/usr/bin/env python3
"""Integrated deterministic checks for the unreleased V3 X5 candidate."""
from __future__ import annotations

from pathlib import Path

from v3_vocabulary import resolve_alias


ROOT = Path(__file__).resolve().parents[1]


def require(path: str, needles: list[str], errors: list[str]) -> None:
    target = ROOT / path
    if not target.exists():
        errors.append(f"missing {path}")
        return
    text = target.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            errors.append(f"{path} is missing {needle!r}")


def main() -> int:
    errors: list[str] = []
    for utterance, canonical in [("create a note", "Record"), ("use the fonte", "Source")]:
        result = resolve_alias(utterance)
        if result["canonical"] != canonical or result["status"] != "resolved":
            errors.append(f"alias routing failed for {utterance!r}")
    ambiguous = resolve_alias("save this in the vault")
    if ambiguous["status"] != "clarification_required":
        errors.append("ambiguous routing did not fail into didactic clarification")

    require("docs/v3-vocabulary-and-aliases.md", ["Canonical terms", "didactic clarification"], errors)
    require("docs/v3-documentation-architecture.md", ["SPEC.md", "README", "additive or more restrictive"], errors)
    require("docs/v3-license-and-vault-privacy-contract.md", ["legal license", "vault contract", "content_license"], errors)
    require("docs/v3-language-policy.md", ["always written in English", "English is the default", "ES-419"], errors)
    require("docs/v3-surface-authority-contract.md", ["normative sources", "fail-closed", "Recency alone"], errors)
    require("docs/v3-external-reference-policy.md", ["comparison", "adopted format", "new Decision Record"], errors)
    require("docs/v3-x5-fixtures.yaml", ["local-extension-additive", "offline-missing-spec", "external-reference"], errors)

    if errors:
        print(f"validate_v3_x5: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_v3_x5: OK — vocabulary, documentation, privacy, language, authority and references")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
