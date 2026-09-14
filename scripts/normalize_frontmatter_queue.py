#!/usr/bin/env python3
"""Apply only supported deterministic frontmatter corrections.

This script refuses semantic and staleness queues. It is intentionally opt-in:
without --write it reports what would change.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

import yaml

from v3_crud_engine import ContractError, persist_record_document
from v3_queue_engine import DEPRECATED_VALUES, parse_document


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--queue", required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    queue_path = Path(args.queue).resolve()
    if "fila-frontmatter" not in queue_path.name:
        print("normalize_frontmatter_queue: BLOCKED — only fila-frontmatter.yaml is supported")
        return 2
    root = Path(args.root).resolve()
    try:
        queue = yaml.safe_load(queue_path.read_text(encoding="utf-8")) or []
    except (OSError, yaml.YAMLError) as exc:
        print(f"normalize_frontmatter_queue: FAILED — {exc}")
        return 1
    if not isinstance(queue, list):
        print("normalize_frontmatter_queue: FAILED — queue must be a list")
        return 1
    changed = 0
    resolved = 0
    now = datetime.now(timezone.utc).isoformat(timespec="seconds") + "Z"
    for finding in queue:
        if not isinstance(finding, dict) or finding.get("status") != "open":
            continue
        if finding.get("finding_kind") != "deprecated_vocabulary":
            continue
        path = root / finding["target_path"]
        frontmatter, body = parse_document(path)
        old = frontmatter.get("source")
        new = DEPRECATED_VALUES.get(old)
        if not new:
            continue
        changed += 1
        if args.write:
            frontmatter["source"] = new
            frontmatter["revision"] = int(frontmatter.get("revision", 0)) + 1
            frontmatter["revision_note"] = "Deterministic V3 frontmatter vocabulary normalization"
            try:
                persist_record_document(
                    path,
                    frontmatter,
                    body,
                    expected_revision=int(frontmatter["revision"]) - 1,
                    actor="frontmatter-normalizer",
                    reason="deterministic vocabulary normalization",
                )
            except (ContractError, OSError, KeyError, TypeError) as exc:
                print(f"normalize_frontmatter_queue: FAILED — {path}: {exc}")
                return 1
            finding["status"] = "resolved"
            finding["resolved_at"] = now
            resolved += 1
    if args.write:
        queue_path.write_text(yaml.safe_dump(queue, sort_keys=False, allow_unicode=True), encoding="utf-8")
    mode = "written" if args.write else "preview"
    print(f"normalize_frontmatter_queue: OK — {mode}; candidates={changed}, resolved={resolved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
