#!/usr/bin/env python3
"""Shared source/channel policy. Candidate warnings never become exceptions."""
from __future__ import annotations

import re


class ChannelError(ValueError):
    pass


def parse_version(value: str) -> tuple[tuple[int, int, int], tuple[str, ...]] | None:
    if not isinstance(value, str):
        return None
    match = re.fullmatch(
        r"v?(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
        r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
        r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?", value.strip())
    if not match:
        return None
    prerelease = tuple(match[4].split(".")) if match[4] else ()
    if any(part.isdigit() and len(part) > 1 and part[0] == "0" for part in prerelease):
        return None
    return tuple(int(match[i]) for i in (1, 2, 3)), prerelease


def matches(candidate: str, requirement: str, *, experimental: bool = False) -> bool:
    parsed = parse_version(candidate)
    minimum = parse_version(requirement[1:]) if isinstance(requirement, str) and requirement.startswith("^") else None
    if parsed is None or minimum is None or minimum[1]:
        return False
    current, prerelease = parsed
    lower = minimum[0]
    if prerelease and not experimental:
        return False
    if lower[0]:
        return current >= lower and current[0] == lower[0]
    if lower[1]:
        return current >= lower and current[:2] == lower[:2]
    return current == lower


def resolve_channel(channel: str, methodology: str, compatibility: str,
                    *, source_commit: str, release: dict | None = None) -> list[dict]:
    if channel not in {"stable", "experimental"}:
        raise ChannelError("channel must be stable or explicitly experimental")
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit or ""):
        raise ChannelError("an exact source commit is required")
    if not matches(methodology, compatibility, experimental=channel == "experimental"):
        raise ChannelError("methodology contract is invalid or incompatible")
    if channel == "experimental":
        return [{"severity": "WARNING", "code": "EXPERIMENTAL_SNAPSHOT",
                 "message": "Candidate execution enabled; final publication/review is not required for valid operations."}]
    release = release or {}
    parsed = parse_version(methodology)
    if parsed is None or parsed[1]:
        raise ChannelError("stable selection excludes prereleases")
    if (release.get("immutable") is not True or release.get("draft") is not False
            or release.get("prerelease") is not False
            or release.get("tag_name") != "v" + methodology
            or release.get("resolved_commit") != source_commit):
        raise ChannelError("stable requires the verified immutable release and exact tag-resolved source")
    return []
