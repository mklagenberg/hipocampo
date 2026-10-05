#!/usr/bin/env python3
"""Atomic Markdown persistence used only through the canonical V3 CRUD gateway."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import tempfile

import yaml

from v3_crud_engine import ContractError, _parse_document_for_crud, validate_record_structure


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
        if candidate.is_absolute() or ".." in candidate.parts:
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
