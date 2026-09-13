#!/usr/bin/env python3
"""Deterministic preflight evaluation for synthetic V2.x to V3 migration cases."""
from __future__ import annotations

from typing import Any


BLOCKING = {
    "mapping": {"missing", "ambiguous"},
    "privacy": {"unknown", "unproven"},
    "rollback": {"missing"},
    "target_contract": {"missing", "unknown"},
}


def evaluate(case: dict[str, Any]) -> str:
    if case.get("unsafe_raw_fallback"):
        return "blocked"
    if any(case.get(field) in values for field, values in BLOCKING.items()):
        return "blocked"
    if case.get("human_approval") != "present":
        return "authorization_required"
    if case.get("semantic_review") == "partial":
        return "partial"
    return "ready"
