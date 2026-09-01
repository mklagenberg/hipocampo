#!/usr/bin/env python3
"""Validate Hipocampo's canonical skill/methodology/vault compatibility contract."""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

import yaml


def version(value: str) -> tuple[int, int, int] | None:
    try:
        parts = value.strip().lstrip("v").split(".")
        if len(parts) != 3:
            return None
        return tuple(int(part) for part in parts)  # type: ignore[return-value]
    except (AttributeError, ValueError):
        return None


def satisfies(candidate: str, requirement: str) -> bool:
    parsed = version(candidate)
    if parsed is None or not isinstance(requirement, str) or not requirement.startswith("^"):
        return False
    minimum = version(requirement[1:])
    if minimum is None:
        return False
    if minimum[0] > 0:
        return parsed >= minimum and parsed[0] == minimum[0]
    return parsed >= minimum and parsed[:2] == minimum[:2]


def state(case: dict) -> str:
    if not case.get("sources_available", False):
        return "access_unavailable"
    if not case.get("package_integrity", False):
        return "unsupported_or_unknown"
    methodology = case.get("methodology_version", "")
    skill_range = case.get("skill_methodology_range", "")
    vault_range = case.get("vault_range", "")
    if not methodology or not satisfies(methodology, skill_range):
        return "unsupported_or_unknown"
    if not satisfies(methodology, vault_range):
        return "migration_required"
    return "compatible"


def package_is_intact(root: Path) -> bool:
    lock = yaml.safe_load((root / "skill" / "package-lock.yaml").read_text(encoding="utf-8"))
    expected = {item["path"]: item["sha256"] for item in lock["package"]["files"]}
    actual_paths = {
        path.relative_to(root / "skill").as_posix(): path
        for path in (root / "skill").rglob("*")
        if path.is_file() and path.name != "package-lock.yaml"
    }
    if set(expected) != set(actual_paths):
        return False
    return all(
        hashlib.sha256(actual_paths[relative].read_bytes()).hexdigest() == digest
        for relative, digest in expected.items()
    )


def vault_manifest_is_valid(path: Path, contract: dict) -> tuple[bool, dict]:
    fixture = yaml.safe_load(path.read_text(encoding="utf-8"))
    for field in contract["vault"]["required_fields"]:
        value = fixture
        for part in field.split("."):
            value = value.get(part) if isinstance(value, dict) else None
        if not value or (isinstance(value, str) and value.startswith("<fill in")):
            return False, fixture
    return True, fixture


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument(
        "--vault-manifest",
        help="path to a real hipocampo.yaml; defaults to the checked-in reference fixture",
    )
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors: list[str] = []

    contract_path = root / "COMPATIBILITY.yaml"
    fixtures_path = root / "docs" / "compatibility-fixtures.yaml"
    try:
        contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
        fixtures = yaml.safe_load(fixtures_path.read_text(encoding="utf-8"))["fixtures"]
        skill = yaml.safe_load((root / "skill" / "manifest.yaml").read_text(encoding="utf-8"))
    except (OSError, KeyError, yaml.YAMLError) as exc:
        print(f"validate_compatibility: FAILED — cannot load contract: {exc}")
        return 1

    if contract.get("schema_version") != "1.0":
        errors.append("COMPATIBILITY.yaml: unsupported schema_version")
    expected_methodology = contract["methodology"]["version"]
    if skill["skill"]["version"] != contract["skill"]["required_version"]:
        errors.append("skill/manifest.yaml: skill version does not match the required compatibility version")
    if skill["methodology"]["compatibility"] != contract["methodology"]["supported_vault_range"]:
        errors.append("skill/manifest.yaml: methodology.compatibility diverges from COMPATIBILITY.yaml")
    if not satisfies(expected_methodology, skill["methodology"]["compatibility"]):
        errors.append("skill/manifest.yaml: compatibility does not cover the canonical methodology version")
    if not (root / "skill" / "package-lock.yaml").is_file():
        errors.append("skill/package-lock.yaml: required package lock is missing")
    elif not package_is_intact(root):
        errors.append("skill/package-lock.yaml: package files do not match their recorded SHA-256 hashes")
    if contract["methodology"]["taxonomy_revision"] not in (root / "docs" / "taxonomy.md").read_text(encoding="utf-8"):
        errors.append("docs/taxonomy.md: compatibility revision is not recorded")
    if contract["methodology"]["vocabulary_revision"] not in (root / "docs" / "vocabulary-dictionary.md").read_text(encoding="utf-8"):
        errors.append("docs/vocabulary-dictionary.md: compatibility revision is not recorded")
    vault_path = Path(args.vault_manifest) if args.vault_manifest else root / "docs" / "compatibility-vault-fixture.yaml"
    try:
        vault_valid, vault = vault_manifest_is_valid(vault_path, contract)
    except (OSError, yaml.YAMLError, TypeError):
        errors.append(f"{vault_path}: vault manifest is unavailable or malformed")
        vault_valid, vault = False, {}
    if not vault_valid:
        errors.append(f"{vault_path}: required vault fields are incomplete")
    elif not satisfies(expected_methodology, vault["hipocampo"]["compatibility"]):
        errors.append(f"{vault_path}: compatibility declaration does not cover the canonical methodology version")

    expected_states = {item["id"] for item in contract["states"]}
    if expected_states != {
        "compatible", "compatible_with_upgrade", "migration_required",
        "unsupported_or_unknown", "access_unavailable",
    }:
        errors.append("COMPATIBILITY.yaml: state vocabulary is incomplete")
    for relative, required in {
        "docs/taxonomy.md": ["Compatibility decision state", "compatible_with_upgrade", "migration_required"],
        "docs/vocabulary-dictionary.md": ["Compatibility decision states", "compatible_with_upgrade", "access_unavailable"],
    }.items():
        text = (root / relative).read_text(encoding="utf-8")
        for snippet in required:
            if snippet not in text:
                errors.append(f"{relative}: missing compatibility vocabulary {snippet!r}")
    for fixture in fixtures:
        actual = state(fixture)
        if actual != fixture.get("expected"):
            errors.append(f"fixture {fixture.get('id')}: expected {fixture.get('expected')}, got {actual}")

    if errors:
        print(f"validate_compatibility: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print(f"validate_compatibility: OK — {len(fixtures)} fixtures, 0 errors")
    return 0


if __name__ == "__main__":
    sys.exit(main())
