#!/usr/bin/env python3
"""Compute a version-age notice from caller-verified source and stable versions."""
from __future__ import annotations

from v3_channel import parse_version


class VersionNoticeError(ValueError):
    """Source or published-stable evidence is insufficient for a notice."""


def version_notice(source_version: str, published_stable: str, *,
                   stable_verified: bool, source_verified: bool) -> dict | None:
    """Return an age WARNING, never a compatibility or access decision.

    The caller must verify both identities against the source contract and
    immutable published release. These booleans are assertions, not proof.
    """
    source = parse_version(source_version)
    stable = parse_version(published_stable)
    if source is None or not source_verified:
        raise VersionNoticeError("source_version_unverified")
    if stable is None or stable[1] or not stable_verified:
        raise VersionNoticeError("published_stable_unverified")
    source_core, source_pre = source
    stable_core, _ = stable
    older = source_core < stable_core or (source_core == stable_core and bool(source_pre))
    if not older:
        return None
    route = "governed V2-to-V3 migration before V3 writes" if source_core[0] < 3 else "the applicable V3 upgrade checklist"
    return {
        "severity": "WARNING",
        "code": "VAULT_SOURCE_VERSION_OLDER",
        "source_version": source_version,
        "published_stable": published_stable,
        "message": (f"Vault source contract {source_version} predates published stable "
                    f"{published_stable}; assess {route}. Age alone does not prove a vulnerability."),
    }
