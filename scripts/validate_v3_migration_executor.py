#!/usr/bin/env python3
"""Exercise the canonical Markdown-backed migration path with synthetic Git repositories."""
from __future__ import annotations

import hashlib
from pathlib import Path
import shutil
import subprocess
import uuid
from types import SimpleNamespace

import yaml

from v3_crud_engine import ContractError, RecordCrud
from v3_migration_engine import inventory_fingerprint
from v3_migration_executor import run
from v3_record_store import MarkdownRecordStore, parse_record, serialize_record


ACTIVE_COLLECTIONS = {"collection-general": {"collection_id": "collection-general", "active": True}}


def record(record_id: str = "rec-migration-001") -> dict:
    return {
        "record_id": record_id,
        "record_version": 1,
        "entity": "entity-fixture",
        "scope": "scope-fixture",
        "source": {"source_id": "source-fixture", "source_kind": "conversation", "entity": "entity-fixture"},
        "vault": {"vault_id": "vault-fixture", "entity": "entity-fixture", "profile": "entity", "role": "anchor"},
        "governance": {"owner": "owner-fixture", "authority": "authority-fixture"},
        "content": "Sanitized fixture prose.\nSecond line.",
        "physical_path": f"records/{record_id}.md",
        "status": "active",
        "visibility": "internal",
        "staleness": "current",
        "collection_ids": ["collection-general"],
        "chunks": [{"chunk_id": "chunk-fixture", "parent_record_id": record_id, "text_ref": "body"}],
        "artifacts": [],
    }


def review(record_id: str = "rec-migration-001", *, decision: str = "accepted") -> dict:
    return {
        "review_id": "review-fixture",
        "target_id": record_id,
        "reviewer": "reviewer-fixture",
        "purpose": "synthetic migration executor validation",
        "evidence_refs": ["fixture/source-sha256"],
        "rationale": "Sanitized fixture mapping reviewed and explicitly accepted.",
        "reviewed_at": "2026-10-04T12:00:00Z",
        "decision": decision,
    }


def make_repo(parent: Path, name: str = "vault") -> tuple[Path, bytes]:
    repo = parent / name
    (repo / "records").mkdir(parents=True)
    source = b"---\nid: legacy-fixture\nrevision: 4\n---\nLegacy sanitized prose.\n"
    (repo / "records/rec-migration-001.md").write_bytes(source)
    return repo, source


def manifest(source: bytes, *, semantic_decision: str = "accepted") -> dict:
    target = record()
    return {
        "source_version": "2.2.0",
        "target_version": "3.0.0",
        "mapping": "complete",
        "privacy": "proven",
        "rollback": "tested",
        "target_contract": "verified",
        "human_approval": "present",
        "unsafe_raw_fallback": False,
        "semantic_review_status": "complete",
        "execution_state": "not_started",
        "vault_id": "vault-fixture",
        "approved_vault_id": "vault-fixture",
        "approval_scope": "v2.2-to-v3-branch-local",
        "approval_ref": "synthetic-fixture-approval",
        "source_inventory_sha256": inventory_fingerprint([{
            "source_path": target["physical_path"],
            "source_sha256": hashlib.sha256(source).hexdigest(),
        }]),
        "active_collections": ACTIVE_COLLECTIONS,
        "actor": "migration-fixture-operator",
        "records": [{
            "source_path": target["physical_path"],
            "source_sha256": hashlib.sha256(source).hexdigest(),
            "mapping_ref": "synthetic-fixture-mapping",
            "privacy_review_ref": "synthetic-fixture-privacy-review",
            "semantic_review": review(decision=semantic_decision),
            "record": target,
            "reason": "synthetic migration fixture",
            "idempotency_key": "synthetic-vault-fixture:rec-migration-001:v3",
        }],
    }


def check(condition: bool, label: str, errors: list[str]) -> None:
    if not condition:
        errors.append(label)


def main() -> int:
    errors: list[str] = []
    temp_root = Path(__file__).resolve().parents[2] / ".tmp"
    temp_root.mkdir(parents=True, exist_ok=True)
    parent = temp_root / f"migration-executor-test-{uuid.uuid4().hex}"
    parent.mkdir()
    original_subprocess_run = subprocess.run
    branches: dict[Path, str] = {}
    unrelated_dirty: set[Path] = set()

    def fake_git_run(argv, *, capture_output=False, text=False, check=False, **kwargs):
        repo = Path(argv[2]).resolve()
        command = argv[3]
        if command == "branch":
            output = branches.get(repo, "migration/v3-fixture")
        elif command == "rev-parse":
            output = str(repo)
        elif command == "merge-base":
            output = ""
        elif command == "status":
            if repo in unrelated_dirty:
                output = "?? unrelated.md\0"
            else:
                source_path = repo / "records/rec-migration-001.md"
                expected = serialize_record(record())
                output = " M records/rec-migration-001.md\0" if source_path.is_file() and source_path.read_bytes() == expected else ""
        else:
            raise AssertionError(f"unexpected synthetic git command: {command}")
        return SimpleNamespace(stdout=output, stderr="", returncode=0)

    subprocess.run = fake_git_run
    try:
        repo, source = make_repo(parent)
        branches[repo.resolve()] = "migration/v3-fixture"
        migration_manifest = manifest(source)

        code, planned = run(repo, migration_manifest, mode="dry-run")
        check(code == 0 and planned.get("status") == "ready", "valid mapping did not pass dry-run", errors)
        check((repo / "records/rec-migration-001.md").read_bytes() == source, "dry-run changed the source", errors)

        code, applied = run(repo, migration_manifest, mode="apply")
        output_path = repo / "records/rec-migration-001.md"
        check(code == 0 and applied.get("written") == 1, "canonical CRUD did not persist the Record", errors)
        check(parse_record(output_path.read_bytes()) == record(), "persisted Record did not round-trip", errors)

        code, repeated = run(repo, migration_manifest, mode="apply")
        check(code == 2 and repeated.get("status") == "blocked",
              "an interrupted migration was not blocked on retry", errors)

        invalid_repo, invalid_source = make_repo(parent, "invalid-review-vault")
        branches[invalid_repo.resolve()] = "migration/v3-fixture"
        invalid_map = manifest(invalid_source, semantic_decision="needs_review")
        code, blocked = run(invalid_repo, invalid_map, mode="apply")
        check(code == 2 and blocked.get("status") == "blocked", "unaccepted semantic review was not blocked", errors)
        check((invalid_repo / "records/rec-migration-001.md").read_bytes() == invalid_source,
              "blocked semantic review changed the source", errors)

        stale_repo, stale_source = make_repo(parent, "stale-vault")
        branches[stale_repo.resolve()] = "migration/v3-fixture"
        stale_map = manifest(stale_source)
        stale_path = stale_repo / "records/rec-migration-001.md"
        stale_path.write_bytes(stale_source + b"unapproved change\n")
        before = stale_path.read_bytes()
        code, stale = run(stale_repo, stale_map, mode="apply")
        check(code == 2 and stale.get("status") == "blocked", "stale source fingerprint was not blocked", errors)
        check(stale_path.read_bytes() == before, "stale fingerprint failure changed the source", errors)

        traversal_repo, traversal_source = make_repo(parent, "path-vault")
        branches[traversal_repo.resolve()] = "migration/v3-fixture"
        traversal_map = manifest(traversal_source)
        traversal_map["records"][0]["source_path"] = "../outside.md"
        traversal_map["records"][0]["record"]["physical_path"] = "../outside.md"
        code, traversal = run(traversal_repo, traversal_map, mode="dry-run")
        check(code == 2 and traversal.get("status") == "blocked", "path traversal was not blocked", errors)

        update_repo = parent / "update-vault"
        (update_repo / "records").mkdir(parents=True)
        old_record = record("rec-update-fixture")
        old_record["physical_path"] = "records/rec-update-fixture.md"
        update_path = update_repo / old_record["physical_path"]
        update_path.write_bytes(serialize_record(old_record))
        changed = dict(old_record)
        changed["content"] = "Updated sanitized fixture prose."
        crud = RecordCrud(ACTIVE_COLLECTIONS, {old_record["record_id"]: old_record},
                          persistence=MarkdownRecordStore(update_repo))
        update_result = crud.update(
            old_record["record_id"], {"content": changed["content"]},
            expected_version=1, semantic_review=review(old_record["record_id"]),
            actor="fixture-curator", reason="exercise persistent canonical update",
        )
        check(update_result["record"]["record_version"] == 2, "CRUD update did not increment the version", errors)
        check(parse_record(update_path.read_bytes()) == update_result["record"],
              "CRUD update did not persist through the Markdown store", errors)
        reloaded = RecordCrud(ACTIVE_COLLECTIONS, persistence=MarkdownRecordStore(update_repo))
        check(reloaded.read("rec-update-fixture", authorized_vault_ids=["vault-fixture"])
              == update_result["record"],
              "persisted Record did not reload through the canonical CRUD state", errors)

        legacy_path = update_repo / "records/legacy-normalize.md"
        legacy_frontmatter = {
            "title": "Sanitized legacy fixture", "source": "conversa", "revision": 4,
            "visibility": "internal", "tags": ["fixture"],
        }
        legacy_body = "\nLegacy sanitized prose.\n"
        legacy_path.write_text(
            "---\n" + yaml.safe_dump(legacy_frontmatter, sort_keys=False).rstrip()
            + "\n---" + legacy_body,
            encoding="utf-8",
        )
        legacy_store = MarkdownRecordStore(update_repo)
        legacy_frontmatter, legacy_body, _ = legacy_store.read_legacy_document(
            "records/legacy-normalize.md"
        )
        legacy_crud = RecordCrud({}, records={}, persistence=MarkdownRecordStore(update_repo))
        normalized_frontmatter = dict(legacy_frontmatter)
        normalized_frontmatter.update({
            "source": "conversation", "revision": 5,
            "revision_note": "Deterministic V3 frontmatter vocabulary normalization",
        })
        legacy_crud.normalize_legacy_frontmatter(
            "records/legacy-normalize.md", normalized_frontmatter, legacy_body,
            expected_revision=4, actor="fixture-normalizer", reason="fixture deterministic normalization",
        )
        normalized, normalized_body, _ = MarkdownRecordStore(update_repo).read_legacy_document(
            "records/legacy-normalize.md"
        )
        check(normalized == normalized_frontmatter and normalized_body == legacy_body,
              "legacy normalization did not persist through canonical CRUD", errors)
        changed_legacy = dict(normalized)
        changed_legacy["title"] = "Unapproved title change"
        try:
            legacy_crud.normalize_legacy_frontmatter(
                "records/legacy-normalize.md", changed_legacy, normalized_body,
                expected_revision=5, actor="fixture-normalizer", reason="should be rejected",
            )
            errors.append("legacy normalizer accepted a field change outside its mapping")
        except ContractError:
            pass

        retry_repo, retry_source = make_repo(parent, "idempotent-crud-vault")
        retry_target = record()
        retry_manifest = manifest(retry_source)
        retry_crud = RecordCrud(ACTIVE_COLLECTIONS, persistence=MarkdownRecordStore(retry_repo))
        retry_arguments = {
            "source_path": retry_manifest["records"][0]["source_path"],
            "expected_source_sha256": retry_manifest["records"][0]["source_sha256"],
            "semantic_review": retry_manifest["records"][0]["semantic_review"],
            "migration_context": retry_manifest,
            "actor": retry_manifest["actor"],
            "reason": retry_manifest["records"][0]["reason"],
            "idempotency_key": retry_manifest["records"][0]["idempotency_key"],
        }
        first_retry = retry_crud.migrate(retry_target, **retry_arguments)
        second_retry = retry_crud.migrate(retry_target, **retry_arguments)
        check(first_retry["status"] == "accepted" and second_retry == first_retry
              and len(retry_crud.events) == 1,
              "same-request retry was not idempotent within the canonical gateway", errors)
        changed_retry_target = dict(retry_target)
        changed_retry_target["content"] = "Different proposal with the same key."
        try:
            retry_crud.migrate(changed_retry_target, **retry_arguments)
            errors.append("reused migration idempotency key accepted a different proposal")
        except ContractError:
            pass

        locked_record = record("rec-locked-fixture")
        locked_record["physical_path"] = "records/rec-locked-fixture.md"
        lock_path = retry_repo / "records/.rec-locked-fixture.md.crud.lock"
        lock_path.write_text("synthetic active lock\n", encoding="utf-8")
        try:
            MarkdownRecordStore(retry_repo).create(locked_record)
            errors.append("active CRUD write lock did not block persistence")
        except ContractError:
            pass
        check(not (retry_repo / locked_record["physical_path"]).exists(),
              "write-lock block created a Record file", errors)
        lock_path.unlink()

        wrong_branch_repo, wrong_branch_source = make_repo(parent, "wrong-branch-vault")
        branches[wrong_branch_repo.resolve()] = "main"
        wrong_branch_manifest = manifest(wrong_branch_source)
        code, wrong_branch = run(wrong_branch_repo, wrong_branch_manifest, mode="apply")
        check(code == 2 and wrong_branch.get("status") == "blocked",
              "main branch did not block migration apply", errors)
        check((wrong_branch_repo / "records/rec-migration-001.md").read_bytes() == wrong_branch_source,
              "wrong-branch block changed the source", errors)

        dirty_repo, dirty_source = make_repo(parent, "dirty-branch-vault")
        branches[dirty_repo.resolve()] = "migration/v3-fixture"
        unrelated_dirty.add(dirty_repo.resolve())
        dirty_manifest = manifest(dirty_source)
        code, dirty = run(dirty_repo, dirty_manifest, mode="apply")
        check(code == 2 and dirty.get("status") == "blocked",
              "unrelated dirty tree did not block migration apply", errors)
        check((dirty_repo / "records/rec-migration-001.md").read_bytes() == dirty_source,
              "dirty-tree block changed the source", errors)

    finally:
        subprocess.run = original_subprocess_run
        shutil.rmtree(parent)

    if errors:
        print(f"validate_v3_migration_executor: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print("validate_v3_migration_executor: OK — dry-run, canonical persistence/update/legacy normalization, idempotency, stale source, semantic and Git gates, path containment")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
