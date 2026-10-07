#!/usr/bin/env python3
"""Validate cross-surface contracts that structural link checks cannot see.

This validator protects the declared methodology consistency contracts: the canonical
manifest fields, six invariants, registered-anchor discovery, privacy routing,
and the Codex adapter. It intentionally checks a small set of durable agreements rather
than attempting to infer methodology semantics from arbitrary prose.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED = {
    "SPEC.md": [
        "instance.policy_profile",
        "instance.curation_level",
        "discovery.registered_repositories",
        "4. Default convention from the scaffold profile",
    ],
    "skill/references/invariants.md": [
        "## 6. Repository state outranks cached skill state",
        "canonical CRUD",
    ],
    "skill/references/personalization.md": [
        "anchor_repository",
        "discovery.registered_repositories",
    ],
    "skill/references/codex.md": [
        "hipocampo.local.yaml",
        "Never self-update",
        "package-lock.yaml",
    ],
    "skill/manifest.yaml": [
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
        "## Route by user intent",
        "skill/package-lock.yaml",
    ],
    "CONTRIBUTING.md": [
        "## Terms and names",
        "## Privacy and learned safeguards",
    ],
    "docs/privacy-and-licensing-boundaries.md": [
        "Progressive remediation",
        "Apache-2.0",
    ],
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors: list[str] = []
    import yaml
    from validate_compatibility import satisfies
    contract = yaml.safe_load((root / "COMPATIBILITY.yaml").read_text(encoding="utf-8"))
    manifest = yaml.safe_load((root / "skill/manifest.yaml").read_text(encoding="utf-8"))
    if not any(item.get("target") == "codex" for item in manifest.get("adapters", []) if isinstance(item, dict)):
        errors.append("manifest must declare the codex adapter")
    if manifest.get("skill", {}).get("package_lock") != "skill/package-lock.yaml":
        errors.append("manifest must identify the canonical package lock")
    methodology_version = contract["methodology"]["version"]
    if "Version: " + methodology_version not in (root / "SPEC.md").read_text(encoding="utf-8"):
        errors.append("SPEC version differs from the compatibility tuple")
    if contract["skill"]["required_version"] != manifest["skill"]["version"]:
        errors.append("canonical skill version differs from the compatibility tuple")
    if not satisfies(methodology_version, manifest["methodology"]["compatibility"]):
        errors.append("canonical skill does not support the declared methodology")
    for profile_path in ["scaffold/profiles/pessoal.yaml", "scaffold/profiles/empresa.yaml"]:
        profile = yaml.safe_load((root / profile_path).read_text(encoding="utf-8"))
        if not satisfies(methodology_version, profile["methodology"]["compatibility"]):
            errors.append(profile_path + ": scaffold does not support the target methodology")
    skeleton = yaml.safe_load((root / "scaffold/skeleton/hipocampo.yaml").read_text(encoding="utf-8"))
    if not satisfies(methodology_version, skeleton["hipocampo"]["compatibility"]):
        errors.append("scaffold skeleton does not support the target methodology")

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
    if "repository-wide inspection" not in upgrade:
        errors.append("UPGRADE.md: must state progressive, non-sweep privacy adoption")

    if errors:
        print(f"validate_contracts: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_contracts: OK — 0 errors")
    return 0


if __name__ == "__main__":
    sys.exit(main())
