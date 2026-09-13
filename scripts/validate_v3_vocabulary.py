#!/usr/bin/env python3
"""Validate candidate V3 aliases without persisting conversational aliases."""
from __future__ import annotations

from v3_vocabulary import persisted_type, resolve_alias


def main() -> int:
    errors: list[str] = []
    checks = [
        ("create a note", "Record"),
        ("use the fonte", "Source"),
        ("send this to the second brain", "Hipocampo"),
    ]
    for utterance, expected in checks:
        result = resolve_alias(utterance)
        if result["status"] != "resolved" or result["canonical"] != expected:
            errors.append(f"alias did not resolve: {utterance!r}")
    if persisted_type(resolve_alias("send this to the second brain")) is not None:
        errors.append("methodology routing alias became a persisted type")
    ambiguous = resolve_alias("save this in the vault")
    if ambiguous["status"] != "clarification_required":
        errors.append("ambiguous vault destination did not request clarification")
    if "personal vault" not in str(ambiguous["question"]) or "company vault" not in str(ambiguous["question"]):
        errors.append("clarification question was not didactic enough")
    if errors:
        print(f"validate_v3_vocabulary: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_v3_vocabulary: OK — canonical routing, ambiguity and persistence boundaries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
