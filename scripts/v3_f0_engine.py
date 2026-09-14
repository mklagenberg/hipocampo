#!/usr/bin/env python3
"""Deterministic helpers for the unreleased V3 F0 candidate."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_CLASSES = {"deterministic", "cognitive", "human", "hybrid"}
OPERATIONAL_PATTERNS = ("v3_*.py", "normalize_frontmatter_queue.py", "scan_v3_queues.py")


def load_yaml(relative: str) -> dict[str, Any]:
    return yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))


def operational_scripts() -> set[str]:
    paths: set[Path] = set()
    scripts = ROOT / "scripts"
    for pattern in OPERATIONAL_PATTERNS:
        paths.update(scripts.glob(pattern))
    return {path.relative_to(ROOT).as_posix() for path in paths}


def outcome(required: list[str], observed: list[str], blocking: list[str], *, authorization_missing: bool = False) -> str:
    missing = set(required) - set(observed)
    if not missing:
        return "completed"
    if authorization_missing:
        return "authorization_required"
    if set(blocking) & missing:
        return "blocked"
    return "partial"
