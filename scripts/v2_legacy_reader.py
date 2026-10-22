#!/usr/bin/env python3
"""Interpret one already-authorized V2 document; no transport, IAM or writes."""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
from pathlib import Path, PurePosixPath
import re

import yaml
from v3_channel import parse_version
from vault_version_notice import version_notice


class LegacyReadError(ValueError):
    """A typed, body-free denial from the bounded legacy reader."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


_ROOT = Path(__file__).resolve().parents[1]
_VISIBILITY = {"public", "internal", "confidential", "restricted"}
_LIMIT = 2 * 1024 * 1024
_HEADER_LIMIT = 64 * 1024


def _entry(version: str, source_commit: str) -> dict:
    catalog = yaml.safe_load((_ROOT / "OPERATION-SUPPORT.yaml").read_text(encoding="utf-8"))
    for entry in catalog["entries"]:
        if entry["operation"] == "read" and entry["source_version"] == version:
            if entry["source_commit"] != source_commit:
                raise LegacyReadError("source_contract_mismatch")
            if entry["effect"] != "read_only" or entry["adapter"] != "scripts/v2_legacy_reader.py":
                raise LegacyReadError("adapter_contract_mismatch")
            return entry
    raise LegacyReadError("source_contract_unsupported")


def _selected_path(value: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise LegacyReadError("path_invalid")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {".", ".."} for part in value.split("/")):
        raise LegacyReadError("path_invalid")
    if path.suffix.lower() != ".md":
        raise LegacyReadError("path_invalid")
    return str(path)


def _parse(data: bytes) -> tuple[dict, str]:
    if not isinstance(data, bytes) or len(data) > _LIMIT:
        raise LegacyReadError("document_invalid")
    match = re.match(rb"\A---\r?\n(.*?)\r?\n---\r?\n", data[:_HEADER_LIMIT + 8], re.DOTALL)
    if match is None:
        raise LegacyReadError("header_invalid")
    try:
        header = yaml.safe_load(match.group(1).decode("utf-8"))
        body = data[match.end():].decode("utf-8")
    except (UnicodeError, yaml.YAMLError) as exc:
        raise LegacyReadError("document_invalid") from exc
    if not isinstance(header, dict) or not isinstance(body, str):
        raise LegacyReadError("header_invalid")
    return header, body


def read_document(data: bytes, context: dict) -> dict:
    """Return a bounded V2 view after a trusted caller verifies all gates.

    Caller assertions are inputs, not independently authenticated evidence.
    The caller must prove them through the selected GitHub MCP and vault policy
    before fetching bytes. This function never reads a repository or writes.
    """
    if not isinstance(context, dict):
        raise LegacyReadError("context_invalid")
    required = ("source_version", "source_commit", "repository", "path",
                "expected_head", "observed_head", "pre_retrieval_visibility",
                "stable_reference")
    if any(not isinstance(context.get(key), str) or not context[key].strip() for key in required):
        raise LegacyReadError("context_incomplete")
    entry = _entry(context["source_version"], context["source_commit"])
    if context.get("source_contract_verified") is not True:
        raise LegacyReadError("source_contract_unverified")
    stable = parse_version(context["stable_reference"])
    if context.get("stable_reference_verified") is not True or stable is None or stable[1]:
        raise LegacyReadError("published_stable_unverified")
    path = _selected_path(context["path"])
    if context["expected_head"] != context["observed_head"]:
        raise LegacyReadError("ref_changed")
    if context.get("mcp_read_verified") is not True:
        raise LegacyReadError("mcp_read_unavailable")
    if context.get("repository_read_verified") is not True:
        raise LegacyReadError("repository_access_unavailable")
    declared_class = context["pre_retrieval_visibility"]
    if declared_class not in _VISIBILITY:
        raise LegacyReadError("privacy_class_unknown")
    if declared_class in {"confidential", "restricted"} and context.get("specific_grant_verified") is not True:
        raise LegacyReadError("privacy_grant_required")
    header, body = _parse(data)
    if header.get("visibility") != declared_class:
        raise LegacyReadError("privacy_class_mismatch")
    for field in ("title", "source", "type", "status", "revision", "author"):
        if field not in header or header[field] in (None, ""):
            raise LegacyReadError("legacy_header_incomplete")
    age_warning = version_notice(entry["source_version"], context["stable_reference"],
                                 stable_verified=True, source_verified=True)
    if age_warning is None:
        raise LegacyReadError("published_stable_not_newer")
    return {
        "status": "read_only",
        "general_compatibility": "migration_required",
        "operation_support": entry["evidence_level"],
        "source_contract": {"version": entry["source_version"], "ref": entry["source_ref"],
                            "commit": entry["source_commit"]},
        "vault_source": {"repository": context["repository"], "path": path,
                         "ref": context["observed_head"], "sha256": sha256(data).hexdigest()},
        "original_frontmatter": deepcopy(header),
        "body": body,
        "warning": age_warning["message"] + " Bounded read only; no V3 writes.",
        "mutation": "none",
    }
