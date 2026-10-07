#!/usr/bin/env python3
"""Atomic Markdown persistence used only through the canonical V3 CRUD gateway."""
from __future__ import annotations

import hashlib
import base64
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import uuid

import yaml

from v3_crud_engine import ContractError, VISIBILITY_RANK, _parse_document_for_crud, validate_record_structure


def serialize_record(record: dict) -> bytes:
    """Encode the governed envelope as YAML and keep prose in the Markdown body."""
    frontmatter = dict(record)
    content = frontmatter.pop("content", None)
    if not isinstance(content, str):
        raise ContractError("Record content must be prose before persistence")
    encoded = yaml.safe_dump(frontmatter, sort_keys=True, allow_unicode=True).encode("utf-8")
    return b"---\n" + encoded + b"---\n" + content.encode("utf-8")


def parse_record(document: bytes) -> dict:
    """Decode one canonical V3 Markdown Record without changing its body."""
    if not document.startswith(b"---\n"):
        raise ContractError("Record document is missing YAML frontmatter")
    end = document.find(b"\n---\n", 4)
    if end < 0:
        raise ContractError("Record document has an unterminated YAML header")
    try:
        record = yaml.safe_load(document[4:end])
        content = document[end + 5:].decode("utf-8")
    except (yaml.YAMLError, UnicodeDecodeError) as exc:
        raise ContractError("Record document cannot be decoded") from exc
    if not isinstance(record, dict):
        raise ContractError("Record frontmatter must be a mapping")
    record["content"] = content
    return record


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class MarkdownRecordStore:
    """Repository-contained atomic writer invoked by RecordCrud after validation."""

    def __init__(self, repository_root: Path):
        self.root = repository_root.resolve(strict=True)

    def load_all(self, active_collections: dict[str, dict]) -> dict[str, dict]:
        """Load and validate persisted V3 Records; leave legacy documents unmigrated."""
        records: dict[str, dict] = {}
        skipped = {".git", ".tmp", ".backup", "node_modules"}
        for path in sorted(self.root.rglob("*.md")):
            relative = path.relative_to(self.root)
            if any(part in skipped or part.startswith(".") for part in relative.parts):
                continue
            document = path.read_bytes()
            try:
                if not document.startswith(b"---\n"):
                    continue
                end = document.find(b"\n---\n", 4)
                if end < 0:
                    header = document[4:].splitlines()
                else:
                    header = document[4:end].splitlines()
                parsed_header = yaml.safe_load(b"\n".join(header).decode("utf-8"))
            except (yaml.YAMLError, UnicodeDecodeError):
                if b"record_id:" in document[:4096] or b"record_version:" in document[:4096]:
                    raise ContractError("V3 Record frontmatter is malformed")
                continue
            if not isinstance(parsed_header, dict) or not {"record_id", "record_version"}.issubset(parsed_header):
                continue
            record = parse_record(document)
            validated = validate_record_structure(record, active_collections)
            if validated["physical_path"] != relative.as_posix():
                raise ContractError("persisted Record path does not match its physical_path")
            record_id = validated["record_id"]
            if record_id in records:
                raise ContractError("duplicate persisted V3 Record identity")
            records[record_id] = validated
        return records

    def _path(self, relative_path: str) -> Path:
        candidate = Path(relative_path)
        if candidate.is_absolute() or ".." in candidate.parts or any(
            part in {".git", ".backup"} for part in candidate.parts):
            raise ContractError("Record path must stay repository-relative")
        target = (self.root / candidate).resolve(strict=False)
        if not target.is_relative_to(self.root):
            raise ContractError("Record path escapes the repository")
        if target.suffix.lower() != ".md":
            raise ContractError("Record persistence target must be Markdown")
        return target

    def _replace(self, target: Path, expected_sha256: str | None, output: bytes) -> None:
        if not target.parent.is_dir():
            raise ContractError("Record destination directory does not exist")
        lock_path = target.with_name(f".{target.name}.crud.lock")
        try:
            lock_fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError as exc:
            raise ContractError("Record write lock exists; inspect before recovery") from exc
        temporary_path: Path | None = None
        try:
            os.write(lock_fd, f"pid={os.getpid()}\n".encode("ascii"))
            os.fsync(lock_fd)
            os.close(lock_fd)
            if expected_sha256 is None:
                if target.exists():
                    raise ContractError("Record destination already exists")
            elif not target.is_file() or sha256_bytes(target.read_bytes()) != expected_sha256:
                raise ContractError("Record source changed since migration or read")
            with tempfile.NamedTemporaryFile(
                mode="wb", prefix=f".{target.name}.", suffix=".tmp",
                dir=target.parent, delete=False,
            ) as temporary:
                temporary.write(output)
                temporary.flush()
                os.fsync(temporary.fileno())
                temporary_path = Path(temporary.name)
            if expected_sha256 is not None:
                if not target.is_file() or sha256_bytes(target.read_bytes()) != expected_sha256:
                    raise ContractError("Record source changed during persistence")
            os.replace(temporary_path, target)
            temporary_path = None
        finally:
            try:
                os.close(lock_fd)
            except OSError:
                pass
            if temporary_path is not None:
                try:
                    temporary_path.unlink()
                except FileNotFoundError:
                    pass
            try:
                lock_path.unlink()
            except FileNotFoundError:
                pass

    def create(self, record: dict) -> None:
        target = self._path(record["physical_path"])
        self._replace(target, None, serialize_record(record))

    def update(self, previous: dict, record: dict) -> None:
        old_path = self._path(previous["physical_path"])
        new_path = self._path(record["physical_path"])
        if old_path != new_path:
            raise ContractError("Record move requires its separately governed CRUD operation")
        expected = sha256_bytes(serialize_record(previous))
        self._replace(new_path, expected, serialize_record(record))

    def migrate(self, record: dict, source_path: str, expected_source_sha256: str) -> str:
        target = self._path(record["physical_path"])
        if self._path(source_path) != target:
            raise ContractError("initial migration must preserve the physical path")
        output = serialize_record(record)
        if target.is_file() and target.read_bytes() == output:
            raise ContractError("Record migration was already applied; recovery review is required")
        self._replace(target, expected_source_sha256, output)
        return "written"

    def validate_legacy_binding(self, record: dict, source_path: str,
                               expected_sha256: str, context_files: dict) -> None:
        if ".tmp" in Path(source_path).parts:
            raise ContractError("direct legacy source cannot be a temporary working artifact")
        target = self._path(source_path)
        raw = target.read_bytes()
        if sha256_bytes(raw) != expected_sha256:
            raise ContractError("legacy source fingerprint changed")
        if not raw.startswith((b"---\n", b"---\r\n")):
            raise ContractError("direct legacy route requires parseable YAML frontmatter")
        fields, body, _ = self.read_legacy_document(source_path)
        if not isinstance(fields, dict) or not fields or {"record_id", "record_version"}.intersection(fields):
            raise ContractError("direct legacy route requires an unmigrated parsed source")
        if (record.get("content") != body or record.get("legacy_frontmatter") != fields
            or record.get("legacy_source_sha256") != expected_sha256):
            raise ContractError("direct legacy mapping must preserve body and every legacy field")
        if fields.get("visibility") not in VISIBILITY_RANK or (
            VISIBILITY_RANK[record["visibility"]] < VISIBILITY_RANK[fields["visibility"]]):
            raise ContractError("direct legacy route cannot infer or weaken source visibility")
        for relative, expected in context_files.items():
            candidate = Path(relative)
            if candidate.is_absolute() or ".." in candidate.parts or ".git" in candidate.parts:
                raise ContractError("legacy context path must remain in vault working files")
            path = (self.root / candidate).resolve()
            if relative == "profile.md" and expected == "absent":
                if path.exists():
                    raise ContractError("previously absent profile now requires context reconciliation")
                continue
            if not path.is_relative_to(self.root) or not path.is_file() or sha256_bytes(path.read_bytes()) != expected:
                raise ContractError("legacy context fingerprint changed")

    def _recovery_git_context(self) -> tuple[Path, str, str]:
        def query(*args):
            try:
                return subprocess.run(["git", "-C", str(self.root), *args],
                    capture_output=True, check=True, timeout=30).stdout.decode().strip()
            except (OSError, subprocess.SubprocessError) as exc:
                raise ContractError("recovery Git context unavailable") from exc
        if Path(query("rev-parse", "--show-toplevel")).resolve() != self.root:
            raise ContractError("recovery requires the exact vault repository root")
        branch = query("branch", "--show-current")
        if not branch.startswith("migration/"):
            raise ContractError("recovery requires its dedicated migration branch")
        git_dir = Path(query("rev-parse", "--absolute-git-dir")).resolve()
        return git_dir, branch, query("rev-parse", "HEAD")

    def prepare_migration_recovery(self, record: dict, source_path: str,
                                   expected_sha256: str) -> dict:
        """Immutable preimage in own Git administration, before CRUD persistence."""
        raw = self._path(source_path).read_bytes()
        if sha256_bytes(raw) != expected_sha256 or record.get("record_version") != 1:
            raise ContractError("recovery preimage or initial Record version changed")
        git_dir, branch, head = self._recovery_git_context()
        folder = (git_dir / "canonical-migration-recovery").resolve()
        if not folder.is_relative_to(git_dir):
            raise ContractError("recovery archive escapes own Git administration")
        folder.mkdir(exist_ok=True)
        for previous in folder.glob("*.json"):
            try:
                attempt = json.loads(previous.read_bytes())
            except (ValueError, UnicodeDecodeError) as exc:
                raise ContractError("prior recovery ticket requires reconciliation") from exc
            if not isinstance(attempt, dict):
                raise ContractError("prior recovery ticket requires reconciliation")
            if (attempt.get("source_path") == source_path
                and attempt.get("source_sha256") == expected_sha256
                and attempt.get("record_id") == record["record_id"]):
                raise ContractError("prior migration attempt requires separately governed reexecution")
        ticket_id = uuid.uuid4().hex
        ticket = {"schema": "canonical-migration-recovery/v1", "ticket_id": ticket_id,
            "source_path": source_path, "source_sha256": expected_sha256,
            "source_bytes_b64": base64.b64encode(raw).decode("ascii"),
            "migrated_sha256": sha256_bytes(serialize_record(record)),
            "record_id": record["record_id"], "record_version": 1,
            "vault_id": record["vault"]["vault_id"], "entity": record["entity"],
            "branch": branch, "originating_commit": head}
        encoded = json.dumps(ticket, sort_keys=True, ensure_ascii=False).encode("utf-8")
        path = folder / (ticket_id + ".json")
        with path.open("xb") as output:
            output.write(encoded)
            output.flush()
            os.fsync(output.fileno())
        if path.read_bytes() != encoded:
            raise ContractError("immutable recovery ticket verification failed")
        return {"ticket_id": ticket_id, "ticket_sha256": sha256_bytes(encoded),
            "source_sha256": expected_sha256, "migrated_sha256": ticket["migrated_sha256"]}

    def load_recovery_ticket(self, ticket_id: str, expected_ticket_sha256: str) -> dict:
        if not re.fullmatch(r"[0-9a-f]{32}", str(ticket_id)) or not re.fullmatch(r"[0-9a-f]{64}", str(expected_ticket_sha256)):
            raise ContractError("recovery requires exact ticket identity and SHA-256")
        git_dir, branch, _ = self._recovery_git_context()
        path = (git_dir / "canonical-migration-recovery" / (ticket_id + ".json")).resolve()
        if not path.is_relative_to(git_dir):
            raise ContractError("recovery ticket path escapes own Git administration")
        raw = path.read_bytes()
        if sha256_bytes(raw) != expected_ticket_sha256:
            raise ContractError("recovery ticket fingerprint changed")
        try:
            ticket = json.loads(raw)
        except (ValueError, UnicodeDecodeError) as exc:
            raise ContractError("recovery ticket cannot be decoded") from exc
        required = {"schema", "ticket_id", "source_path", "source_sha256", "source_bytes_b64",
            "migrated_sha256", "record_id", "record_version", "vault_id", "entity", "branch", "originating_commit"}
        if (not isinstance(ticket, dict) or required - ticket.keys()
            or ticket["schema"] != "canonical-migration-recovery/v1"
            or ticket["ticket_id"] != ticket_id or ticket["record_version"] != 1
            or ticket["branch"] != branch):
            raise ContractError("recovery ticket scope or schema mismatch")
        try:
            preimage = base64.b64decode(ticket["source_bytes_b64"], validate=True)
            fields, _ = _parse_document_for_crud(preimage.decode("utf-8"))
        except (ValueError, UnicodeDecodeError, yaml.YAMLError) as exc:
            raise ContractError("recovery preimage cannot be decoded") from exc
        if (sha256_bytes(preimage) != ticket["source_sha256"] or not isinstance(fields, dict)
            or not fields or {"record_id", "record_version"}.intersection(fields)
            or not re.fullmatch(r"[0-9a-f]{64}", str(ticket["migrated_sha256"]))):
            raise ContractError("recovery preimage integrity or legacy identity mismatch")
        try:
            ancestor = subprocess.run(["git", "-C", str(self.root), "merge-base", "--is-ancestor",
                ticket["originating_commit"], "HEAD"], capture_output=True, timeout=30).returncode
        except (OSError, subprocess.SubprocessError) as exc:
            raise ContractError("recovery lineage unavailable") from exc
        if ancestor != 0:
            raise ContractError("recovery branch no longer includes ticket origin")
        self._path(ticket["source_path"])
        return ticket

    def recover_migration(self, ticket: dict) -> str:
        """Called only after RecordCrud has validated exact-ticket approval."""
        target = self._path(ticket["source_path"])
        current = target.read_bytes()
        if sha256_bytes(current) == ticket["source_sha256"]:
            return "source_present_no_write"
        if sha256_bytes(current) != ticket["migrated_sha256"]:
            raise ContractError("recovery target changed; reconcile without overwrite")
        record = parse_record(current)
        if (record.get("record_id") != ticket["record_id"] or record.get("record_version") != 1
            or record.get("entity") != ticket["entity"] or record.get("vault", {}).get("vault_id") != ticket["vault_id"]):
            raise ContractError("recovery target identity changed")
        original = base64.b64decode(ticket["source_bytes_b64"], validate=True)
        self._replace(target, ticket["migrated_sha256"], original)
        if target.read_bytes() != original:
            raise ContractError("canonical recovery must be reconciled after persistence")
        return "restored"

    def read_legacy_document(self, relative_path: str) -> tuple[dict, str, str]:
        target = self._path(relative_path)
        if not target.is_file():
            raise ContractError("legacy Record document does not exist")
        raw = target.read_bytes()
        try:
            frontmatter, body = _parse_document_for_crud(raw.decode("utf-8"))
        except (UnicodeDecodeError, yaml.YAMLError) as exc:
            raise ContractError("legacy Record document cannot be decoded") from exc
        return frontmatter, body, sha256_bytes(raw)

    def normalize_legacy_document(
        self, relative_path: str, frontmatter: dict, body: str, expected_source_sha256: str
    ) -> None:
        target = self._path(relative_path)
        serialized = (
            "---\n"
            + yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True).rstrip()
            + "\n---"
            + body
        ).encode("utf-8")
        self._replace(target, expected_source_sha256, serialized)
