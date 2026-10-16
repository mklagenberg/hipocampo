#!/usr/bin/env python3
"""Real isolated installs/CLI calls; all source metadata and content are fixtures."""
from __future__ import annotations

import argparse
from copy import deepcopy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import patch
import uuid
import zipfile

import yaml

from v3_channel import matches, parse_version, resolve_channel, ChannelError
from v3_distribution import archive, install, make_inventory, payload_files
from v3_runtime import os_principal
from v3_preflight import review_errors, validate_graph


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--engine-context", action="store_true", help="also execute the complete installed engine catalogue through the RC entrypoint")
    args = parser.parse_args()
    root = args.root.resolve()
    workspace = Path(tempfile.gettempdir()) / ("hrt-" + uuid.uuid4().hex[:8])
    workspace.mkdir(parents=True)
    results = []
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")

    def check(condition, label):
        if not condition:
            raise AssertionError(label)
        results.append(label)

    def reject(callback, label):
        try:
            callback()
        except (ChannelError, ValueError):
            results.append(label)
        else:
            raise AssertionError(label)

    def git(path, *argv):
        return subprocess.check_output(["git", "-C", str(path), *argv], text=True, stderr=subprocess.DEVNULL, env=env).strip()

    # The fixture repository has an explicit synthetic commit and canonical-origin
    # configuration. No remote tag/release, private vault or global install is used.
    source = workspace / "source"
    source.mkdir()
    for relative in payload_files(root):
        target = source / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / relative, target)
    contract = yaml.safe_load((source / "COMPATIBILITY.yaml").read_text(encoding="utf-8"))
    base = contract["methodology"]["version"].split("-")[0]
    contract["methodology"]["version"] = base + "-rc.1"
    (source / "COMPATIBILITY.yaml").write_text(yaml.safe_dump(contract, sort_keys=False), encoding="utf-8")
    git(source, "init")
    git(source, "config", "core.autocrlf", "false")
    git(source, "config", "user.name", "Synthetic fixture")
    git(source, "config", "user.email", "fixture@example.invalid")
    git(source, "remote", "add", "origin", "https://github.com/mklagenberg/hipocampo.git")
    git(source, "add", ".")
    git(source, "commit", "-m", "Synthetic isolated RC source; not a publication")
    sha = git(source, "rev-parse", "HEAD")
    inventory = make_inventory(source)
    fingerprint = inventory["payload_sha256"]
    installation = workspace / "installed-experimental"
    outcome = install(source, installation, channel="experimental", source_commit=sha, expected_payload=fingerprint)
    check(outcome["diagnostics"][0]["severity"] == "WARNING", "RC installs without GitHub Release and emits structured warning")
    for host, location in (("claude-code", ".claude/skills"), ("github-copilot", ".github/skills")):
        workspace_path = Path(outcome["host_workspaces"][host])
        check((workspace_path / location / "hipocampo/SKILL.md").read_bytes() == (source / "skill/SKILL.md").read_bytes(),
              host + " isolated workspace contains the exact skill bytes; actual host loading remains unverified")
    reject(lambda: install(source, installation, channel="experimental", source_commit=sha, expected_payload=fingerprint), "existing installation is preserved")
    reject(lambda: install(source, workspace / "bad-hash", channel="experimental", source_commit=sha, expected_payload="0" * 64), "wrong payload blocks installation")

    from v3_crud_engine import RecordCrud
    from v3_record_store import MarkdownRecordStore
    from validate_v3_search_progressive_disclosure import runtime_record
    from validate_v3_crud_use_cases import review
    instance = workspace / "instance"
    instance.mkdir()
    (instance / "records").mkdir()
    manifest = {"hipocampo": {"compatibility": "^3.0.0"},
                "instance": {"entity": "entity-a", "repository": "https://example.invalid/synthetic-instance"}}
    (instance / "hipocampo.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
    collections = {"collection-a": {"collection_id": "collection-a", "active": True}}
    record = runtime_record("rec-one", text="alpha synthetic context")
    policy = {"schema_version": 1, "principal": os_principal(), "actor": "fixture-authorized-actor",
              "entity": "entity-a", "vault_id": "vault-a", "scope": "scope-a",
              "repository": manifest["instance"]["repository"],
              "operations": ["create", "read", "update", "delete", "search"],
              "active_collections": collections,
              "record_paths": {"rec-one": "records/rec-one.md", "rec-two": "records/rec-two.md"}}
    policy_file = instance / ".hipocampo/runtime-policy.json"
    policy_file.parent.mkdir()
    def save_policy(value):
        policy_file.write_text(json.dumps(value), encoding="utf-8")
    save_policy(policy)
    crud = RecordCrud(collections, records={}, persistence=MarkdownRecordStore(instance))
    crud.create(record, semantic_review=review("rec-one"), actor="fixture-curator", reason="synthetic test setup")

    def cli(request, *, channel="experimental", expected=0):
        request_file = workspace / (uuid.uuid4().hex + ".json")
        request_file.write_text(json.dumps(request), encoding="utf-8")
        run = subprocess.run([sys.executable, "-B", str(installation / "scripts/v3_runtime.py"),
            "--instance", str(instance), "--channel", channel, "--expected-payload", fingerprint,
            "--request", str(request_file)], capture_output=True, text=True, encoding="utf-8", env=env)
        value = json.loads(run.stdout)
        if run.returncode != expected:
            raise AssertionError((request.get("operation"), run.returncode, value, run.stderr))
        check(not run.stderr, "CLI response preserves protocol without stderr-as-error")
        return value

    read = cli({"operation": "read", "record_id": "rec-one"})
    check(read["result"]["record"]["content"] == record["content"], "real installed RC dispatch reads canonical Record")
    check(read["diagnostics"][0]["code"] == "EXPERIMENTAL_SNAPSHOT", "warning survives entrypoint and result envelope")
    artifact = archive(source, workspace / "candidate.zip", source_commit=sha, expected_payload=fingerprint)
    repeated = archive(source, workspace / "candidate-rebuild.zip", source_commit=sha, expected_payload=fingerprint)
    check(artifact["archive_sha256"] == repeated["archive_sha256"], "distribution ZIP is reproducible before any release exists")
    extracted = workspace / "extracted"
    with zipfile.ZipFile(workspace / "candidate.zip") as package:
        package.extractall(extracted)
    archive_install = workspace / "archive-installed"
    installed_asset = install(extracted, archive_install, channel="experimental", source_commit=sha, expected_payload=fingerprint)
    check(installed_asset["status"] == "installed", "explicit release asset is installable without a Git checkout")
    result = cli({"operation": "search", "record_ids": ["rec-one"], "request_id": "fixture-search",
                  "query": "alpha", "requested_disclosure": "L2"})
    check(bool(result["result"]), "real installed RC dispatch executes canonical Search")
    cli({"operation": "read", "record_id": "rec-one"}, channel="stable", expected=2)
    results.append("stable default cannot silently consume an experimental installation")
    cli({"operation": "read", "record_id": "rec-one", "actor": {"authorized_vault_ids": ["other"]}}, expected=2)
    results.append("request cannot inject an authorization context")
    cli({"operation": "read", "record_id": "not-authorized"}, expected=2)
    results.append("unauthorized Record remains blocked")
    denied = deepcopy(policy); denied["principal"] = "not-the-running-principal"; save_policy(denied)
    cli({"operation": "read", "record_id": "rec-one"}, expected=2)
    save_policy(policy); results.append("OS-principal mismatch remains blocked")
    second = runtime_record("rec-two", text="second synthetic context")
    created = cli({"operation": "create", "record": second, "semantic_review": review("rec-two"),
                   "reason": "explicit fixture create", "idempotency_key": "fixture-create"})
    check(created["result"]["status"] == "accepted", "RC create persists only through canonical CRUD")
    cli({"operation": "read", "record_id": "rec-two"})
    results.append("fresh process reloads created Record")
    updated = cli({"operation": "update", "record_id": "rec-two", "patch": {"content": "Updated synthetic prose"},
                   "expected_version": 1, "semantic_review": review("rec-two"), "reason": "fixture update"})
    check(updated["result"]["record"]["record_version"] == 2, "RC update preserves versioned CRUD")
    cli({"operation": "update", "record_id": "rec-two", "patch": {"content": "stale"}, "expected_version": 1,
         "semantic_review": review("rec-two"), "reason": "stale fixture"}, expected=2)
    results.append("RC does not downgrade stale-version errors")
    cli({"operation": "delete", "record_id": "rec-two", "expected_version": 2,
         "semantic_review": review("rec-two"), "reason": "archive fixture"})
    archived = cli({"operation": "read", "record_id": "rec-two"})
    check(archived["result"]["record"]["status"] == "archived", "delete retains canonical archive semantics")
    if args.engine_context:
        engine_run = subprocess.run([sys.executable, "-B", str(installation / "scripts/v3_runtime.py"),
            "--channel", "experimental", "--expected-payload", fingerprint, "--self-test-engines"],
            capture_output=True, text=True, encoding="utf-8", env=env)
        engine_result = json.loads(engine_run.stdout)
        check(engine_run.returncode == 0, "entire installed engine catalogue executes through real RC entrypoint: " + str(engine_result))
        check(engine_result["diagnostics"][0]["severity"] == "WARNING", "catalogue execution retains nonfatal RC diagnostic")
    (installation / "README.md").write_text("tampered fixture", encoding="utf-8")
    cli({"operation": "read", "record_id": "rec-one"}, expected=2)
    results.append("post-install payload tampering remains blocked")

    for invalid in ("3.01.0", "3.1.0-rc.01", "3.1.0-", "3.1", "vv3.1.0"):
        check(parse_version(invalid) is None, "reject malformed version " + invalid)
    check(matches("3.1.0-rc.1", "^3.0.0", experimental=True), "explicit experimental range permits compatible RC")
    check(not matches("3.1.0-rc.1", "^3.0.0"), "stable range excludes RC by default")
    check(not matches("4.0.0-rc.1", "^3.0.0", experimental=True), "experimental preserves major compatibility")
    check(matches("0.0.1", "^0.0.1") and not matches("0.0.2", "^0.0.1"), "caret zero patch range remains bounded")
    stable = {"immutable": True, "draft": False, "prerelease": False, "tag_name": "v3.1.0", "resolved_commit": sha}
    check(resolve_channel("stable", "3.1.0", "^3.0.0", source_commit=sha, release=stable) == [], "synthetic stable evidence has no candidate warning")
    reject(lambda: resolve_channel("stable", "3.1.0", "^3.0.0", source_commit=sha), "stable still requires published immutable evidence")
    check(bool(review_errors(None, fingerprint)), "missing final review receipt is never treated as approval")
    graph = [{"id": "before", "phase": "pre", "needs": []}, {"id": "after", "phase": "post", "needs": ["before"]}]
    check(not validate_graph(graph), "ordered pre/post graph passes")
    graph[0]["needs"] = ["after"]
    check(bool(validate_graph(graph)), "pre-tag dependency on post-tag work is rejected")
    print(json.dumps({"suite": "v3-preview-runtime", "privacy": "synthetic-only", "passed": len(results),
                      "cases": results, "limitations": "No external host, remote RC/release, private vault or real approval exercised."}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
