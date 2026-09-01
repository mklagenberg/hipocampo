#!/usr/bin/env python3
"""Flag non-placeholder @handles in explicitly supplied new/changed files."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HANDLE = re.compile(r"(?<![A-Za-z0-9])@[A-Za-z0-9][A-Za-z0-9_-]{1,38}")
ALLOWED = {"@example", "@handle", "@github-username", "@personal-handle", "@section-name", "@mklagenberg"}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", help="explicit new or changed files only")
    args = parser.parse_args()
    findings = []
    for filename in args.files:
        path = Path(filename)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            findings.append(f"{path}: unavailable ({exc})")
            continue
        for match in HANDLE.finditer(text):
            if match.group() not in ALLOWED:
                findings.append(f"{path}: nominal citation {match.group()!r}")
    if findings:
        print(f"validate_nominal_citations: FAILED — {len(findings)} finding(s)")
        for finding in findings: print(f"  [FAIL] {finding}")
        return 1
    print(f"validate_nominal_citations: OK — {len(args.files)} file(s), no non-placeholder handles")
    return 0

if __name__ == "__main__":
    sys.exit(main())
