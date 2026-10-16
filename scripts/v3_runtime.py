#!/usr/bin/env python3
"""Scoped CLI composition of the unchanged canonical V3 CRUD and Search engines."""
from __future__ import annotations

import argparse
from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys

import yaml

from v3_channel import ChannelError, matches, resolve_channel
from v3_distribution import verify_inventory


def os_principal() -> str:
    """Bind to the running OS credential, never a caller-supplied actor string."""
    if os.name == "nt":
        return subprocess.check_output(["whoami"], text=True, stderr=subprocess.DEVNULL).strip().casefold()
    import pwd
    return pwd.getpwuid(os.getuid()).pw_name


def safe_path(root: Path, relative: str) -> Path:
    from v3_distribution import contained
    path = contained(root, relative)
    for parent in (path, *path.parents):
        if parent == root:
            break
        if parent.is_symlink():
            raise ChannelError("Record/policy path uses a symlink")
    return path


def read_header(path: Path) -> dict:
    """Check identity/scope before loading any Record prose."""
    header = bytearray()
    with path.open("rb") as stream:
        if stream.readline(8) != b"---\n":
            raise ChannelError("selected Record has no canonical header")
        while len(header) <= 1024 * 1024:
            line = stream.readline(1024 * 1024 + 1)
            if line == b"---\n":
                value = yaml.safe_load(header.decode("utf-8"))
                if not isinstance(value, dict):
                    break
                return value
            if not line:
                break
            header.extend(line)
    raise ChannelError("selected Record header is malformed or exceeds the bound")


def runtime_policy(root: Path, relative: str, operation: str) -> dict:
    policy = json.loads(safe_path(root, relative).read_text(encoding="utf-8"))
    if not isinstance(policy, dict):
        raise ChannelError("runtime policy must be a mapping")
    if policy.get("schema_version") != 1 or policy.get("principal") != os_principal():
        raise ChannelError("runtime policy does not authorize the current OS principal")
    if operation not in policy.get("operations", []):
        raise ChannelError("operation is outside the instance policy")
    for field in ("actor", "entity", "vault_id", "scope"):
        if not isinstance(policy.get(field), str) or not policy[field].strip():
            raise ChannelError("runtime policy is missing " + field)
    if not isinstance(policy.get("record_paths"), dict) or len(policy["record_paths"]) > 256:
        raise ChannelError("runtime policy needs a bounded record_paths mapping")
    if not isinstance(policy.get("active_collections"), dict) or not policy["active_collections"]:
        raise ChannelError("runtime policy needs accepted active Collections")
    manifest = yaml.safe_load(safe_path(root, "hipocampo.yaml").read_text(encoding="utf-8"))
    if manifest.get("instance", {}).get("entity") != policy["entity"]:
        raise ChannelError("runtime policy entity does not match the instance manifest")
    if manifest.get("instance", {}).get("repository") != policy.get("repository"):
        raise ChannelError("runtime policy repository does not match the instance manifest")
    policy["compatibility"] = manifest.get("hipocampo", {}).get("compatibility", "")
    return policy


def guard_record(record: dict, policy: dict) -> None:
    if not isinstance(record, dict) or not isinstance(record.get("vault"), dict):
        raise ChannelError("Record proposal/header must carry its canonical mapping and vault")
    if (record.get("entity") != policy["entity"] or record.get("scope") != policy["scope"]
            or record.get("vault", {}).get("vault_id") != policy["vault_id"]
            or policy["record_paths"].get(record.get("record_id")) != record.get("physical_path")):
        raise ChannelError("Record identity/path/entity/vault/scope is outside the granted policy")


def dispatch(root: Path, request: dict, policy: dict) -> dict:
    """Authorization precedes body reads; mutations have exactly one CRUD gateway."""
    from v3_crud_engine import RecordCrud
    from v3_record_store import MarkdownRecordStore, parse_record
    from v3_search_engine import search

    if not isinstance(request, dict):
        raise ChannelError("runtime request must be a mapping")
    operation = request.get("operation")
    if operation not in {"create", "read", "update", "delete", "search"}:
        raise ChannelError("runtime exposes create/read/update/delete(archive)/search")
    if any(key in request for key in ("actor", "authorized_vault_ids", "vault_scope", "entity", "scope")):
        raise ChannelError("request may not supply or widen its authorization context")
    ids = request.get("record_ids") if operation == "search" else [request.get("record_id")]
    if operation == "create":
        guard_record(request.get("record", {}), policy)
        ids = []
    if not isinstance(ids, list) or len(ids) > 64 or (operation != "create" and not ids):
        raise ChannelError("select between one and 64 authorized Record identities")
    records = {}
    for record_id in ids:
        relative = policy["record_paths"].get(record_id)
        if not relative:
            raise ChannelError("Record identity is outside the granted policy")
        path = safe_path(root, relative)
        header = read_header(path)
        guard_record(header, policy)
        if header.get("record_id") != record_id:
            raise ChannelError("selected Record identity does not match its authorized path")
        records[record_id] = parse_record(path.read_bytes())
        guard_record(records[record_id], policy)
    if operation == "update":
        proposed = deepcopy(records[request["record_id"]])
        proposed.update(request.get("patch", {}))
        guard_record(proposed, policy)
    crud = RecordCrud(policy["active_collections"], records,
                      persistence=MarkdownRecordStore(root))
    if operation == "search":
        query = {key: request[key] for key in ("query", "requested_disclosure", "request_id",
                 "presentation", "explicit_structured_request", "explicit_expansion_authorization") if key in request}
        query.update(entity=policy["entity"], knowledge_scope=policy["scope"],
                     vault_scope=[policy["vault_id"]], authorized_vault_ids=[policy["vault_id"]])
        return search(crud, query)
    call = deepcopy(request)
    call["actor"] = {"authorized_vault_ids": [policy["vault_id"]]} if operation == "read" else policy["actor"]
    return crud.apply(call)


def installation_context(installation: Path, channel: str, expected_payload: str) -> tuple[dict, dict, list]:
    metadata = json.loads((installation / "installation.json").read_text(encoding="utf-8"))
    if not isinstance(metadata, dict) or metadata.get("source_repository") != "https://github.com/mklagenberg/hipocampo":
        raise ChannelError("installation source metadata is invalid")
    if metadata.get("channel") != channel:
        raise ChannelError("installed channel differs from explicit invocation; choose the matching channel")
    verify_inventory(installation, metadata["inventory"], expected_payload)
    contract = yaml.safe_load((installation / "COMPATIBILITY.yaml").read_text(encoding="utf-8"))
    diagnostics = resolve_channel(channel, contract["methodology"]["version"],
        contract["methodology"]["supported_vault_range"],
        source_commit=metadata["source_commit"], release=metadata.get("release"))
    return metadata, contract, diagnostics


def execute(installation: Path, instance: Path, request: dict, *, policy_path: str,
            channel: str, expected_payload: str) -> dict:
    metadata, contract, diagnostics = installation_context(installation, channel, expected_payload)
    instance = instance.resolve(strict=True)
    if not isinstance(request, dict):
        raise ChannelError("runtime request must be a mapping")
    policy = runtime_policy(instance, policy_path, request.get("operation"))
    if not matches(contract["methodology"]["version"], policy["compatibility"], experimental=channel == "experimental"):
        raise ChannelError("instance contract is incompatible with the selected distribution")
    result = dispatch(instance, request, policy)
    return {"status": "completed", "result": result, "diagnostics": diagnostics,
            "source": {"commit": metadata["source_commit"], "payload_sha256": expected_payload,
                       "channel": channel}}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--installation", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--instance", type=Path)
    parser.add_argument("--policy", default=".hipocampo/runtime-policy.json")
    parser.add_argument("--channel", choices=("stable", "experimental"), default="stable")
    parser.add_argument("--expected-payload")
    parser.add_argument("--request", type=Path)
    parser.add_argument("--principal", action="store_true", help="show the authenticated OS principal for operator configuration")
    parser.add_argument("--self-test-engines", action="store_true", help="run the complete engine catalogue on synthetic reference fixtures")
    args = parser.parse_args()
    try:
        if args.principal:
            print(json.dumps({"principal": os_principal()}))
            return 0
        if args.self_test_engines:
            _, _, diagnostics = installation_context(args.installation.resolve(), args.channel, args.expected_payload)
            result = subprocess.run([sys.executable, "-B", str(args.installation / "scripts/validate_v3_engine_suite.py"),
                "--root", str(args.installation), "--channel", args.channel], capture_output=True, text=True, encoding="utf-8", errors="replace",
                env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1"))
            print(json.dumps({"status": "completed" if result.returncode == 0 else "blocked",
                "diagnostics": diagnostics, "result": {"engine_suite_exit": result.returncode,
                "output": (result.stdout + result.stderr).strip()}, "privacy": "synthetic-only"}, ensure_ascii=False))
            return 0 if result.returncode == 0 else 2
        if args.instance is None or args.request is None:
            raise ChannelError("--instance and --request are required")
        request = json.loads(args.request.read_text(encoding="utf-8"))
        result = execute(args.installation.resolve(), args.instance, request,
                         policy_path=args.policy, channel=args.channel, expected_payload=args.expected_payload)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        # Do not disclose a Record body or dump a context/policy on failure.
        print(json.dumps({"status": "blocked", "error": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
