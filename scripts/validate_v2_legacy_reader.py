#!/usr/bin/env python3
"""Synthetic, side-effect-free contract cases for exact V2 read releases."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import subprocess
import sys

import yaml

from v2_legacy_reader import LegacyReadError, read_document
from validate_compatibility import state as compatibility_state


ROOT = Path(__file__).resolve().parents[1]
CATALOG = yaml.safe_load((ROOT / "OPERATION-SUPPORT.yaml").read_text(encoding="utf-8"))


def document(*, visibility: str = "internal", crlf: bool = False) -> bytes:
    text = ("---\n"
            "title: Example\nsource: conversa\ntype: note\nstatus: active\n"
            "revision: 1\nauthor: Example Author\n"
            f"visibility: {visibility}\nunknown_legacy_field: stay\n"
            "---\nUnicode: ação, café, 東京.\n")
    return text.replace("\n", "\r\n").encode("utf-8") if crlf else text.encode("utf-8")


def context(entry: dict, **changes: object) -> dict:
    value = {"source_version": entry["source_version"],
             "source_commit": entry["source_commit"],
             "repository": "owner/synthetic-vault", "path": "notes/example.md",
             "expected_head": "a" * 40, "observed_head": "a" * 40,
             "pre_retrieval_visibility": "internal", "stable_reference": "3.0.1",
             "mcp_read_verified": True, "repository_read_verified": True,
             "specific_grant_verified": False}
    value.update(changes)
    return value


def denies(code: str, data: bytes, supplied: dict) -> None:
    try:
        read_document(data, supplied)
    except LegacyReadError as exc:
        assert exc.code == code, (code, exc.code)
    else:
        raise AssertionError("expected denial: " + code)


def main() -> int:
    entries = CATALOG["entries"]
    assert [item["source_version"] for item in entries] == ["2.0.0", "2.1.0", "2.1.1", "2.2.0"]
    assert all(item["operation"] == "read" and item["effect"] == "read_only" for item in entries)
    assert all(item["host_evidence"] == "not_assessed" for item in entries)
    cases = 0
    for entry in entries:
        commit = subprocess.check_output(
            ["git", "rev-list", "-n", "1", entry["source_ref"]],
            cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
        assert commit == entry["source_commit"], entry["source_ref"]
        historical_spec = subprocess.check_output(
            ["git", "show", entry["source_ref"] + ":SPEC.md"],
            cwd=ROOT, text=True, encoding="utf-8", stderr=subprocess.DEVNULL)
        assert all(field in historical_spec for field in
                   ("visibility:", "source:", "revision:", "author:", "status:"))
        original = document(crlf=entry["source_version"] == "2.1.1")
        saved = bytes(original)
        supplied = context(entry)
        saved_context = deepcopy(supplied)
        result = read_document(original, supplied)
        assert result["general_compatibility"] == "migration_required"
        assert result["operation_support"] == entry["evidence_level"]
        assert result["body"].endswith("ação, café, 東京.\r\n" if b"\r\n" in original else "ação, café, 東京.\n")
        assert result["original_frontmatter"]["source"] == "conversa"
        assert result["original_frontmatter"]["unknown_legacy_field"] == "stay"
        assert result["mutation"] == "none" and original == saved and supplied == saved_context
        assert entry["source_version"] in result["warning"]
        assert compatibility_state({
            "sources_available": True, "package_integrity": True,
            "methodology_version": "3.1.0", "skill_methodology_range": "^3.0.0",
            "vault_range": "^2.1.1" if entry["source_version"] != "2.0.0" else "^2.0.0",
        }) == "migration_required"
        cases += 1
    entry = entries[2]
    value = document()
    tests = [
        ("mcp_read_unavailable", value, context(entry, mcp_read_verified=False)),
        ("repository_access_unavailable", value, context(entry, repository_read_verified=False)),
        ("source_contract_mismatch", value, context(entry, source_commit="0" * 40)),
        ("source_contract_unsupported", value, context(entry, source_version="2.1.2")),
        ("ref_changed", value, context(entry, observed_head="b" * 40)),
        ("privacy_class_unknown", value, context(entry, pre_retrieval_visibility="unknown")),
        ("privacy_class_mismatch", value, context(entry, pre_retrieval_visibility="public")),
        ("privacy_grant_required", document(visibility="restricted"),
         context(entry, pre_retrieval_visibility="restricted")),
        ("path_invalid", value, context(entry, path="../notes/example.md")),
        ("header_invalid", b"no yaml\n", context(entry)),
        ("legacy_header_incomplete", value.replace(b"revision: 1\n", b""), context(entry)),
    ]
    for code, data, supplied in tests:
        denies(code, data, supplied)
        cases += 1
    restricted = read_document(document(visibility="restricted"),
                               context(entry, pre_retrieval_visibility="restricted",
                                       specific_grant_verified=True))
    assert restricted["original_frontmatter"]["visibility"] == "restricted"
    cases += 1
    assert compatibility_state({
        "sources_available": True, "package_integrity": True,
        "methodology_version": "3.1.0", "skill_methodology_range": "^3.0.0",
        "vault_range": "^3.0.0",
    }) == "compatible"
    cases += 1
    assert "Operation support" in (ROOT / "docs/taxonomy.md").read_text(encoding="utf-8")
    assert "pre-retrieval privacy" in (ROOT / "docs/legacy-read-support.md").read_text(encoding="utf-8")
    print(f"validate_v2_legacy_reader: OK — {cases} synthetic cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
