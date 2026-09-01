#!/usr/bin/env python3
"""Validate bounded, non-mutating enforcement-policy simulations."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

def decide(rule: dict, *, authorized: bool, adapter_available: bool) -> str:
    if not adapter_available:
        return "blocked_unavailable"
    if authorized:
        return "allow"
    return rule["decision"]

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    path = Path(args.root).resolve() / "docs" / "enforcement-policy.yaml"
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"validate_enforcement_policy: FAILED — {exc}")
        return 1
    errors = []
    for rule in data.get("rules", []):
        if decide(rule, authorized=False, adapter_available=True) == "allow":
            errors.append(f"{rule.get('id')}: unauthorized operation allowed")
        if decide(rule, authorized=False, adapter_available=False) != "blocked_unavailable":
            errors.append(f"{rule.get('id')}: unavailable adapter did not block")
        if decide(rule, authorized=True, adapter_available=True) != "allow":
            errors.append(f"{rule.get('id')}: authorized operation did not allow")
        if rule.get("barrier") != "pre_execution" or not rule.get("proof_scope"):
            errors.append(f"{rule.get('id')}: incomplete pre-execution proof boundary")
    if errors:
        print(f"validate_enforcement_policy: FAILED — {len(errors)} error(s)")
        for error in errors: print(f"  [FAIL] {error}")
        return 1
    print(f"validate_enforcement_policy: OK — {len(data.get('rules', []))} bounded rules")
    return 0

if __name__ == "__main__":
    sys.exit(main())
