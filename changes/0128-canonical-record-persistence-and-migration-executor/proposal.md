# Change Set 0128 — Canonical Record persistence and migration executor

## Problem

V3 `RecordCrud` validated mutations in memory but did not persist V3 Markdown
Records. The available legacy writer only normalized frontmatter and could not
serve as the V2-to-V3 migration path. A migration script that wrote files
directly would create a second mutation boundary.

## Proposed change

Add a Markdown persistence adapter invoked by canonical `RecordCrud` only
after semantic and deterministic validation. It loads existing V3 Records,
persists Create and Update atomically, and compares expected on-disk state.
Add an internal migration method on `RecordCrud` and a deterministic executor
that accepts a complete, reviewed vault-local manifest. The executor runs
dry-run by default, requires complete mapping/privacy/destination/rollback and
exact-vault approval declarations, verifies source fingerprints, and refuses
to run on `main`, a branch that does not include local `main`, or a dirty tree.

The migration operation is internal to the canonical gateway and is not added
to the MCP operation surface. An interrupted multi-Record batch stays on its
dedicated branch and blocks automatic retry; recovery must be reviewed
separately. The script summary contains counts and status only.

## Acceptance criteria

- Create, Update, and V3 reload use the same canonical Markdown persistence
  adapter after CRUD validation.
- Migration persistence is invoked only from `RecordCrud.migrate` after full
  Record structure and accepted semantic review pass.
- The migration executor requires an exact-vault manifest with complete
  preflight statuses, per-Record source hashes, mapping references, privacy
  references, review envelopes, and unique idempotency keys.
- Dry-run makes no writes; apply blocks on missing mapping, rejected review,
  stale source, path escape, wrong branch, dirty tree, or incomplete inventory
  fingerprint.
- A single Record replacement is atomic and round-trips through the V3 store.
- A second apply after an interrupted or completed write does not silently
  resume the migration.
- Synthetic tests prove these local code paths while making no claim about real
  vault semantic readiness or host authorization.

## Compatibility and recovery

Operational, additive implementation for the unreleased V3 candidate; no
SemVer impact to the released V2.2 package. Existing V2 documents remain
untouched by default. A future real migration must provide a complete
vault-specific manifest, validated rollback, dry-run review, and the existing
human gates. Each per-file write uses same-directory atomic replacement; Git
history on the dedicated branch preserves the source version. A partial batch
is not auto-resumed.

## Risks and limits

- The executor checks manifest declarations and fingerprints but cannot prove
  semantic truth, privacy correctness, or completeness of the repository-wide
  inventory.
- The Markdown store supports one-record atomic writes; it does not provide a
  whole-vault transaction.
- A process interruption after one or more writes requires separate recovery
  review.
- V3 remains an unreleased candidate; the implementation does not authorize
  skill installation, publication, push, merge, or real-vault execution.

## Status

Implemented on the local candidate branch for synthetic validation. Real-vault
migration remains blocked until per-vault inventories, mappings, privacy
reviews, destination checks, and rollback evidence are complete.
