#!/usr/bin/env python3
"""Plan or apply an explicitly reviewed V2-to-V3 Record migration via canonical CRUD."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import yaml

from v3_crud_engine import ContractError, RecordCrud, validate_record_semantics, validate_record_structure
from v3_migration_engine import SHA256_RE, validate_execution_manifest
from v3_record_store import MarkdownRecordStore, serialize_record


def _safe_path(root: Path, relative_path: str) -> Path:
    candidate = Path(relative_path)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ContractError("source path must stay repository-relative")
    target = (root / candidate).resolve(strict=False)
    if not target.is_relative_to(root):
        raise ContractError("source path escapes the repository")
    return target


def _load_manifest(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ContractError("migration manifest must be a mapping")
    return data


def _preflight(manifest: dict) -> str:
    return validate_execution_manifest(manifest)


def _inspect_record(root: Path, manifest: dict, item: dict) -> str:
    required = {
        "source_path", "source_sha256", "mapping_ref", "privacy_review_ref",
        "semantic_review", "record", "reason", "idempotency_key",
    }
    if not isinstance(item, dict) or required - item.keys():
        return "record_mapping_incomplete"
    if not SHA256_RE.fullmatch(str(item.get("source_sha256", ""))):
        return "source_fingerprint_invalid"
    if not item.get("mapping_ref") or not item.get("privacy_review_ref"):
        return "review_references_missing"
    try:
        source = _safe_path(root, item["source_path"])
        record = validate_record_structure(item["record"], manifest["active_collections"])
        if record.get("vault", {}).get("vault_id") != manifest["vault_id"]:
            return "target_vault_mismatch"
        if record.get("physical_path") != item["source_path"]:
            return "physical_path_changed"
        semantic_operation = "current-use" if record.get("current_use") else "migration"
        validate_record_semantics(record, item["semantic_review"], operation=semantic_operation)
        if item["semantic_review"].get("decision") != "accepted":
            return "semantic_review_not_accepted"
        if not item.get("reason") or not item.get("idempotency_key"):
            return "crud_request_incomplete"
    except (ContractError, OSError, TypeError, KeyError):
        return "record_validation_failed"
    if not source.is_file():
        return "source_missing"
    source_bytes = source.read_bytes()
    if source_bytes == serialize_record(record):
        return "migration_already_started"
    if hashlib.sha256(source_bytes).hexdigest() != item["source_sha256"]:
        return "source_fingerprint_mismatch"
    return "ready"


def _git_apply_gate(root: Path) -> str | None:
    try:
        branch = subprocess.run(
            ["git", "-C", str(root), "branch", "--show-current"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        top_level = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        main_ancestor = subprocess.run(
            ["git", "-C", str(root), "merge-base", "--is-ancestor", "main", "HEAD"],
            capture_output=True, text=True, check=False,
        ).returncode
        status = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain", "-z"],
            capture_output=True, text=True, check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return "git_repository_unavailable"
    if not branch.startswith("migration/"):
        return "dedicated_migration_branch_required"
    if Path(top_level).resolve() != root:
        return "vault_root_must_be_repository_root"
    if main_ancestor != 0:
        return "migration_branch_must_include_current_main"
    if status:
        return "working_tree_must_be_clean_before_apply"
    return None


def run(root: Path, manifest: dict, *, mode: str) -> tuple[int, dict]:
    root = root.resolve(strict=True)
    global_status = _preflight(manifest)
    if global_status != "ready":
        return 2, {"status": "blocked", "reason": global_status, "records": 0, "written": 0, "already_applied": 0}
    if mode == "apply":
        gate = _git_apply_gate(root)
        if gate:
            return 2, {
                "status": "blocked", "reason": gate, "records": len(manifest["records"]),
                "written": 0, "already_applied": 0,
            }
    statuses = [
        _inspect_record(root, manifest, item)
        for item in manifest["records"]
    ]
    blocked = sum(status != "ready" for status in statuses)
    already = 0
    if blocked:
        return 2, {
            "status": "blocked", "records": len(statuses), "ready": statuses.count("ready"),
            "blocked": blocked, "already_applied": already, "written": 0,
        }
    if mode == "dry-run":
        return 0, {
            "status": "ready", "records": len(statuses), "ready": statuses.count("ready"),
            "blocked": 0, "already_applied": 0, "written": 0,
        }

    store = MarkdownRecordStore(root)
    crud = RecordCrud(manifest["active_collections"], persistence=store)
    written = 0
    try:
        for item in manifest["records"]:
            result = crud.migrate(
                item["record"],
                source_path=item["source_path"],
                expected_source_sha256=item["source_sha256"],
                semantic_review=item["semantic_review"],
                migration_context=manifest,
                actor=manifest["actor"],
                reason=item["reason"],
                idempotency_key=item["idempotency_key"],
            )
            if result["status"] == "accepted":
                written += 1
    except (ContractError, OSError):
        return 3, {
            "status": "partial", "records": len(statuses), "written": written,
            "already_applied": already, "blocked": len(statuses) - written - already,
        }
    return 0, {
        "status": "completed", "records": len(statuses), "written": written,
        "already_applied": already, "blocked": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault-root", required=True)
    parser.add_argument("--manifest")
    parser.add_argument("--mode", choices=("dry-run", "apply"), default="dry-run")
    args = parser.parse_args()
    root = Path(args.vault_root)
    if not args.manifest:
        print(json.dumps({
            "status": "blocked", "reason": "mapping_manifest_required",
            "records": 0, "written": 0, "already_applied": 0,
        }, sort_keys=True))
        return 2
    try:
        manifest = _load_manifest(Path(args.manifest))
        code, report = run(root, manifest, mode=args.mode)
    except (OSError, yaml.YAMLError, ContractError):
        # Error messages are intentionally limited to schema/path diagnostics;
        # never print source Record content or manifest values.
        print(json.dumps({"status": "blocked", "reason": "manifest_unreadable_or_invalid", "written": 0}, sort_keys=True))
        return 2
    print(json.dumps(report, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
