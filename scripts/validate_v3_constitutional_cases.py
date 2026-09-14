#!/usr/bin/env python3
"""Exercise deterministic constitutional exception and rejudgment cases."""
from __future__ import annotations

import argparse
from pathlib import Path


class ConstitutionalBlock(ValueError):
    pass


def authorize_rule(rule: dict, *, constitution_version: str = "1.0.0") -> dict:
    if rule.get("contradicts_constitution"):
        exception = rule.get("exception_decision")
        if not isinstance(exception, dict) or exception.get("status") != "accepted":
            raise ConstitutionalBlock("contradiction without accepted exception Decision Record")
        required = ("clause", "entity", "vault", "scope", "duration", "reason", "risk", "review_condition")
        if any(not exception.get(field) for field in required):
            raise ConstitutionalBlock("exception envelope is incomplete")
        if exception.get("non_waivable_limit"):
            raise ConstitutionalBlock("non-waivable privacy or safety limit cannot be excepted")
        return {"status": "accepted-within-scope", "scope": exception["scope"], "constitution_version": constitution_version}
    return {"status": "compatible", "constitution_version": constitution_version}


def use_rule(rule_result: dict, *, entity: str, vault: str, scope: str) -> str:
    if rule_result["status"] == "accepted-within-scope":
        expected = rule_result["scope"]
        if expected != {"entity": entity, "vault": vault, "scope": scope}:
            raise ConstitutionalBlock("exception used outside declared scope")
    return "allowed"


def rejudge(rule: dict, *, constitution_version: str) -> dict:
    if rule.get("constitution_version") == constitution_version:
        return {"status": "compatible", "review_required": False}
    return {"status": "review-required", "review_required": True}


def privacy_first(operation: dict) -> str:
    if operation.get("privacy") != "passed":
        return "blocked-before-tool-cache-or-export"
    return "continue"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.parse_args()
    errors: list[str] = []

    try:
        authorize_rule({"contradicts_constitution": True})
    except ConstitutionalBlock:
        pass
    else:
        errors.append("unrecorded constitutional contradiction was not blocked")

    incomplete = {
        "contradicts_constitution": True,
        "exception_decision": {"status": "accepted", "clause": "2.9"},
    }
    try:
        authorize_rule(incomplete)
    except ConstitutionalBlock:
        pass
    else:
        errors.append("incomplete exception envelope was not blocked")

    bounded = {
        "contradicts_constitution": True,
        "exception_decision": {
            "status": "accepted", "clause": "2.9", "entity": "entity-a",
            "vault": "vault-a", "scope": {"entity": "entity-a", "vault": "vault-a", "scope": "task-a"},
            "duration": "2026-09-14/2026-09-30", "reason": "bounded test",
            "risk": "accepted-by-owner", "review_condition": "close on task completion",
        },
    }
    try:
        result = authorize_rule(bounded)
        if use_rule(result, entity="entity-a", vault="vault-a", scope="task-a") != "allowed":
            errors.append("bounded exception was not allowed within scope")
    except ConstitutionalBlock as exc:
        errors.append(f"bounded exception was blocked within scope: {exc}")
    try:
        use_rule(result, entity="entity-a", vault="vault-a", scope="task-b")
    except ConstitutionalBlock:
        pass
    else:
        errors.append("bounded exception escaped its declared scope")

    try:
        authorize_rule({**bounded, "exception_decision": {**bounded["exception_decision"], "non_waivable_limit": True}})
    except ConstitutionalBlock:
        pass
    else:
        errors.append("non-waivable limit was incorrectly excepted")

    if rejudge({"constitution_version": "0.9.0"}, constitution_version="1.0.0") != {"status": "review-required", "review_required": True}:
        errors.append("constitutional amendment did not require rejudgment")
    if rejudge({"constitution_version": "1.0.0"}, constitution_version="1.0.0")["review_required"]:
        errors.append("compatible rule was incorrectly marked for review")
    if privacy_first({"privacy": "pending"}) != "blocked-before-tool-cache-or-export":
        errors.append("privacy-first ordering did not block before external processing")

    if errors:
        print(f"validate_v3_constitutional_cases: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_v3_constitutional_cases: OK — exception, scope, rejudgment and privacy-first enforcement")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
