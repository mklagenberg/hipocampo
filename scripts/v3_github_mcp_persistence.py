#!/usr/bin/env python3
"""GitHub MCP persistence port for the canonical RecordCrud gateway.

The host supplies an MCP invoker and an explicit atomic expected-head commit
operation. Generic file tools are deliberately not treated as governed CRUD.
"""
from __future__ import annotations

import base64
from copy import deepcopy
import hashlib
import json
import re
from typing import Callable, Mapping
from urllib.parse import quote

import yaml

from v3_crud_engine import ContractError, validate_record_structure
from v3_record_store import parse_record, serialize_record, sha256_bytes


class GitHubMcpUnavailable(ContractError):
    pass


class GitHubMcpGitDataBridge:
    """Compose injected GitHub MCP callables into the persistence operations.

    The host maps its tools to the logical keys below. No MCP runtime import or
    provider-specific callable name is required by this module.
    """

    TOOL_KEYS = {"fetch_git_data", "fetch_file", "create_blob", "create_tree", "create_commit", "update_ref"}

    def __init__(self, tools: Mapping[str, Callable[..., object]]):
        missing = self.TOOL_KEYS - set(tools)
        if missing:
            raise GitHubMcpUnavailable(f"GitHub MCP tool callables are missing: {sorted(missing)}")
        self.tools = dict(tools)

    @staticmethod
    def _payload(result: object) -> dict:
        if isinstance(result, dict):
            if isinstance(result.get("structuredContent"), dict):
                payload = dict(result["structuredContent"])
                if result.get("isError"):
                    payload["_mcp_is_error"] = True
                return payload
            content = result.get("content")
            if isinstance(content, list):
                texts = [item.get("text") for item in content if isinstance(item, dict) and isinstance(item.get("text"), str)]
                if texts:
                    try:
                        decoded = json.loads("\n".join(texts))
                    except json.JSONDecodeError:
                        return {"content": "\n".join(texts)}
                    if isinstance(decoded, dict):
                        return decoded
            return result
        raise GitHubMcpUnavailable("GitHub MCP tool returned an unsupported response")

    def _tool(self, key: str, args: dict) -> dict:
        payload = self._payload(self.tools[key](**args))
        if key == "fetch_git_data" and isinstance(payload.get("content"), str):
            # github_fetch wraps the GitHub JSON body inside structuredContent.content.
            try:
                decoded = json.loads(payload["content"])
            except json.JSONDecodeError:
                decoded = None
            if isinstance(decoded, dict) and any(name in decoded for name in ("object", "tree")):
                payload = decoded
        if payload.get("_mcp_is_error"):
            error = payload.get("error_data")
            status = error.get("status") if isinstance(error, dict) else None
            code = payload.get("error_code")
            if key == "fetch_file" and (code == "NOT_FOUND" or status == "404" or status == 404):
                return {"status_code": 404, "exists": False}
            raise GitHubMcpUnavailable(f"GitHub MCP {key} tool returned an error")
        return payload

    @staticmethod
    def _repository(args: dict) -> str:
        repository = args.get("repository")
        if not isinstance(repository, str) or repository.count("/") != 1:
            raise ContractError("GitHub repository must be owner/name")
        owner, name = repository.split("/", 1)
        if (not owner or not name or any(not part or any(not (character.isalnum() or character in "._-")
                                                         for character in part) for part in (owner, name))):
            raise ContractError("GitHub repository must be owner/name")
        return repository

    def _ref(self, repository: str, branch: str) -> str:
        # GitHub MCP fetch validates the REST path and rejects an encoded
        # branch separator; encode each name component but retain `/`.
        encoded = quote(branch, safe="/")
        result = self._tool("fetch_git_data", {
            "url": f"https://api.github.com/repos/{repository}/git/ref/heads/{encoded}"
        })
        sha = result.get("object", {}).get("sha") if isinstance(result.get("object"), dict) else result.get("head_sha")
        if not isinstance(sha, str) or not sha:
            raise ContractError("GitHub MCP ref read omitted head SHA")
        return sha

    def _read_file(self, repository: str, pinned_ref: str, path: str) -> dict:
        result = self._tool("fetch_file", {
            "repository_full_name": repository, "path": path, "ref": pinned_ref, "encoding": "base64"
        })
        if result.get("status_code") == 404 or result.get("exists") is False:
            return {"exists": False}
        encoded = result.get("content_base64")
        if encoded is None and isinstance(result.get("content"), str):
            encoded = result["content"]
        if not isinstance(encoded, str):
            raise ContractError("GitHub MCP file read omitted base64 content")
        try:
            # GitHub Contents API line-wraps base64; retain strict validation
            # after removing only its transport line breaks.
            content = base64.b64decode(encoded.replace("\r", "").replace("\n", ""), validate=True)
        except (ValueError, TypeError) as exc:
            raise ContractError("GitHub MCP file content is invalid base64") from exc
        return {"exists": True, "content": content, "blob_sha": result.get("sha")}

    def __call__(self, operation: str, args: dict) -> dict:
        repository = self._repository(args)
        branch = args.get("branch")
        if not isinstance(branch, str) or not branch:
            raise ContractError("GitHub MCP branch is required")
        if operation == "read_ref":
            return {"head_sha": self._ref(repository, branch)}
        if operation == "read_file":
            expected_head = args.get("expected_head_sha")
            head = self._ref(repository, branch)
            if expected_head and head != expected_head:
                raise ContractError("remote branch changed before file read")
            file = self._read_file(repository, head, args["path"])
            if not file["exists"]:
                return {"head_sha": head, "content_base64": None}
            return {"head_sha": head, "content_base64": base64.b64encode(file["content"]).decode("ascii")}
        if operation != "commit_file_cas":
            raise GitHubMcpUnavailable(f"unsupported bridge operation: {operation}")
        path = args.get("path")
        if not isinstance(path, str) or not path or path.startswith("/") or ".." in path.split("/"):
            raise ContractError("CAS file path must be repository-relative")
        expected_head = args.get("expected_head_sha")
        current_head = self._ref(repository, branch)
        if not isinstance(expected_head, str) or current_head != expected_head:
            raise ContractError("expected-head CAS conflict before commit construction")
        current_file = self._read_file(repository, current_head, path)
        current_bytes = current_file["content"] if current_file["exists"] else None
        expected_file_sha = args.get("expected_file_sha256")
        actual_file_sha = hashlib.sha256(current_bytes).hexdigest() if current_bytes is not None else None
        if actual_file_sha != expected_file_sha:
            raise ContractError("expected-file CAS conflict before commit construction")
        extra_files = args.get("additional_files", [])
        if not isinstance(extra_files, list):
            raise ContractError("CAS additional_files must be a list")
        for item in extra_files:
            if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                raise ContractError("CAS additional file entry is malformed")
            extra_path = item["path"]
            if not extra_path or extra_path.startswith("/") or ".." in extra_path.split("/"):
                raise ContractError("CAS additional file path must be repository-relative")
            existing = self._read_file(repository, current_head, extra_path)
            existing_bytes = existing["content"] if existing["exists"] else None
            expected_extra_sha = item.get("expected_file_sha256")
            actual_extra_sha = hashlib.sha256(existing_bytes).hexdigest() if existing_bytes is not None else None
            if actual_extra_sha != expected_extra_sha:
                raise ContractError("expected-file CAS conflict for additional file")
        try:
            content = base64.b64decode(args["content_base64"], validate=True)
        except (ValueError, TypeError, KeyError) as exc:
            raise ContractError("CAS payload is invalid base64") from exc
        commit = self._tool("fetch_git_data", {
            "url": f"https://api.github.com/repos/{repository}/git/commits/{current_head}"
        })
        tree_sha = commit.get("tree", {}).get("sha") if isinstance(commit.get("tree"), dict) else None
        if not tree_sha:
            raise ContractError("GitHub MCP parent commit omitted tree SHA")
        tree_elements = []
        files = [(path, content)] + [
            (item["path"], base64.b64decode(item["content_base64"], validate=True)) for item in extra_files
        ]
        for file_path, file_content in files:
            blob = self._tool("create_blob", {"repository_full_name": repository,
                                               "content": base64.b64encode(file_content).decode("ascii"),
                                               "encoding": "base64"})
            blob_sha = blob.get("sha")
            if not blob_sha:
                raise ContractError("GitHub MCP blob creation omitted SHA")
            tree_elements.append({"path": file_path, "mode": "100644", "type": "blob", "sha": blob_sha})
        tree = self._tool("create_tree", {"repository_full_name": repository, "base_tree_sha": tree_sha,
                                           "tree_elements": tree_elements})
        new_tree_sha = tree.get("sha")
        if not new_tree_sha:
            raise ContractError("GitHub MCP tree creation omitted SHA")
        created = self._tool("create_commit", {"repository_full_name": repository,
                                                "message": "Governed Record CRUD mutation",
                                                "parent_sha": current_head, "tree_sha": new_tree_sha})
        commit_sha = created.get("sha")
        if not commit_sha:
            raise ContractError("GitHub MCP commit creation omitted SHA")
        moved = self._tool("update_ref", {"repository_full_name": repository, "branch_name": branch,
                                           "expected_sha": current_head, "force": False, "sha": commit_sha})
        moved_sha = moved.get("object", {}).get("sha") if isinstance(moved.get("object"), dict) else moved.get("head_sha", commit_sha)
        head_after = self._ref(repository, branch)
        if moved_sha != commit_sha or head_after != commit_sha:
            raise ContractError("GitHub MCP ref update was not confirmed at the requested commit")
        return {"status": "committed", "commit_sha": commit_sha, "head_sha": head_after}


class GitHubMcpRecordPersistence:
    """A minimal remote RecordPersistence implementation.

    `invoke` maps a named operation to the current host's GitHub MCP tool.
    The only write primitive accepted is `commit_file_cas`, which must be
    atomic with respect to `expected_head_sha` and idempotent by key.
    """

    REQUIRED_OPERATIONS = {"read_ref", "read_file", "commit_file_cas"}

    def __init__(self, invoke: Callable[[str, dict], dict], *, repository: str,
                 branch: str, capabilities: set[str], synthetic: bool = False,
                 methodology_version: str | None = None,
                 source_method_version: str | None = None,
                 source_commit: str | None = None):
        if not repository or not branch:
            raise ContractError("remote repository and branch are required")
        if not all(isinstance(value, str) and value.strip() for value in
                   (methodology_version, source_method_version, source_commit)):
            raise ContractError("remote CRUD requires explicit methodology, source method, and source commit pins")
        self.invoke = invoke
        self.repository = repository
        self.branch = branch
        self.capabilities = set(capabilities)
        self.synthetic = synthetic
        self.methodology_version = methodology_version
        self.source_method_version = source_method_version
        self.source_commit = source_commit
        self.last_receipt: dict | None = None
        self._active_context: dict = {}

    def _require(self, operation: str) -> None:
        if operation not in self.capabilities:
            raise GitHubMcpUnavailable(f"required GitHub MCP operation unavailable: {operation}")

    def _call(self, operation: str, payload: dict) -> dict:
        self._require(operation)
        result = self.invoke(operation, {"repository": self.repository, **payload})
        if not isinstance(result, dict):
            raise ContractError(f"GitHub MCP {operation} returned a non-object result")
        return result

    def _current(self, path: str) -> tuple[str, bytes | None]:
        ref = self._call("read_ref", {"branch": self.branch})
        head = ref.get("head_sha")
        if not isinstance(head, str) or not head:
            raise ContractError("GitHub MCP read_ref omitted head_sha")
        if not path:
            return head, None
        result = self._call("read_file", {"branch": self.branch, "path": path, "expected_head_sha": head})
        if result.get("head_sha") != head:
            raise ContractError("remote file read does not match the observed branch head")
        encoded = result.get("content_base64")
        if encoded is None:
            return head, None
        import base64
        try:
            return head, base64.b64decode(encoded, validate=True)
        except (ValueError, TypeError) as exc:
            raise ContractError("GitHub MCP returned invalid base64 file content") from exc

    def load_all(self, active_collections: dict[str, dict]) -> dict[str, dict]:
        self._require("list_record_paths")
        listing = self._call("list_record_paths", {"branch": self.branch})
        paths = listing.get("paths")
        if not isinstance(paths, list) or any(not isinstance(path, str) for path in paths):
            raise ContractError("GitHub MCP record listing is malformed")
        records: dict[str, dict] = {}
        for path in paths:
            head, content = self._current(path)
            if content is None:
                raise ContractError("listed Record disappeared during remote read")
            try:
                record = parse_record(content)
                validated = validate_record_structure(record, active_collections)
            except Exception as exc:
                raise ContractError(f"remote Record failed canonical validation: {path}") from exc
            if validated["physical_path"] != path or validated["record_id"] in records:
                raise ContractError("remote Record path or identity is inconsistent")
            records[validated["record_id"]] = validated
        return records

    def load_one(self, record_id: str, path: str, active_collections: dict[str, dict]) -> dict:
        """Load one policy-selected remote Record without scanning other bodies."""
        if not record_id or not path:
            raise ContractError("remote Record read requires an authorized identity and path")
        head, content = self._current(path)
        if content is None:
            raise ContractError("authorized remote Record was not found")
        try:
            record = parse_record(content)
            validated = validate_record_structure(record, active_collections)
        except Exception as exc:
            raise ContractError("remote Record failed canonical validation") from exc
        if validated["record_id"] != record_id or validated["physical_path"] != path:
            raise ContractError("remote Record identity/path differs from the authorized mapping")
        self.last_read = {"status": "confirmed", "repository": self.repository, "branch": self.branch,
                          "head_sha": head, "record_id": record_id, "path": path,
                          "record_sha256": sha256_bytes(content), "readback_confirmed": True}
        return validated

    @staticmethod
    def _receipt_path(key: str) -> str:
        key_hash = hashlib.sha256(key.encode("utf-8")).hexdigest()
        return f"meta/operation-receipts/record-mutations/sha256-{key_hash}.yaml"

    @staticmethod
    def _key_hash(key: str) -> str:
        return hashlib.sha256(key.encode("utf-8")).hexdigest()

    def set_idempotency_context(self, key: str, fingerprint: str, *, actor: str, reason: str,
                                expected_base_head: str | None = None) -> None:
        if not key or not re.fullmatch(r"[0-9a-f]{64}", fingerprint):
            raise ContractError("remote CRUD requires an idempotency key and canonical request fingerprint")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,63}", actor):
            raise ContractError("durable receipt requires a minimized stable actor account ID")
        if not isinstance(reason, str) or not reason.strip():
            raise ContractError("durable receipt requires a non-empty reason")
        self._active_context = {"key": key, "key_hash": self._key_hash(key), "request_fingerprint": fingerprint,
                               "actor": actor, "reason_sha256": hashlib.sha256(reason.encode("utf-8")).hexdigest(),
                               "expected_base_head": expected_base_head}
        self._active_idempotency_key = key

    def _decode_receipt(self, content: bytes | None) -> dict | None:
        if content is None:
            return None
        try:
            receipt = yaml.safe_load(content.decode("utf-8"))
        except (UnicodeError, yaml.YAMLError) as exc:
            raise ContractError("durable operation receipt is malformed") from exc
        if not isinstance(receipt, dict):
            raise ContractError("durable operation receipt must be an object")
        return receipt

    def _check_receipt_context(self, receipt: dict, *, record_id: str, path: str,
                               vault_id: str, key: str, fingerprint: str) -> None:
        expected = {"schema_version": "1.0", "key_hash": self._key_hash(key),
                    "request_fingerprint": fingerprint, "target_vault_id": vault_id,
                    "record_id": record_id, "physical_path": path,
                    "methodology_version": self.methodology_version,
                    "source_method_version": self.source_method_version,
                    "source_commit": self.source_commit}
        requested_base_head = self._active_context.get("expected_base_head")
        if requested_base_head and receipt.get("expected_base_head") != requested_base_head:
            raise ContractError("idempotency receipt conflicts with requested base head")
        mismatches = [field for field, value in expected.items() if receipt.get(field) != value]
        if mismatches:
            raise ContractError(f"idempotency key receipt conflicts with request context: {', '.join(mismatches)}")

    def replay(self, *, record_id: str, path: str, vault_id: str,
               active_collections: dict[str, dict]) -> dict | None:
        context = self._active_context
        key = context.get("key")
        if not key:
            raise ContractError("remote CRUD replay requires an active idempotency key")
        receipt_path = self._receipt_path(key)
        observed_head, raw_receipt = self._current(receipt_path)
        receipt = self._decode_receipt(raw_receipt)
        if receipt is None:
            return None
        self._check_receipt_context(receipt, record_id=record_id, path=path, vault_id=vault_id,
                                    key=key, fingerprint=context["request_fingerprint"])
        current = self.load_one(record_id, path, active_collections)
        if getattr(self, "last_read", {}).get("head_sha") != observed_head:
            raise ContractError("remote branch changed between receipt and Record readback")
        current_bytes = serialize_record(current)
        if (sha256_bytes(current_bytes) != receipt.get("resulting_record_hash") or
                current.get("record_version") != receipt.get("resulting_record_version")):
            raise ContractError("idempotency receipt exists but current Record has drifted; retry cannot claim success")
        transport_receipt = {"status": "confirmed", "repository": self.repository, "branch": self.branch,
                             "head_sha": observed_head, "path": path, "record_id": record_id,
                             "record_version": current["record_version"], "idempotency_key_hash": context["key_hash"],
                             "record_sha256": sha256_bytes(current_bytes), "readback_confirmed": True,
                             "replayed_from_durable_receipt": True}
        self.last_receipt = transport_receipt
        return {"record": current, "receipt": transport_receipt}

    def _commit(self, record: dict, *, prior: dict | None, key: str) -> None:
        if not key:
            raise ContractError("remote CRUD persistence requires an idempotency key")
        context = self._active_context
        if context.get("key") != key:
            raise ContractError("remote CRUD idempotency context changed before persistence")
        path = record["physical_path"]
        observed_head, old_bytes = self._current(path)
        requested_base_head = context.get("expected_base_head")
        if requested_base_head and requested_base_head != observed_head:
            raise ContractError("remote CRUD observed head differs from requested base head")
        expected_record_sha = sha256_bytes(serialize_record(prior)) if prior else None
        vault_id = record.get("vault", {}).get("vault_id", "")
        receipt_path = self._receipt_path(key)
        receipt_head, existing_receipt_bytes = self._current(receipt_path)
        existing_receipt = self._decode_receipt(existing_receipt_bytes)
        if existing_receipt is not None:
            self._check_receipt_context(existing_receipt, record_id=record["record_id"], path=path,
                                        vault_id=vault_id, key=key, fingerprint=context["request_fingerprint"])
            if (receipt_head != observed_head or old_bytes != serialize_record(record) or
                    existing_receipt.get("resulting_record_hash") != sha256_bytes(old_bytes or b"") or
                    existing_receipt.get("resulting_record_version") != record.get("record_version")):
                raise ContractError("matching idempotency receipt exists but remote Record has drifted")
            self.last_receipt = {"status": "confirmed", "repository": self.repository, "branch": self.branch,
                                 "head_sha": observed_head, "path": path, "record_id": record["record_id"],
                                 "record_version": record["record_version"],
                                 "idempotency_key_hash": context["key_hash"],
                                 "record_sha256": sha256_bytes(old_bytes), "readback_confirmed": True,
                                 "replayed_from_durable_receipt": True}
            return
        if receipt_head != observed_head:
            raise ContractError("remote branch changed while checking durable operation receipt")
        if prior is None and old_bytes is not None:
            raise ContractError("remote Record destination already exists")
        if prior is not None and (old_bytes is None or sha256_bytes(old_bytes) != expected_record_sha):
            raise ContractError("remote Record changed since canonical read; expected-head conflict")
        receipt = {
            "schema_version": "1.0", "key_hash": context["key_hash"],
            "request_fingerprint": context["request_fingerprint"], "target_vault_id": vault_id,
            "record_id": record["record_id"], "physical_path": path,
            "expected_base_head": observed_head, "resulting_record_hash": sha256_bytes(serialize_record(record)),
            "resulting_record_version": record["record_version"],
            "actor": context["actor"], "reason_sha256": context["reason_sha256"],
            "methodology_version": self.methodology_version,
            "source_method_version": self.source_method_version, "source_commit": self.source_commit,
        }
        payload = {
            "branch": self.branch,
            "path": path,
            "content_base64": __import__("base64").b64encode(serialize_record(record)).decode("ascii"),
            "expected_head_sha": observed_head,
            "expected_file_sha256": expected_record_sha,
            "additional_files": [{"path": receipt_path,
                                   "content_base64": __import__("base64").b64encode(
                                       yaml.safe_dump(receipt, sort_keys=True, allow_unicode=True).encode("utf-8")
                                   ).decode("ascii"), "expected_file_sha256": None}],
        }
        result = self._call("commit_file_cas", payload)
        commit_sha = result.get("commit_sha")
        new_head = result.get("head_sha")
        if not commit_sha or not new_head or result.get("status") not in {"committed", "already_committed"}:
            raise ContractError("CAS commit did not provide a confirmed commit and head")
        read_head, readback = self._current(path)
        if read_head != new_head or readback != serialize_record(record):
            raise ContractError("remote CRUD readback did not match committed Record")
        receipt_read_head, receipt_readback = self._current(receipt_path)
        expected_receipt_bytes = yaml.safe_dump(receipt, sort_keys=True, allow_unicode=True).encode("utf-8")
        if receipt_read_head != new_head or receipt_readback != expected_receipt_bytes:
            raise ContractError("remote CRUD readback did not match the durable operation receipt")
        self.last_receipt = {
            "status": "confirmed", "repository": self.repository, "branch": self.branch,
            "base_head_sha": observed_head, "commit_sha": commit_sha, "head_sha": new_head,
            "path": path, "record_id": record["record_id"], "record_version": record["record_version"],
            "idempotency_key_hash": context["key_hash"], "record_sha256": sha256_bytes(readback),
            "readback_confirmed": True,
        }

        self.last_receipt.update(methodology_version=self.methodology_version,
                                 source_method_version=self.source_method_version,
                                 source_commit=self.source_commit)

    def create(self, record: dict) -> None:
        key = getattr(self, "_active_idempotency_key", None)
        self._commit(record, prior=None, key=key or "")

    def update(self, previous: dict, record: dict) -> None:
        key = getattr(self, "_active_idempotency_key", None)
        self._commit(record, prior=previous, key=key or "")

    def set_idempotency_key(self, key: str) -> None:
        # Retained as a fail-closed compatibility hook; production composition
        # must provide the canonical request fingerprint via set_idempotency_context.
        if key:
            raise ContractError("remote CRUD requires the canonical idempotency context")

    def reconcile(self, record: dict, key: str) -> dict:
        raise ContractError("content equality cannot prove a durable idempotent receipt")

    def __getattr__(self, name: str):
        if name in {"migrate", "validate_legacy_binding", "prepare_migration_recovery",
                    "load_recovery_ticket", "recover_migration", "read_legacy_document",
                    "normalize_legacy_document"}:
            raise GitHubMcpUnavailable(f"remote persistence does not implement {name}")
        raise AttributeError(name)


class GitHubMcpCrudAdapter:
    """Run requests through RecordCrud and attach remote persistence evidence."""

    def __init__(self, crud, persistence: GitHubMcpRecordPersistence):
        self.crud = crud
        self.persistence = persistence

    def call(self, request: dict) -> dict:
        self.persistence.last_receipt = None
        operation = request.get("operation")
        if operation not in {"create", "update", "delete"}:
            raise ContractError("remote write adapter accepts canonical mutation verbs only")
        key = request.get("idempotency_key")
        if operation == "create":
            fingerprint_payload = {"operation": operation, "record": request.get("record", {}),
                                   "semantic_review": request.get("semantic_review"),
                                   "actor": request.get("actor", ""), "reason": request.get("reason", "")}
            proposed = request.get("record", {})
            record_id = proposed.get("record_id")
            path = proposed.get("physical_path")
        else:
            patch = request.get("patch", {}) if operation == "update" else {"status": "archived", "current_use": False}
            fingerprint_payload = {"operation": operation, "record_id": request.get("record_id"),
                                   "patch": patch, "expected_version": request.get("expected_version"),
                                   "semantic_review": request.get("semantic_review"),
                                   "actor": request.get("actor", ""), "reason": request.get("reason", "")}
            record_id = request.get("record_id")
            proposed = self.crud.records.get(record_id, {})
            path = proposed.get("physical_path")
        if not isinstance(key, str) or not key:
            raise ContractError("remote CRUD requires an idempotency key")
        fingerprint = self.crud._request_fingerprint(fingerprint_payload)
        self.persistence.set_idempotency_context(key, fingerprint,
                                                actor=str(request.get("actor", "")),
                                                reason=str(request.get("reason", "")),
                                                expected_base_head=request.get("expected_base_head"))
        vault_id = proposed.get("vault", {}).get("vault_id") if isinstance(proposed, dict) else None
        if not vault_id and operation == "create":
            vault = request.get("record", {}).get("vault", {})
            vault_id = vault.get("vault_id") if isinstance(vault, dict) else None
        if record_id and path and vault_id:
            replay = self.persistence.replay(record_id=record_id, path=path, vault_id=vault_id,
                                             active_collections=self.crud.active_collections)
            if replay is not None:
                self.crud._records[record_id] = deepcopy(replay["record"])
                return {"status": "accepted", "record": deepcopy(replay["record"]),
                        "remote_receipt": deepcopy(replay["receipt"]),
                        "evidence_level": "synthetic-adapter" if self.persistence.synthetic else "host-tool-result"}
        result = self.crud.apply(deepcopy(request))
        receipt = self.persistence.last_receipt
        if result.get("status") == "accepted" and not receipt:
            raise ContractError("canonical CRUD accepted a remote mutation without a durable receipt")
        result["remote_receipt"] = deepcopy(receipt)
        result["evidence_level"] = "synthetic-adapter" if getattr(self.persistence, "synthetic", False) else "host-tool-result"
        return result
