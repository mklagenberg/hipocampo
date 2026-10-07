# 0116 — Canonical Record persistence and V3 migration execution

**Status:** Accepted for the scoped local experiment

**Date:** 2026-10-05

## Context

The V3 Record CRUD contract defines the canonical mutation boundary and
requires deterministic validation before persistence. The current fixture
engine validated proposals in memory, while its legacy Markdown writer only
normalized V2 frontmatter. No executable path applied a reviewed V2-to-V3
mapping through the canonical gateway and persisted the validated result.

## Decision

Accepted by the operator on 2026-10-06 for the local WRK-0074 experiment.

Give the canonical `RecordCrud` gateway an optional persistence adapter for
Markdown-backed Records. The adapter loads V3 Records, creates and updates
canonical V3 documents atomically, and rejects stale on-disk state. Add an
internal `RecordCrud.migrate` operation for an explicitly mapped V2 document;
keep it out of the logical MCP surface. The operation requires an accepted
semantic review, exact source hash, exact-vault approval, complete mapping and
privacy evidence, verified destination, tested rollback, and an untouched
migration branch.

The deterministic executor accepts a vault-local manifest containing complete
Record proposals and review references. It defaults to dry-run, prints only a
sanitized summary, and applies only after all preflight checks pass. The
executor never writes Record files directly. An interrupted batch remains on
its task branch and blocks another apply until a separately governed recovery.

## Rationale

This makes the script a coordinator and the CRUD gateway the single write
boundary. Deterministic execution prevents drift between reviewed mappings and
persisted values; it does not decide semantic meaning, authority, privacy, or
truth. Per-file atomic replacement and Git branch isolation provide a clear
recovery boundary without claiming whole-vault transactional atomicity.

## Discarded alternatives

- Let the migration script write Markdown directly after validating a Record:
  rejected because it creates a second write boundary and bypasses the CRUD
  gateway.
- Reuse the legacy frontmatter normalizer:
  rejected because it does not validate or serialize a complete V3 Record.
- Automatically resume an interrupted batch:
  rejected because migration preflight explicitly blocks an already-started
  execution until its state and recovery plan are reviewed.
- Infer missing mapping fields from folder names or legacy values:
  rejected because it can change authority, scope, privacy, or epistemic state
  without evidence.

## Constitutional and contract impact

Compatible with `FF-CON-0001:2.2`, `2.6`–`2.10` and section 4. The design
keeps interpretation separate from deterministic validation, makes the CRUD
gateway the only Record writer, preserves uncertainty, minimizes output, and
keeps each migration branch recoverable. It does not publish V3, install the
candidate skill, or authorize a real-vault write without a complete manifest.

## Validation

Run the migration executor validator and CRUD validators; run the integrated
V3 engine suite, migration fixtures, engine catalog, repository, Change Set,
skill, contract, and compatibility validators. Exercise dry-run, accepted and
rejected semantic reviews, source-hash drift, path containment, canonical
Create/Update persistence, round-trip loading, branch checks, and interrupted
execution. Keep real vaults outside the test fixtures.

## Approval

The operator explicitly accepted the canonical persistence design and Change
Set 0128 on 2026-10-06, after being presented with the three entry decisions.
This acceptance covers the architecture for the local experiment only. It
does not accept individual Collections, mappings, semantic reviews, privacy
claims or recovery declarations. Decision 0117 records the experiment scope;
V3 release and real-vault readiness remain separate gates.
