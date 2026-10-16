#!/usr/bin/env python3
"""Content inventory and isolated installation of the canonical local runtime."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import urllib.request
import zipfile

import yaml

from v3_channel import ChannelError, resolve_channel

REPOSITORY = "https://github.com/mklagenberg/hipocampo"
API = "https://api.github.com/repos/mklagenberg/hipocampo"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(data: object) -> bytes:
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def payload_files(root: Path) -> list[str]:
    """Operational files only; review receipts and generated inventories are excluded."""
    names = {"SPEC.md", "README.md", "CHANGELOG.md", "COMPATIBILITY.yaml", "GETTING-STARTED.md",
             "UPGRADE.md", "MIGRATIONS.md", "RELEASE-CHECKLIST.md", "requirements-dev.txt",
             "requirements-runtime.txt", "LICENSE", "NOTICE"}
    names.update(p.name for pattern in ("*.md", "*.yaml") for p in root.glob(pattern) if p.is_file())
    for dirname in ("skill", "scripts", "scaffold", "decisions", "changes", "conformance", "candidates", "audits", ".github"):
        for p in (root / dirname).rglob("*"):
            if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc":
                names.add(p.relative_to(root).as_posix())
    for p in (root / "docs").rglob("*"):
        relative = p.relative_to(root).as_posix()
        if p.is_file():
            names.add(relative)
    return sorted(names)


def make_inventory(root: Path) -> dict:
    entries = []
    for relative in payload_files(root):
        path = contained(root, relative)
        entries.append({"path": relative, "sha256": digest(path.read_bytes())})
    return {"schema_version": 1, "files": entries, "payload_sha256": digest(canonical_json(entries))}


def contained(root: Path, relative: str) -> Path:
    if (not isinstance(relative, str) or not relative or "\\" in relative or ":" in relative
            or any(ord(char) < 32 for char in relative)
            or relative.startswith("/") or any(part in {"", ".", ".."} for part in relative.split("/"))):
        raise ChannelError("non-canonical payload path")
    candidate = root / relative
    if candidate.is_symlink() or root.resolve() not in candidate.resolve().parents:
        raise ChannelError("payload path escapes its root or uses a symlink")
    for parent in candidate.parents:
        if parent == root:
            break
        if parent.is_symlink():
            raise ChannelError("payload parent uses a symlink")
    return candidate


def verify_inventory(root: Path, inventory: dict, expected: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{64}", expected or ""):
        raise ChannelError("expected payload digest is required")
    if not isinstance(inventory, dict) or inventory.get("schema_version") != 1:
        raise ChannelError("unsupported distribution inventory")
    entries = inventory.get("files")
    if not isinstance(entries, list) or not entries or digest(canonical_json(entries)) != expected or inventory.get("payload_sha256") != expected:
        raise ChannelError("payload inventory digest mismatch")
    seen = set()
    for entry in entries:
        relative = entry["path"]
        if relative in seen:
            raise ChannelError("duplicate inventory path")
        seen.add(relative)
        if digest(contained(root, relative).read_bytes()) != entry.get("sha256"):
            raise ChannelError("distribution file hash mismatch: " + relative)
    if seen != set(payload_files(root)):
        raise ChannelError("distribution file set differs from inventory")


def source_identity(root: Path, expected: str, *, allow_dirty: bool = False) -> None:
    if not (root / ".git").exists() and (root / "distribution.json").is_file():
        envelope = json.loads((root / "distribution.json").read_text(encoding="utf-8"))
        if envelope.get("source_commit") != expected or envelope.get("source_repository") != REPOSITORY:
            raise ChannelError("source archive identity does not match the chosen official snapshot")
        return
    def git(*args):
        return subprocess.check_output(["git", "-C", str(root), *args], text=True, stderr=subprocess.DEVNULL).strip()
    if git("rev-parse", "HEAD") != expected:
        raise ChannelError("source commit does not match the explicitly selected snapshot")
    origin = git("remote", "get-url", "origin").removesuffix(".git").rstrip("/")
    if origin not in {REPOSITORY, "git@github.com:mklagenberg/hipocampo"}:
        raise ChannelError("source origin is not the canonical methodology repository")
    if not allow_dirty and git("status", "--porcelain", "--untracked-files=normal"):
        raise ChannelError("installation requires a clean pinned source checkout")
    # Git can call a CRLF working copy clean while its committed blob is LF.
    # A commit alone therefore does not identify the actual distributed bytes.
    files = payload_files(root)
    queries = b"".join((expected + ":" + relative + "\n").encode("utf-8") for relative in files)
    blobs = subprocess.run(["git", "-C", str(root), "cat-file", "--batch"], input=queries,
                           capture_output=True, check=True).stdout
    offset = 0
    for relative in files:
        end = blobs.find(b"\n", offset)
        header = blobs[offset:end].split()
        if len(header) != 3 or header[1] != b"blob":
            raise ChannelError("payload is not completely represented by the pinned commit")
        size = int(header[2])
        committed = blobs[end + 1:end + 1 + size]
        offset = end + size + 2
        if contained(root, relative).read_bytes() != committed:
            raise ChannelError("checkout bytes differ from pinned Git blob; honor .gitattributes: " + relative)


def read_api(path: str) -> dict:
    request = urllib.request.Request(API + path, headers={"Accept": "application/vnd.github+json", "User-Agent": "hipocampo-installer"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def published_release(version: str) -> dict:
    from urllib.parse import quote
    ref = "v" + version
    release = read_api("/releases/tags/" + quote(ref, safe=""))
    obj = read_api("/git/ref/tags/" + quote(ref, safe=""))["object"]
    for _ in range(8):
        if obj.get("type") == "commit":
            release["resolved_commit"] = obj["sha"]
            return release
        if obj.get("type") != "tag":
            break
        obj = read_api("/git/tags/" + obj["sha"])["object"]
    raise ChannelError("release tag does not resolve to a commit")


def install(source: Path, prefix: Path, *, channel: str, source_commit: str,
            expected_payload: str) -> dict:
    source = source.resolve(strict=True)
    prefix = prefix.resolve()
    if prefix.exists():
        raise ChannelError("installation destination already exists; preserve it and choose a new version directory")
    if source == prefix or source in prefix.parents:
        raise ChannelError("installation must be outside the source checkout")
    source_identity(source, source_commit)
    inventory = make_inventory(source)
    verify_inventory(source, inventory, expected_payload)
    contract = yaml.safe_load((source / "COMPATIBILITY.yaml").read_text(encoding="utf-8"))
    methodology = contract["methodology"]["version"]
    release = published_release(methodology) if channel == "stable" else None
    diagnostics = resolve_channel(channel, methodology, contract["methodology"]["supported_vault_range"], source_commit=source_commit, release=release)
    # A failed copy remains an identifiable incomplete directory; no recursive cleanup.
    prefix.mkdir(parents=True)
    for entry in inventory["files"]:
        target = prefix / entry["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / entry["path"], target)
    verify_inventory(prefix, inventory, expected_payload)
    source_identity(source, source_commit)
    verify_inventory(source, inventory, expected_payload)
    host_workspaces = {}
    for host, skill_directory in (("claude-code", ".claude/skills"), ("github-copilot", ".github/skills")):
        workspace = prefix / "host-workspaces" / host
        skill_target = workspace / skill_directory / "hipocampo"
        shutil.copytree(prefix / "skill", skill_target)
        command = [sys.executable, str(prefix / "scripts/v3_runtime.py"), "--channel", channel,
                   "--expected-payload", expected_payload]
        (workspace / "AGENTS.md").write_text(
            "# Isolated Hipocampo host workspace\n\n"
            "Read the installed Hipocampo skill. This is client-local generated configuration, not a vault.\n"
            "Runtime argument vector (append authorized --instance and --request):\n\n```json\n"
            + json.dumps(command) + "\n```\n\n"
            "Candidate warnings do not stop valid canonical operations. Do not create a real-instance policy,\n"
            "grant access or read private content without its own authorization. Confirm actual skill loading;\n"
            "workspace generation is not host verification.\n", encoding="utf-8")
        if host == "claude-code":
            (workspace / "CLAUDE.md").write_text("# Hipocampo test workspace\n\n@AGENTS.md\n", encoding="utf-8")
        host_workspaces[host] = str(workspace)
    metadata = {"schema_version": 1, "source_repository": REPOSITORY,
                "source_commit": source_commit, "channel": channel, "release": release,
                "inventory": inventory, "payload_sha256": expected_payload}
    # Written last: a partial installation cannot look activated.
    (prefix / "installation.json").write_bytes(canonical_json(metadata))
    return {"status": "installed", "installation": str(prefix), "diagnostics": diagnostics,
            "runtime": str(prefix / "scripts/v3_runtime.py"), "payload_sha256": expected_payload,
            "host_workspaces": host_workspaces}


def archive(source: Path, target: Path, *, source_commit: str, expected_payload: str) -> dict:
    """Assemble before publication; no lookup of the future final tag is needed."""
    source = source.resolve(strict=True)
    source_identity(source, source_commit)
    inventory = make_inventory(source)
    verify_inventory(source, inventory, expected_payload)
    if target.exists():
        raise ChannelError("archive destination already exists; do not replace a frozen artifact")
    envelope = {"source_repository": REPOSITORY, "source_commit": source_commit,
                "inventory": inventory, "payload_sha256": expected_payload}
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "x", compression=zipfile.ZIP_DEFLATED) as output:
        for item in inventory["files"]:
            info = zipfile.ZipInfo(item["path"], date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            output.writestr(info, (source / item["path"]).read_bytes())
        info = zipfile.ZipInfo("distribution.json", date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.create_system = 3
        info.external_attr = 0o100644 << 16
        output.writestr(info, canonical_json(envelope))
    source_identity(source, source_commit)
    verify_inventory(source, inventory, expected_payload)
    return {"archive": str(target), "archive_sha256": digest(target.read_bytes()),
            "payload_sha256": expected_payload, "source_commit": source_commit}


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--inventory-only", action="store_true")
    parser.add_argument("--prefix", type=Path)
    parser.add_argument("--channel", choices=("stable", "experimental"), default="stable")
    parser.add_argument("--source-commit")
    parser.add_argument("--expected-payload")
    parser.add_argument("--archive", type=Path, help="create a deterministic source/runtime asset before publication")
    args = parser.parse_args()
    try:
        if args.inventory_only:
            result = make_inventory(args.source.resolve())
        elif args.archive:
            result = archive(args.source, args.archive, source_commit=args.source_commit, expected_payload=args.expected_payload)
        elif args.prefix is None:
            raise ChannelError("--prefix is required for installation")
        else:
            result = install(args.source, args.prefix, channel=args.channel,
                             source_commit=args.source_commit, expected_payload=args.expected_payload)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (ChannelError, OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "blocked", "error": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
