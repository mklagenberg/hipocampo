#!/usr/bin/env python3
"""Deterministic preflight evaluation for synthetic V2.x to V3 migration cases."""
from __future__ import annotations

from typing import Any
import re


BLOCKING = {
    "mapping": {"missing", "ambiguous"},
    "privacy": {"unknown", "unproven"},
    "rollback": {"missing"},
    "target_contract": {"missing", "unknown"},
}
VERSION_RE = re.compile(r"^\d+\.\d+(?:\.\d+)?$")


def evaluate(case: dict[str, Any]) -> str:
    if case.get("unsafe_raw_fallback"):
        return "blocked"
    source_version = case.get("source_version")
    target_version = case.get("target_version")
    if not isinstance(source_version, str) or not VERSION_RE.fullmatch(source_version):
        return "blocked"
    if not isinstance(target_version, str) or not VERSION_RE.fullmatch(target_version):
        return "blocked"
    if source_version == target_version:
        return "blocked"
    if any(case.get(field) in values for field, values in BLOCKING.items()):
        return "blocked"
    if case.get("human_approval") != "present":
        return "authorization_required"
    if case.get("semantic_review") == "partial":
        return "partial"
    return "ready"
