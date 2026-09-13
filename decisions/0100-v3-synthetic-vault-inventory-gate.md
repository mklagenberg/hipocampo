# 0100 — V3 synthetic vault inventory gate

**Status:** Accepted for the unreleased V3 candidate

## Context

The migration fixtures test individual blocking conditions, but migration
preparation also needs to classify complete vault profiles. A single generic
case cannot expose the differences between an anchor vault, an additional
vault with an inaccessible artifact frontier and an invited vault that cannot
be reached.

## Decision

Use sanitized, vault-shaped inventories before preparing any real-vault
inventory. Each inventory declares entity, role, source and target versions,
access, mapping, privacy, rollback, target contract, approval and artifact
frontier.

The evaluator returns the strongest applicable state:

- `blocked` for unavailable access, incomplete or ambiguous mapping,
  unproven privacy, untested rollback, missing target contract or unsafe raw
  fallback;
- `authorization_required` when technical checks pass but human approval is
  absent;
- `partial` when migration can be prepared with an explicitly bounded
  artifact frontier;
- `ready` only when all required technical and human gates pass.

An inaccessible artifact may remain an explicit reference with a bounded
frontier. It must not be silently reconstructed, fetched or promoted.

## Rationale

Vault-level profiles exercise routing and authority boundaries while keeping
the test deterministic and free of real knowledge. They make it possible to
prepare later per-vault work without treating one successful fixture as proof
that every vault is migratable.

## Consequences

- Inventory readiness is per vault, not a repository-wide assumption.
- `partial` is a valid preparation result but not authorization to migrate.
- The first real inventory, when separately authorized, must follow the same
  schema and retain inaccessible frontiers explicitly.

## Discarded alternatives

- One global migration status was rejected because entities, roles and access
  boundaries differ by vault.
- Treating an inaccessible artifact as a blocker in every case was rejected
  when a bounded reference is sufficient for the selected migration purpose.
- Treating an inaccessible artifact as available was rejected because it would
  invent content or authority.

## Validation plan

Run `python scripts/validate_v3_inventory.py` and confirm that all synthetic
vault profiles produce their declared typed outcome.
