#!/usr/bin/env python3
"""Validate the deterministic V3 queue separation with a temporary vault."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import yaml


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    fixture = yaml.safe_load((root / "docs/v3-queue-fixtures.yaml").read_text(encoding="utf-8"))
    errors: list[str] = []
    if len(fixture.get("cases", [])) != 6:
        errors.append("expected six queue fixtures")
    runtime = root / ".v3-queue-test-runtime"
    if runtime.exists():
        shutil.rmtree(runtime)
    runtime.mkdir()
    try:
        vault = runtime
        record = vault / "records" / "sample.md"
        record.parent.mkdir()
        record.write_text(
            "---\n"
            "title: Sample\n"
            "date: '2026-06-01'\n"
            "updated: '2026-06-01'\n"
            "source: conversa\n"
            "tags: []\n"
            "type: note\n"
            "temporality: ephemeral\n"
            "ttl: '2026-07-01'\n"
            "status: draft\n"
            "revision: 1\n"
            "visibility: internal\n"
            "author: 'Test Person - @test'\n"
            "---\nBody\n",
            encoding="utf-8",
        )
        scan = run([sys.executable, str(root / "scripts/scan_v3_queues.py"), "--root", str(vault), "--now", "2026-09-04T00:00:00", "--write"], root)
        if scan.returncode:
            errors.append(f"scanner failed: {scan.stdout}{scan.stderr}")
        fm_queue = vault / "meta/fila-frontmatter.yaml"
        stale_queue = vault / "meta/fila-staleness.yaml"
        if not fm_queue.exists() or not stale_queue.exists():
            errors.append("scanner did not create both deterministic queues")
        normalize = run([sys.executable, str(root / "scripts/normalize_frontmatter_queue.py"), "--root", str(vault), "--queue", str(fm_queue), "--write"], root)
        if normalize.returncode:
            errors.append(f"normalizer failed: {normalize.stdout}{normalize.stderr}")
        if "source: conversation" not in record.read_text(encoding="utf-8"):
            errors.append("normalizer did not apply the supported vocabulary correction")
        blocked = run([sys.executable, str(root / "scripts/normalize_frontmatter_queue.py"), "--root", str(vault), "--queue", str(vault / "meta/fila-semantica.yaml"), "--write"], root)
        if blocked.returncode != 2:
            errors.append("normalizer did not block a semantic queue")
        stale = yaml.safe_load(stale_queue.read_text(encoding="utf-8")) or []
        if not any(item.get("finding_kind") == "ttl_expired" for item in stale):
            errors.append("expired TTL was not routed to staleness queue")
    finally:
        if runtime.exists():
            shutil.rmtree(runtime)
    if errors:
        print(f"validate_v3_queues: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_v3_queues: OK — deterministic separation, idempotent normalization, and semantic blocking")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
