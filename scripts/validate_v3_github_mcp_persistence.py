#!/usr/bin/env python3
"""Synthetic tests for the GitHub MCP CAS persistence adapter."""
from __future__ import annotations

import argparse
import base64
import hashlib
from pathlib import Path
from urllib.parse import unquote, urlparse

from v3_crud_engine import ContractError, RecordCrud
from v3_github_mcp_persistence import GitHubMcpCrudAdapter, GitHubMcpGitDataBridge, GitHubMcpRecordPersistence, GitHubMcpUnavailable
from v3_runtime import dispatch
from validate_v3_crud_use_cases import ACTIVE_COLLECTIONS, base_record, request, review


FIXTURE_SOURCE = {"methodology_version": "3.1.0", "source_method_version": "3.1.0",
                  "source_commit": "fixture-method-source-commit"}


class FakeGitHubMcp:
    def __init__(self):
        self.head = "head-0"
        self.files: dict[str, bytes] = {}
        self.drop_next_commit_response = False
        self.drift_after_receipt_read = False

    def invoke(self, operation: str, args: dict) -> dict:
        if operation == "list_record_paths":
            return {"paths": sorted(self.files)}
        if operation == "read_ref":
            return {"head_sha": self.head}
        if operation == "read_file":
            observed_head = self.head
            content = self.files.get(args["path"])
            result = {"head_sha": observed_head, "content_base64": base64.b64encode(content).decode() if content is not None else None}
            if self.drift_after_receipt_read and "operation-receipts/record-mutations/" in args["path"]:
                self.drift_after_receipt_read = False
                self.head = hashlib.sha256((self.head + "drift").encode()).hexdigest()
            return result
        if operation == "commit_file_cas":
            if args["expected_head_sha"] != self.head:
                raise ContractError("expected-head conflict")
            prior = self.files.get(args["path"])
            expected_file_sha = args.get("expected_file_sha256")
            actual_file_sha = hashlib.sha256(prior).hexdigest() if prior is not None else None
            if expected_file_sha != actual_file_sha:
                raise ContractError("expected-file conflict")
            content = base64.b64decode(args["content_base64"], validate=True)
            self.files[args["path"]] = content
            additions = args.get("additional_files", [])
            for item in additions:
                if item.get("path") in self.files:
                    raise ContractError("synthetic receipt path already exists")
                self.files[item["path"]] = base64.b64decode(item["content_base64"], validate=True)
            committed = "".join(path + self.files[path].hex() for path in sorted([args["path"]] + [item["path"] for item in additions]))
            self.head = hashlib.sha256((self.head + committed).encode()).hexdigest()
            if self.drop_next_commit_response:
                self.drop_next_commit_response = False
                raise OSError("synthetic lost MCP response after commit")
            return {"status": "committed", "commit_sha": self.head, "head_sha": self.head}
        raise AssertionError(f"unexpected operation: {operation}")


class FakeGitHubTools:
    """Tool-callable fixture that models Git Data objects and expected_sha ref leases."""

    def __init__(self):
        self.heads = {"runtime-fixture": "commit-0", "homologation/runtime-fixture": "commit-0"}
        self.trees = {"tree-0": {"README.md": b"preserve sibling", "records/pinned.md": b"old snapshot"}}
        self.commits = {"commit-0": "tree-0"}
        self.snapshots = {"commit-0": dict(self.trees["tree-0"])}
        self.blobs: dict[str, bytes] = {}
        self.call_order: list[str] = []
        self.drift_on_next_ref = False

    def fetch_git_data(self, *, url: str):
        self.call_order.append("fetch_git_data")
        if "%2f" in url.lower():
            raise AssertionError("GitHub MCP fetch rejects encoded branch separators")
        parsed = urlparse(url)
        segments = [unquote(part) for part in parsed.path.split("/") if part]
        if "heads" in segments:
            branch = "/".join(segments[segments.index("heads") + 1:])
            sha = self.heads[branch]
            response = {"structuredContent": {"content": __import__("json").dumps({"object": {"sha": sha}})}}
            if self.drift_on_next_ref:
                self.drift_on_next_ref = False
                self.snapshots["commit-drift"] = {"README.md": b"preserve sibling", "records/pinned.md": b"new snapshot"}
                self.heads[branch] = "commit-drift"
            return response
        commit_sha = segments[-1]
        return {"structuredContent": {"content": __import__("json").dumps({"tree": {"sha": self.commits[commit_sha]}})}}

    def fetch_file(self, *, repository_full_name: str, path: str, ref: str, encoding: str):
        self.call_order.append("fetch_file")
        data = self.snapshots.get(ref, {}).get(path)
        if data is None:
            return {"isError": True, "structuredContent": {"error_code": "NOT_FOUND", "error_data": {"status": "404"}}}
        encoded = base64.b64encode(data).decode("ascii")
        wrapped = "\n".join(encoded[index:index + 60] for index in range(0, len(encoded), 60))
        return {"structuredContent": {"content": wrapped, "encoding": "base64"}}

    def create_blob(self, *, repository_full_name: str, content: str, encoding: str):
        self.call_order.append("create_blob")
        data = base64.b64decode(content, validate=True)
        sha = hashlib.sha1(data).hexdigest()
        self.blobs[sha] = data
        return {"sha": sha}

    def create_tree(self, *, repository_full_name: str, base_tree_sha: str, tree_elements: list[dict]):
        self.call_order.append("create_tree")
        tree = dict(self.trees[base_tree_sha])
        for element in tree_elements:
            tree[element["path"]] = self.blobs[element["sha"]]
        sha = "tree-" + hashlib.sha1(repr(sorted((key, value.hex()) for key, value in tree.items())).encode()).hexdigest()
        self.trees[sha] = tree
        return {"sha": sha}

    def create_commit(self, *, repository_full_name: str, message: str, parent_sha: str, tree_sha: str):
        self.call_order.append("create_commit")
        sha = "commit-" + hashlib.sha1(f"{parent_sha}:{tree_sha}:{message}".encode()).hexdigest()
        self.commits[sha] = tree_sha
        self.snapshots[sha] = dict(self.trees[tree_sha])
        return {"sha": sha}

    def update_ref(self, *, repository_full_name: str, branch_name: str, expected_sha: str, force: bool, sha: str):
        self.call_order.append("update_ref")
        if self.heads[branch_name] != expected_sha:
            raise ContractError("expected_sha lease mismatch")
        if force:
            raise AssertionError("force updates must not be used")
        self.heads[branch_name] = sha
        return {"object": {"sha": sha}}

    def mapping(self) -> dict:
        return {"fetch_git_data": self.fetch_git_data, "fetch_file": self.fetch_file,
                "create_blob": self.create_blob, "create_tree": self.create_tree,
                "create_commit": self.create_commit, "update_ref": self.update_ref}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.parse_args()
    errors: list[str] = []
    try:
        GitHubMcpRecordPersistence(lambda _operation, _args: {}, repository="fixture/repo", branch="main",
                                  capabilities={"read_ref", "read_file", "commit_file_cas"})
        errors.append("real persistence accepted missing verified source identity pins")
    except ContractError:
        pass
    fake = FakeGitHubMcp()
    persistence = GitHubMcpRecordPersistence(fake.invoke, repository="fixture/repo", branch="crud-fixture",
                                             capabilities={"list_record_paths", "read_ref", "read_file", "commit_file_cas"},
                                             synthetic=True, **FIXTURE_SOURCE)
    crud = RecordCrud(ACTIVE_COLLECTIONS, persistence=persistence)
    adapter = GitHubMcpCrudAdapter(crud, persistence)
    first = adapter.call(request(base_record("remote-001"), key="remote-create-001"))
    if first.get("remote_receipt", {}).get("readback_confirmed") is not True:
        errors.append("create did not return remote readback receipt")
    if first.get("evidence_level") != "synthetic-adapter":
        errors.append("synthetic MCP fixture was mislabeled as host evidence")
    if len(fake.files) != 2 or "remote-001" not in crud.records:
        errors.append("accepted create did not persist exactly once through canonical CRUD")
    replay = adapter.call(request(base_record("remote-001"), key="remote-create-001"))
    if not replay.get("remote_receipt", {}).get("replayed_from_durable_receipt"):
        errors.append("same-request retry did not replay from the durable sidecar receipt")
    receipt_path = persistence._receipt_path("remote-create-001")
    durable_receipt = persistence._decode_receipt(fake.files.get(receipt_path))
    if (not durable_receipt or durable_receipt.get("key_hash") != hashlib.sha256(b"remote-create-001").hexdigest()
            or "remote-create-001" in str(durable_receipt) or durable_receipt.get("expected_base_head") != "head-0"
            or durable_receipt.get("reason_sha256") != hashlib.sha256(b"fixture operation").hexdigest()
            or "reason" in durable_receipt):
        errors.append("sidecar omitted the hashed key/base binding or persisted the raw idempotency key")
    different_key_persistence = GitHubMcpRecordPersistence(fake.invoke, repository="fixture/repo", branch="crud-fixture",
        capabilities={"read_ref", "read_file", "commit_file_cas"}, synthetic=True, **FIXTURE_SOURCE)
    different_key_crud = RecordCrud(ACTIVE_COLLECTIONS, records={}, persistence=different_key_persistence)
    try:
        GitHubMcpCrudAdapter(different_key_crud, different_key_persistence).call(
            request(base_record("remote-001"), key="different-key-same-content"))
        errors.append("identical content under a different idempotency key was deduplicated")
    except ContractError:
        pass
    fake.drift_after_receipt_read = True
    try:
        adapter.call(request(base_record("remote-001"), key="remote-create-001"))
        errors.append("receipt and Record readback at different heads were accepted")
    except ContractError:
        pass
    changed_retry = request(base_record("remote-001"), key="remote-create-001")
    changed_retry["record"]["content"] = "different payload"
    try:
        adapter.call(changed_retry)
        errors.append("durable idempotency key accepted a different request fingerprint")
    except ContractError:
        pass
    replay_persistence = GitHubMcpRecordPersistence(fake.invoke, repository="fixture/repo", branch="crud-fixture",
        capabilities={"read_ref", "read_file", "commit_file_cas"}, synthetic=True, **FIXTURE_SOURCE)
    replay_crud = RecordCrud(ACTIVE_COLLECTIONS, records={}, persistence=replay_persistence)
    durable_replay = GitHubMcpCrudAdapter(replay_crud, replay_persistence).call(
        request(base_record("remote-001"), key="remote-create-001"))
    if not durable_replay.get("remote_receipt", {}).get("replayed_from_durable_receipt"):
        errors.append("fresh CRUD process could not replay from the durable sidecar")
    before = fake.head
    update = adapter.call({"operation": "update", "record_id": "remote-001", "expected_version": 1,
                           "patch": {"scope": "project-alpha-v2"}, "semantic_review": review("remote-001"),
                           "actor": "curator-001", "reason": "scope refinement", "idempotency_key": "remote-update-001"})
    if update["record"]["record_version"] != 2 or update["remote_receipt"].get("base_head_sha") != before:
        errors.append("update omitted expected-head versioned persistence evidence")
    stale = {"operation": "update", "record_id": "remote-001", "expected_version": 1,
             "patch": {"scope": "stale"}, "semantic_review": review("remote-001"),
             "actor": "curator-001", "reason": "stale write", "idempotency_key": "stale-001"}
    try:
        adapter.call(stale)
        errors.append("stale expected_version update was accepted")
    except ContractError:
        pass
    if crud.records["remote-001"]["record_version"] != 2:
        errors.append("failed update mutated canonical in-memory state")
    try:
        adapter.call(request(base_record("remote-001"), key="remote-create-001"))
        errors.append("old durable receipt claimed success after the Record advanced")
    except ContractError:
        pass
    uncertain = request(base_record("remote-uncertain"), key="lost-response-001")
    fake.drop_next_commit_response = True
    try:
        adapter.call(uncertain)
        errors.append("synthetic lost response was not surfaced")
    except OSError:
        pass
    if "remote-uncertain" in crud.records:
        errors.append("uncertain commit mutated canonical state before reconciliation")
    recovered = adapter.call(uncertain)
    if recovered.get("remote_receipt", {}).get("replayed_from_durable_receipt") is not True or "remote-uncertain" not in crud.records:
        errors.append("retry did not reconcile a committed write after lost response")
    limited = GitHubMcpRecordPersistence(fake.invoke, repository="fixture/repo", branch="crud-fixture",
                                         capabilities={"list_record_paths", "read_ref", "read_file"},
                                         synthetic=True, **FIXTURE_SOURCE)
    try:
        limited._require("commit_file_cas")
        errors.append("missing CAS capability did not fail closed")
    except GitHubMcpUnavailable:
        pass
    runtime_fake = FakeGitHubMcp()
    runtime_persistence = GitHubMcpRecordPersistence(
        runtime_fake.invoke, repository="fixture/runtime-repo", branch="runtime-fixture",
        capabilities={"list_record_paths", "read_ref", "read_file", "commit_file_cas"}, synthetic=True,
        **FIXTURE_SOURCE,
    )
    runtime_policy = {
        "repository": "fixture/runtime-repo", "actor": "curator-001", "entity": "entity-a",
        "vault_id": "vault-a", "scope": "project-alpha", "record_paths": {
            "runtime-001": "records/runtime-001.md",
        }, "active_collections": ACTIVE_COLLECTIONS,
    }
    try:
        runtime_request = request(base_record("runtime-001"), key="runtime-create-001")
        runtime_request.pop("actor", None)
        runtime_result = dispatch(
            Path("."), runtime_request,
            runtime_policy, remote_persistence=runtime_persistence,
        )
        receipt = runtime_result.get("remote_receipt", {})
        if (runtime_result.get("status") != "accepted" or runtime_result.get("transport") != "mcp"
                or receipt.get("readback_confirmed") is not True or "records/runtime-001.md" not in runtime_fake.files):
            errors.append("runtime -> RecordCrud -> MCP persistence path did not confirm remote create")
        read_result = dispatch(
            Path("."), {"operation": "read", "record_id": "runtime-001"},
            runtime_policy, remote_persistence=runtime_persistence,
        )
        if read_result.get("record", {}).get("record_id") != "runtime-001":
            errors.append("runtime remote read did not load the policy-selected remote Record")
    except Exception as exc:
        errors.append(f"runtime remote CRUD composition failed: {type(exc).__name__}: {exc}")
    wrong_repo_policy = {**runtime_policy, "repository": "other/repo"}
    try:
        dispatch(Path("."), {"operation": "read", "record_id": "runtime-001"},
                 wrong_repo_policy, remote_persistence=runtime_persistence)
        errors.append("runtime accepted remote persistence for a mismatched repository")
    except ValueError:
        pass
    tools = FakeGitHubTools()
    bridge = GitHubMcpGitDataBridge(tools.mapping())
    if bridge("read_ref", {"repository": "fixture/runtime-repo",
                            "branch": "homologation/runtime-fixture"}).get("head_sha") != "commit-0":
        errors.append("branch with slash could not be read through the GitHub MCP bridge")
    bridge_persistence = GitHubMcpRecordPersistence(
        bridge, repository="fixture/runtime-repo", branch="runtime-fixture",
        capabilities={"read_ref", "read_file", "commit_file_cas"}, synthetic=True, **FIXTURE_SOURCE,
    )
    bridge_request = request(base_record("bridge-001"), key="bridge-create-001")
    bridge_request.pop("actor", None)
    bridge_policy = {**runtime_policy, "record_paths": {"bridge-001": "records/bridge-001.md"}}
    try:
        # Match the host connector's nested structuredContent envelopes and
        # pin file reads to the commit SHA even if the branch moves mid-read.
        tools.drift_on_next_ref = True
        pinned = bridge("read_file", {"repository": "fixture/runtime-repo", "branch": "runtime-fixture",
                                      "path": "records/pinned.md"})
        if (pinned.get("head_sha") != "commit-0"
                or base64.b64decode(pinned.get("content_base64", "")) != b"old snapshot"
                or tools.heads["runtime-fixture"] != "commit-drift"):
            errors.append("branch drift caused a file read to escape its pinned commit snapshot")
        missing = bridge("read_file", {"repository": "fixture/runtime-repo", "branch": "runtime-fixture",
                                       "path": "records/missing.md"})
        if missing.get("content_base64") is not None:
            errors.append("typed GitHub MCP 404 was not treated as an absent file")
        tools.heads["runtime-fixture"] = "commit-0"
        bridged = dispatch(Path("."), bridge_request, bridge_policy, remote_persistence=bridge_persistence)
        if (bridged.get("remote_receipt", {}).get("readback_confirmed") is not True
                or "records/bridge-001.md" not in tools.snapshots[tools.heads["runtime-fixture"]]
                or not any(path.startswith("meta/operation-receipts/record-mutations/")
                           for path in tools.snapshots[tools.heads["runtime-fixture"]])
                or "README.md" not in tools.snapshots[tools.heads["runtime-fixture"]]):
            errors.append("injected Git Data tools did not complete CAS/readback or preserve sibling tree entries")
        required_order = ["create_blob", "create_tree", "create_commit", "update_ref"]
        positions = [tools.call_order.index(name) for name in required_order]
        if positions != sorted(positions) or tools.call_order.count("update_ref") != 1:
            errors.append("GitHub MCP bridge used an unexpected or incomplete Git Data operation sequence")
        original_head = tools.heads["runtime-fixture"]
        try:
            bridge("commit_file_cas", {"repository": "fixture/runtime-repo", "branch": "runtime-fixture",
                   "path": "records/other.md", "expected_head_sha": "stale-head", "expected_file_sha256": None,
                   "content_base64": base64.b64encode(b"blocked").decode(), "idempotency_key": "stale-head"})
            errors.append("bridge accepted a mismatched expected head")
        except ContractError:
            pass
        if tools.heads["runtime-fixture"] != original_head:
            errors.append("CAS conflict changed the branch ref")
    except Exception as exc:
        errors.append(f"injected GitHub tool bridge failed: {type(exc).__name__}: {exc}")
    if errors:
        print(f"validate_v3_github_mcp_persistence: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_v3_github_mcp_persistence: OK - runtime-to-RecordCrud synthetic CAS/readback/receipt, version conflict, and fail-closed capability")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
