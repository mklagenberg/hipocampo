#!/usr/bin/env python3
"""Scan a vault and produce the V3 deterministic queues.

The default is a read-only preview. Use --write explicitly for an instance
where the operator has authorized queue writes. No semantic finding is
invented by this scanner.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from v3_queue_engine import scan_document, write_queue


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="vault root")
    parser.add_argument("--queue-dir", default="meta")
    parser.add_argument("--now", help="UTC date/time, useful for reproducible tests")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    now = datetime.fromisoformat(args.now).replace(tzinfo=timezone.utc) if args.now else datetime.now(timezone.utc)
    frontmatter_findings: list[dict] = []
    staleness_findings: list[dict] = []
    for path in sorted(root.rglob("*.md")):
        if any(part in {".git", "meta"} for part in path.parts):
            continue
        fm, stale = scan_document(path, now, target_path=path.relative_to(root))
        frontmatter_findings.extend(fm)
        staleness_findings.extend(stale)
    queue_root = root / args.queue_dir
    targets = {
        "frontmatter": queue_root / "fila-frontmatter.yaml",
        "staleness": queue_root / "fila-staleness.yaml",
        "semantic": queue_root / "fila-semantica.yaml",
    }
    if args.write:
        write_queue(targets["frontmatter"], frontmatter_findings)
        write_queue(targets["staleness"], staleness_findings)
        if not targets["semantic"].exists():
            write_queue(targets["semantic"], [])
    mode = "written" if args.write else "preview"
    print(f"scan_v3_queues: OK — {mode}; frontmatter={len(frontmatter_findings)}, staleness={len(staleness_findings)}, semantic=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
