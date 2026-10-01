"""Validate contract-drift routing and the V3 migration crosswalk."""
from copy import deepcopy
from pathlib import Path
import sys

import yaml


DRIFT_ACTIONS = {
    "content-change": "continue",
    "instruction-change": "reread",
    "contract-change": "blocked",
    "methodology-version-change": "compatibility-route",
    "unavailable": "blocked",
}
FIXTURE_COLLECTIONS = {
    "docs/contract-drift-fixtures.yaml": ("fixtures", "scripts/validate_contract_drift.py"),
    "docs/v3-synthetic-vault-inventories.yaml": ("profiles", "scripts/validate_v3_inventory.py"),
}


def validate_registry(root: Path, registry: dict, fixture_documents: dict) -> list[str]:
    errors: list[str] = []
    entries = registry.get("classes") if isinstance(registry, dict) else None
    if not isinstance(entries, list):
        return ["registry classes must be a list"]

    found_classes: set[str] = set()
    entry_ids: set[str] = set()
    for index, entry in enumerate(entries):
        prefix = f"registry classes[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be a mapping")
            continue

        class_id = entry.get("id")
        if not isinstance(class_id, str) or class_id not in DRIFT_ACTIONS:
            errors.append(f"{prefix} has unsupported or missing classification {class_id!r}")
        else:
            found_classes.add(class_id)
            if class_id in entry_ids:
                errors.append(f"duplicate classification entry {class_id!r}")
            entry_ids.add(class_id)
            if entry.get("action") != DRIFT_ACTIONS[class_id]:
                errors.append(f"{prefix} action does not match classification {class_id!r}")

        for field in ("surfaces", "authorities"):
            refs = entry.get(field)
            if not isinstance(refs, list) or not refs:
                errors.append(f"{prefix} requires at least one {field} reference")
                continue
            for ref in refs:
                if not isinstance(ref, str) or not (root / ref).is_file():
                    errors.append(f"{prefix} references missing {field} file {ref!r}")

        fixtures = entry.get("fixtures")
        if not isinstance(fixtures, list) or not fixtures:
            errors.append(f"{prefix} requires at least one fixture reference")
            continue
        for fixture_ref in fixtures:
            if not isinstance(fixture_ref, dict):
                errors.append(f"{prefix} fixture reference must be a mapping")
                continue
            fixture_path = fixture_ref.get("path")
            fixture_id = fixture_ref.get("id")
            expected = fixture_ref.get("expected")
            validator = fixture_ref.get("validator")
            fixture_contract = FIXTURE_COLLECTIONS.get(fixture_path)
            if fixture_contract is None:
                errors.append(f"{prefix} uses unsupported fixture document {fixture_path!r}")
                continue
            collection, expected_validator = fixture_contract
            document = fixture_documents.get(fixture_path)
            if not (root / fixture_path).is_file() or not isinstance(document, dict):
                errors.append(f"{prefix} references missing or invalid fixture document {fixture_path!r}")
                continue
            records = document.get(collection)
            if not isinstance(records, list):
                errors.append(f"{prefix} fixture document {fixture_path!r} lacks {collection}")
                continue
            matches = [record for record in records if isinstance(record, dict) and record.get("id") == fixture_id]
            if len(matches) != 1:
                errors.append(f"{prefix} fixture {fixture_id!r} must resolve exactly once in {fixture_path!r}")
            elif matches[0].get("action", matches[0].get("expected")) != expected:
                errors.append(f"{prefix} fixture {fixture_id!r} expected outcome does not match")
            if not isinstance(validator, str) or not (root / validator).is_file():
                errors.append(f"{prefix} references missing validator {validator!r}")
            elif validator != expected_validator:
                errors.append(f"{prefix} fixture document {fixture_path!r} requires validator {expected_validator!r}")

            if fixture_path == "docs/contract-drift-fixtures.yaml":
                if class_id is not None and fixture_id != class_id:
                    errors.append(f"{prefix} fixture classification {fixture_id!r} does not match {class_id!r}")
                if class_id in DRIFT_ACTIONS and expected != DRIFT_ACTIONS[class_id]:
                    errors.append(f"{prefix} fixture outcome does not match classification {class_id!r}")
            elif fixture_path == "docs/v3-synthetic-vault-inventories.yaml":
                if class_id != "unavailable" or fixture_id != "synthetic-invited-vault-inaccessible":
                    errors.append(f"{prefix} inventory fixture is not scoped to unavailable drift")
                elif len(matches) == 1 and matches[0].get("access") != "unavailable":
                    errors.append(f"{prefix} inventory fixture does not represent an unavailable target")

    missing = set(DRIFT_ACTIONS) - found_classes
    if missing:
        errors.append(f"registry is missing classifications: {', '.join(sorted(missing))}")
    return errors


def negative_checks(root: Path, registry: dict, fixture_documents: dict) -> int:
    cases = []

    invalid_class = deepcopy(registry)
    invalid_class["classes"][0]["id"] = "unclassified-surface"
    cases.append((invalid_class, "unsupported or missing classification"))

    missing_fixture = deepcopy(registry)
    missing_fixture["classes"][0]["fixtures"][0]["id"] = "fixture-does-not-exist"
    cases.append((missing_fixture, "must resolve exactly once"))

    missing_surface = deepcopy(registry)
    missing_surface["classes"][0]["surfaces"][0] = "docs/missing-surface.md"
    cases.append((missing_surface, "references missing surfaces file"))

    missing_authority = deepcopy(registry)
    missing_authority["classes"][0]["authorities"][0] = "decisions/missing-contract.md"
    cases.append((missing_authority, "references missing authorities file"))

    wrong_action = deepcopy(registry)
    wrong_action["classes"][0]["action"] = "blocked"
    cases.append((wrong_action, "action does not match classification"))

    for candidate, expected_error in cases:
        if not any(expected_error in error for error in validate_registry(root, candidate, fixture_documents)):
            raise AssertionError(f"negative validation case did not reject: {expected_error}")
    return len(cases)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    procedure = (root / "docs" / "contract-drift-procedure.md").read_text(encoding="utf-8").lower()
    drift_fixtures_path = "docs/contract-drift-fixtures.yaml"
    inventory_fixtures_path = "docs/v3-synthetic-vault-inventories.yaml"
    registry_path = "docs/v3-contract-drift-registry.yaml"
    drift_fixtures = yaml.safe_load((root / drift_fixtures_path).read_text(encoding="utf-8"))
    inventory_fixtures = yaml.safe_load((root / inventory_fixtures_path).read_text(encoding="utf-8"))
    registry = yaml.safe_load((root / registry_path).read_text(encoding="utf-8"))
    fixture_documents = {
        drift_fixtures_path: drift_fixtures,
        inventory_fixtures_path: inventory_fixtures,
    }

    for term in ("content change", "instruction change", "contract change", "methodology-version change", "unavailable", "blocked"):
        if term not in procedure:
            raise AssertionError(f"contract-drift procedure is missing {term!r}")

    fixture_ids = {item.get("id") for item in drift_fixtures.get("fixtures", []) if isinstance(item, dict)}
    if fixture_ids != set(DRIFT_ACTIONS):
        raise AssertionError("the five generic contract-drift fixtures changed unexpectedly")

    errors = validate_registry(root, registry, fixture_documents)
    if errors:
        raise AssertionError("; ".join(errors))
    negative_count = negative_checks(root, registry, fixture_documents)
    fixture_count = sum(len(item["fixtures"]) for item in registry["classes"])
    print(
        "validate_contract_drift: OK — five drift classes, "
        f"five V3 mapping entries, {fixture_count} fixture links, {negative_count} negative cases"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
