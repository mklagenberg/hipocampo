#!/usr/bin/env python3
"""Synthetic cases for the bundled-skill versus external-reference boundary."""
from __future__ import annotations

from validate_skill_version_delta import validate_delta


def main() -> int:
    cases = [
        (["SPEC.md", "docs/legacy-read-support.md"], "2.1.0", "2.1.0", True),
        (["skill/package-lock.yaml"], "2.1.0", "2.1.0", True),
        (["skill/SKILL.md"], "2.1.0", "2.1.0", False),
        (["skill/references/legacy-read.md"], "2.1.0", "2.1.0", False),
        (["skill/SKILL.md"], "2.1.0", "2.1.1", True),
        (["skill/references/legacy-read.md"], "2.1.0", "2.2.0", True),
        (["skill/SKILL.md"], "2.2.0", "2.1.0", False),
        (["skill/SKILL.md"], "2.2.0-rc.1", "2.2.0", True),
        (["skill/SKILL.md"], "2.2.0-rc.2", "2.2.0-rc.1", False),
    ]
    for changed, previous, current, expected in cases:
        assert (not validate_delta(changed, previous, current)) is expected
    print(f"validate_skill_version_delta_cases: OK — {len(cases)} synthetic cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
