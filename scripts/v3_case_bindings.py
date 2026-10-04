#!/usr/bin/env python3
"""Shared deterministic case-to-assertion and case-to-command binding checks."""
from __future__ import annotations


ASSERTION_PREFIXES = {
    "crud": "crud",
    "artifact-provenance": "artifact",
    "ingress": "ingress",
    "rem-curation": "rem",
    "package": "package",
    "delivery-transfer": "delivery",
    "governance": "governance",
    "operational-audit": "audit",
    "migration-compatibility": "migration",
    "maintenance": "maintenance",
    "learning-evolution": "learning",
    "search-progressive-disclosure": "search",
}

ASSERTION_SUFFIX_OVERRIDES = {
    ("artifact-provenance", "record-content-independent-of-artifact"): "record_content_independent",
}


def expected_assertion_id(engine_id: str, case_id: str) -> str | None:
    prefix = ASSERTION_PREFIXES.get(engine_id)
    if prefix is None:
        return None
    suffix = ASSERTION_SUFFIX_OVERRIDES.get(
        (engine_id, case_id), case_id.casefold().replace("-", "_")
    )
    return f"{prefix}.{suffix}"


def validate_binding_set(engines: list[dict], bindings: list[dict]) -> list[str]:
    errors: list[str] = []
    engine_map = {engine.get("id"): engine for engine in engines if isinstance(engine, dict)}
    binding_map: dict[tuple[str, str], dict] = {}
    assertion_ids: set[str] = set()
    for index, binding in enumerate(bindings):
        if not isinstance(binding, dict):
            errors.append(f"binding[{index}] must be a mapping")
            continue
        key = (str(binding.get("engine")), str(binding.get("id")))
        if key in binding_map:
            errors.append(f"duplicate deterministic binding: {key[0]}/{key[1]}")
        binding_map[key] = binding
        engine = engine_map.get(binding.get("engine"))
        if engine is None:
            errors.append(f"{key[0]}/{key[1]}: unknown engine")
            continue
        commands = engine.get("deterministic_commands", [])
        command_index = binding.get("command_index")
        if not isinstance(command_index, int) or not 0 <= command_index < len(commands):
            errors.append(f"{key[0]}/{key[1]}: invalid command_index")
        else:
            expected_command = commands[command_index]
            if binding.get("command") != expected_command:
                errors.append(f"{key[0]}/{key[1]}: command does not match command_index {command_index}")
        expected_id = expected_assertion_id(*key)
        if expected_id is None or binding.get("assertion_id") != expected_id:
            errors.append(f"{key[0]}/{key[1]}: assertion_id does not match its canonical case id")
        assertion_id = binding.get("assertion_id")
        if isinstance(assertion_id, str) and assertion_id:
            if assertion_id in assertion_ids:
                errors.append(f"duplicate assertion_id: {assertion_id}")
            assertion_ids.add(assertion_id)
        if not isinstance(binding.get("assertion"), str) or not binding["assertion"].strip():
            errors.append(f"{key[0]}/{key[1]}: observable assertion text is required")

    expected_keys = {
        (engine.get("id"), str(case_id))
        for engine in engines if isinstance(engine, dict)
        for case_id in engine.get("deterministic_cases", [])
    }
    if set(binding_map) != expected_keys:
        errors.append(
            "deterministic binding coverage mismatch: "
            f"missing={sorted(expected_keys - set(binding_map))}, "
            f"extra={sorted(set(binding_map) - expected_keys)}"
        )
    return errors
