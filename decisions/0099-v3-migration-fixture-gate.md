# 0099 — V3 migration fixture gate

**Status:** Accepted for the unreleased V3 candidate

## Context

The V3 candidate now has a `2.x -> 3.0` migration boundary, but a migration
plan is not executable evidence. Before any real vault is considered, the
blocking conditions must be exercised against sanitized synthetic cases.

## Decision

Use a deterministic migration-fixture gate with the following required
conditions:

- source and target versions are declared;
- field and semantic mapping is complete and unambiguous;
- privacy is proven for source, destination and derived representations;
- rollback is tested;
- the target contract is verified;
- human approval identifies the exact vault and scope;
- no raw sensitive material is automatically routed through the old V2.2
  pending-access fallback.

The gate returns `ready`, `authorization_required`, `blocked` or `partial`.
Missing mapping, unknown privacy, missing rollback, missing target contract or
unsafe raw fallback are blocking. Missing human approval is
`authorization_required` when all technical preconditions are complete.

Fixtures are evidence of gate behavior only. They do not migrate a vault,
prove remote access, establish semantic truth or authorize publication.

## Rationale

Migration risk is concentrated in ambiguity, privacy, rollback and destination
authority. Exercising those boundaries with synthetic inputs provides a
repeatable test without exposing or modifying real knowledge.

## Consequences

- The V2.2-to-V3 matrix now has an executable evidence reference.
- A real-vault migration cannot be described as ready from documentation alone.
- The old pending-access fallback remains historical and cannot bypass V3
  policy.

## Discarded alternatives

- Treating a complete mapping as sufficient was rejected because it does not
  prove destination privacy, rollback or approval.
- Treating human approval as the only gate was rejected because technical
  safety conditions must fail closed.
- Testing directly on a real vault first was rejected because it creates
  irreversible privacy and rollback risk before the gate is exercised.

## Validation plan

Run `python scripts/validate_v3_migration.py` and include the fixture file in
the F0 script inventory. All synthetic cases must produce their declared
outcome.
