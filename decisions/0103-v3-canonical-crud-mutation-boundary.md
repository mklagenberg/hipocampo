# 0103 — V3 canonical CRUD mutation boundary

**Status:** Accepted for the unreleased V3 candidate

## Context

The V3 candidate had separate in-memory routines for Artifact divergence,
processed ingress, received-package promotion, migration preflight and audit.
Some routines could produce Record-shaped mutations without crossing one
explicit persistence boundary. That made it possible for a future MCP adapter
or engine to bypass version control, semantic review, provenance and audit.

## Decision

All V3 Record creation, update, archive and deletion decisions must cross one
canonical CRUD gateway. The gateway has two distinct responsibilities:

- semantic validation or an explicit semantic-review decision establishes
  admissibility in context;
- deterministic validation enforces structure, references, versioning,
  immutability, idempotency, state transitions and atomic commit.

MCP is only a transport adapter for the CRUD gateway. It cannot expose direct
file writes or an alternative Record persistence path. Specialized engines may
prepare proposals, findings, packages, migration plans or reviews, but they
cannot persist a Record.

Operational metadata such as queues, events, ledgers and Artifact indexes is
not a Record and keeps its own `meta/` persistence rules. If an operation needs
to change a Record field, it must submit a CRUD mutation.

## Consequences

- Record version conflicts fail closed.
- Artifact updates preserve the historically used version and create a review
  boundary instead of silently rewriting knowledge.
- Processed ingress cannot overclaim processing without explicit proofs.
- Receipt acceptance cannot promote stale or immature content to current use.
- Migration preflight cannot succeed without explicit source and target
  versions.
- Fingerprint disagreement cannot be reported as valid integrity.
- The 18 use cases in `docs/v3-crud-governed-use-cases.md` become a V3 gate.

This decision does not migrate a vault, activate V3, publish a release, or
authorize remote MCP/GitHub writes.

## Rationale

One mutation boundary makes versioning, provenance, privacy and audit
enforceable regardless of whether the caller is an MCP client, a migration
routine or a maintenance engine. Keeping semantic review separate from
deterministic commit prevents a structural pass from being mistaken for a
claim that knowledge is true or current.

## Discarded alternatives

- Allowing each engine to write its own Record-shaped result was rejected
  because it creates bypasses and inconsistent version histories.
- Treating MCP as an authorized persistence layer was rejected because
  transport does not establish governance or semantic admissibility.
- Making deterministic validation decide semantic truth was rejected because
  applicability, authority, conflict and meaning require contextual review.
- Using physical deletion as the default CRUD delete was rejected because it
  destroys provenance; archive/tombstone remains the governed default.

## Validation

Run `scripts/validate_v3_crud.py`, `scripts/validate_v3_artifacts.py`,
`scripts/validate_v3_x4.py`, `scripts/validate_v3_migration.py`,
`scripts/validate_v3_l4r_closure.py` and
`scripts/validate_v3_crud_use_cases.py`. The final semantic review remains a
human or agent-reviewed record with sanitized evidence; deterministic green
status alone does not prove semantic truth.
