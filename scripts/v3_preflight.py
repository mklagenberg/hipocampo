#!/usr/bin/env python3
"""Pre-tag readiness, independent of the future tag; preview warnings do not stop engines."""
from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import subprocess
import sys

from v3_distribution import canonical_json, make_inventory, source_identity


def validate_graph(nodes: list[dict]) -> list[str]:
    errors = []
    lookup = {item["id"]: item for item in nodes}
    if len(lookup) != len(nodes):
        return ["duplicate dependency node"]
    phase = {"pre": 0, "publish": 1, "post": 2}
    visiting, done = set(), set()
    def visit(key):
        if key in visiting:
            raise ValueError("cyclic dependency")
        if key in done:
            return
        visiting.add(key)
        for dependency in lookup[key]["needs"]:
            if dependency not in lookup:
                raise ValueError("unknown dependency")
            if phase[lookup[dependency]["phase"]] > phase[lookup[key]["phase"]]:
                raise ValueError("pre-publication task depends on a later publication event")
            visit(dependency)
        visiting.remove(key)
        done.add(key)
    try:
        for key in lookup:
            visit(key)
    except (ValueError, KeyError) as exc:
        errors.append(str(exc))
    return errors


def review_errors(receipt: dict | None, payload: str) -> list[str]:
    if receipt is None:
        return ["final receipt is absent: AI review, independent challenge, human approval and host evidence required"]
    if not isinstance(receipt, dict):
        return ["final receipt must be a mapping"]
    errors = []
    if receipt.get("payload_sha256") != payload:
        errors.append("review receipt belongs to another payload")
    times = []
    sessions = []
    for role in ("ai_review", "independent_challenge", "human_approval"):
        entry = receipt.get(role, {})
        if not isinstance(entry, dict):
            errors.append(role + " is incomplete or malformed")
            continue
        if entry.get("status") != ("approved" if role == "human_approval" else "passed"):
            errors.append(role + " is incomplete")
        if not entry.get("identity") or not entry.get("evidence") or entry.get("payload_sha256") != payload:
            errors.append(role + " needs identity, evidence and exact payload binding")
        try:
            value = entry.get("at")
            if not isinstance(value, str):
                raise ValueError("timestamp is not recorded")
            instant = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if instant.tzinfo is None:
                raise ValueError("timezone required")
            times.append(instant)
        except (KeyError, ValueError, TypeError):
            errors.append(role + " timestamp is invalid")
        if role != "human_approval":
            sessions.append(entry.get("session"))
    if len(times) == 3 and not times[0] < times[1] < times[2]:
        errors.append("reviews must follow AI, independent challenge, then human approval")
    if len(sessions) != 2 or not all(sessions) or sessions[0] == sessions[1]:
        errors.append("independent challenge must use a distinct reviewer session")
    hosts = receipt.get("host_observations", [])
    if not isinstance(hosts, list) or not hosts:
        errors.append("declared-host observations are absent")
    else:
        for host in hosts:
            if not isinstance(host, dict) or host.get("status") != "passed" or not host.get("mode") or not host.get("evidence") or host.get("payload_sha256") != payload:
                errors.append("host observation lacks a passed mode, evidence or payload binding")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--channel", choices=("stable", "experimental"), default="stable")
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--source-commit", help="exact integrated target; required for stable final readiness")
    args = parser.parse_args()
    root = args.root.resolve()
    starting_payload = make_inventory(root)["payload_sha256"]
    reports, failures = [], []
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    commands = ["validate_hipocampo.py", "validate_skill_docs.py", "validate_skill_package.py",
                "validate_compatibility.py", "validate_contracts.py", "validate_change.py",
                "validate_v3_skill_conformance.py",
                "validate_v3_preview_runtime.py", "validate_v3_engine_suite.py"]
    for filename in commands:
        arguments = [sys.executable, "-B", str(root / "scripts" / filename), "--root", str(root)]
        if filename == "validate_v3_preview_runtime.py":
            arguments.append("--engine-context")
        elif filename == "validate_compatibility.py":
            arguments.extend(["--channel", args.channel])
        elif filename == "validate_v3_skill_conformance.py" and args.channel == "experimental":
            arguments.extend(["--mode", "experimental"])
        result = subprocess.run(arguments,
                                capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
        reports.append({"check": filename, "exit_code": result.returncode,
                        "output": (result.stdout + result.stderr).strip()})
        if result.returncode:
            failures.append(filename)
    inventory = make_inventory(root)
    if inventory["payload_sha256"] != starting_payload:
        failures.append("operational payload changed while checks were running; rerun on a frozen source")
    graph = json.loads((root / "docs/release-dependencies.json").read_text(encoding="utf-8"))
    failures.extend(validate_graph(graph["nodes"]))
    for name in ("README.md", "COMPATIBILITY.yaml", "skill/SKILL.md"):
        if "prepared-unreleased" in (root / name).read_text(encoding="utf-8"):
            failures.append(name + " still contains an active preparation-state instruction")
    receipt = json.loads(args.receipt.read_text(encoding="utf-8")) if args.receipt else None
    pending = review_errors(receipt, inventory["payload_sha256"])
    from validate_v3_skill_conformance import validate as validate_conformance
    conformance_errors, conformance_pending = validate_conformance(root, "release", receipt)
    failures.extend(conformance_errors)
    pending = list(dict.fromkeys(pending + conformance_pending))
    if args.channel == "stable":
        try:
            source_identity(root, args.source_commit)
            integrated = subprocess.check_output(["git", "-C", str(root), "rev-parse", "origin/main"], text=True).strip()
            if integrated != args.source_commit:
                pending.append("final source is not the verified origin/main integration target")
        except (ValueError, OSError, subprocess.SubprocessError):
            pending.append("a clean exact integrated source commit is required for final handoff")
    if args.receipt and args.receipt.resolve() in {(root / item["path"]).resolve() for item in inventory["files"]}:
        failures.append("review receipt must remain outside its reviewed payload")
    if args.output and args.output.resolve() in {(root / item["path"]).resolve() for item in inventory["files"]}:
        failures.append("preflight output may not mutate its reviewed payload")
    report = {"status": "blocked" if failures or (pending and args.channel == "stable") else "passed",
              "channel": args.channel, "payload_sha256": inventory["payload_sha256"],
              "checks": reports, "failures": failures,
              "final_readiness_pending": pending,
              "diagnostics": [{"severity": "WARNING", "message": item} for item in pending] if args.channel == "experimental" else []}
    if args.output and not failures:
        args.output.write_bytes(canonical_json(report))
    print(json.dumps(report, ensure_ascii=False))
    return 2 if report["status"] == "blocked" else 0


if __name__ == "__main__":
    sys.exit(main())
