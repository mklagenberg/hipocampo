#!/usr/bin/env python3
"""Small, side-effect-free primitives for the unreleased V3 queue scripts."""
from __future__ import annotations

import hashlib
from datetime import date, datetime
from pathlib import Path

import yaml


REQUIRED_FRONTMATTER = {
    "title", "date", "updated", "source", "tags", "type", "temporality",
    "ttl", "status", "revision", "visibility", "author",
}
DEPRECATED_VALUES = {"conversa": "conversation", "interno": "internal"}
KNOWN_TYPES = {
    "note", "reference", "decision", "project", "person", "case", "framework", "company",
    "question", "hypothesis", "observation", "project-candidate", "decision-candidate",
}


def parse_document(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text
    frontmatter = yaml.safe_load(text[4:end]) or {}
    body = text[end + 4:]
    return frontmatter if isinstance(frontmatter, dict) else {}, body


def finding_id(target: str, kind: str, value: str = "") -> str:
    return hashlib.sha256(f"{target}|{kind}|{value}".encode()).hexdigest()[:16]


def base_finding(path: Path, kind: str, description: str, now: datetime, *, value: str = "") -> dict:
    return {
        "finding_id": finding_id(path.as_posix(), kind, value),
        "target_path": path.as_posix(),
        "target_id": "",
        "finding_kind": kind,
        "rule_revision": "v3.0.0-1",
        "detected_at": now.isoformat(timespec="seconds") + "Z",
        "description": description,
        "status": "open",
    }


def scan_document(path: Path, now: datetime, *, target_path: Path | None = None) -> tuple[list[dict], list[dict]]:
    frontmatter, _ = parse_document(path)
    finding_path = target_path or path
    frontmatter_findings: list[dict] = []
    staleness_findings: list[dict] = []
    for field in sorted(REQUIRED_FRONTMATTER - frontmatter.keys()):
        frontmatter_findings.append(base_finding(finding_path, "missing_required_field", f"missing field: {field}", now, value=field))
    source = frontmatter.get("source")
    if source in DEPRECATED_VALUES:
        frontmatter_findings.append(base_finding(finding_path, "deprecated_vocabulary", f"source uses deprecated value: {source}", now, value=source))
    doc_type = frontmatter.get("type")
    if isinstance(doc_type, str) and doc_type not in KNOWN_TYPES:
        frontmatter_findings.append(base_finding(finding_path, "unknown_type_preserved", f"unknown type preserved: {doc_type}", now, value=doc_type))
    ttl = frontmatter.get("ttl")
    if isinstance(ttl, str):
        try:
            expires = date.fromisoformat(ttl)
        except ValueError:
            expires = None
            frontmatter_findings.append(base_finding(finding_path, "invalid_ttl_format", "ttl must be a concrete ISO date", now, value=ttl))
        if expires and expires < now.date() and frontmatter.get("temporality") != "historical":
            staleness_findings.append(base_finding(finding_path, "ttl_expired", f"ttl expired on {expires.isoformat()}", now, value=ttl))
    return frontmatter_findings, staleness_findings


def write_queue(path: Path, findings: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(findings, sort_keys=False, allow_unicode=True), encoding="utf-8")
