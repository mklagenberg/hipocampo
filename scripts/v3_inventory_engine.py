#!/usr/bin/env python3
"""Deterministic readiness evaluation for synthetic V3 vault inventories."""
from __future__ import annotations

from typing import Any


def evaluate(profile: dict[str, Any]) -> str:
    if profile.get("access") != "available":
        return "blocked"
    if profile.get("mapping") in {"missing", "ambiguous", "unknown"}:
        return "blocked"
    if profile.get("privacy") != "proven":
        return "blocked"
    if profile.get("rollback") != "tested":
        return "blocked"
    if profile.get("target_contract") != "verified":
        return "blocked"
    if profile.get("unsafe_raw_fallback"):
        return "blocked"
    if profile.get("human_approval") != "present":
        return "authorization_required"
    if profile.get("artifact_frontier") == "partial":
        return "partial"
    return "ready"
