#!/usr/bin/env python3
"""Synthetic positive and negative age-notice cases for V2 and V3 vaults."""
from __future__ import annotations

from vault_version_notice import VersionNoticeError, version_notice


def main() -> int:
    cases = 0
    for source in ("2.0.0", "2.1.0", "2.1.1", "2.2.0"):
        warning = version_notice(source, "3.0.1", stable_verified=True, source_verified=True)
        assert warning and warning["code"] == "VAULT_SOURCE_VERSION_OLDER"
        assert "migration" in warning["message"] and "3.0.1" in warning["message"]
        cases += 1
    older_v3 = version_notice("3.0.0", "3.0.1", stable_verified=True, source_verified=True)
    assert older_v3 and "V3 upgrade" in older_v3["message"]
    cases += 1
    for source in ("3.0.1", "3.1.0", "3.1.0-rc.1"):
        assert version_notice(source, "3.0.1", stable_verified=True, source_verified=True) is None
        cases += 1
    candidate = version_notice("3.1.0-rc.1", "3.1.0", stable_verified=True, source_verified=True)
    assert candidate and candidate["published_stable"] == "3.1.0"
    cases += 1
    for source, stable, verified_source, verified_stable, code in (
        ("3.0.0", "3.0.1", False, True, "source_version_unverified"),
        ("unknown", "3.0.1", True, True, "source_version_unverified"),
        ("3.0.0", "3.0.1", True, False, "published_stable_unverified"),
        ("3.0.0", "3.1.0-rc.1", True, True, "published_stable_unverified"),
    ):
        try:
            version_notice(source, stable, stable_verified=verified_stable,
                           source_verified=verified_source)
        except VersionNoticeError as exc:
            assert str(exc) == code
        else:
            raise AssertionError(code)
        cases += 1
    print(f"validate_vault_version_notice: OK — {cases} synthetic cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
