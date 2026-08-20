#!/usr/bin/env python3
"""Validate cross-surface contracts that structural link checks cannot see.

This validator protects the v2.1.0 consistency contracts: the canonical
manifest fields, six invariants, registered-anchor discovery, and the Codex
adapter. It intentionally checks a small set of durable agreements rather
than attempting to infer methodology semantics from arbitrary prose.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED = {
    "SPEC.md": [
        "Version: 2.1.0",
        "instance.policy_profile",
        "instance.curation_level",
        "discovery.registered_repositories",
        "4. Default convention from the scaffold profile",
    ],
    "skill/references/invariants.md": [
        "Six rules",
        "## 6. Content declared in the repository",
    ],
    "skill/references/personalization.md": [
        "anchor_repository",
        "discovery.registered_repositories",
    ],
    "skill/references/codex.md": [
        "hipocampo.local.yaml",
        "Never self-update",
    ],
    "skill/manifest.yaml": [
        'version: "1.1.0"',
        'compatibility: "^2.1.0"',
        'target: "codex"',
    ],
    "scaffold/skeleton/hipocampo.yaml": [
        "policy_profile:",
        "curation_level:",
        "registered_repositories:",
    ],
    "scaffold/skeleton/AGENTS.md": [
        "6. Content declared in this repository",
        "instance.policy_profile",
    ],
    "AGENTS.md": [
        "relationship is `conforms_to`",
    ],
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors: list[str] = []

    for relative, snippets in REQUIRED.items():
        path = root / relative
        if not path.exists():
            errors.append(f"{relative}: missing")
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in text:
                errors.append(f"{relative}: missing required contract text {snippet!r}")

    for profile in ("scaffold/profiles/pessoal.yaml", "scaffold/profiles/empresa.yaml"):
        text = (root / profile).read_text(encoding="utf-8")
        if 'id: "curation_level"' not in text:
            errors.append(f"{profile}: must declare the curation_level input")
        if 'id: "tier"' in text:
            errors.append(f"{profile}: must not emit the ambiguous tier input")

    upgrade = (root / "UPGRADE.md").read_text(encoding="utf-8")
    if "router (`skill/references/personalization.md`" in upgrade:
        errors.append("UPGRADE.md: retired router guidance remains active")

    if errors:
        print(f"validate_contracts: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_contracts: OK — 0 errors")
    return 0


if __name__ == "__main__":
    sys.exit(main())
