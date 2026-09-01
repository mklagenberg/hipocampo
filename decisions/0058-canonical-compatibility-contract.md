# 0058 — Canonical compatibility contract

**Status:** Accepted

## Context

The methodology, its client-side skill, and each content vault declare related
but separate versions and contracts. Without one decision surface, an agent
can mistake a matching version number for compatibility, or treat missing
evidence as permission to proceed. `UPGRADE.md` and `MIGRATIONS.md` explain
remediation, but neither is the operational compatibility decision itself.

## Decision

Adopt `COMPATIBILITY.yaml` as the canonical compatibility contract. It defines
the current methodology tuple, the skill manifest and package-lock references,
the required vault-manifest declarations, five explicit states, and their
precedence. The states are `compatible`,
`compatible_with_recommended_alignment`, `migration_required`,
`unsupported_or_unknown`, and `access_unavailable`.

Only the first two states permit an operation to continue, subject to the
other invariants and write gates. Unknown, unavailable, or incompatible state
blocks the operation and hands the next action back to the operator. The
contract does not replace upgrade or migration guidance and does not add a
mandatory field to existing vaults in this change.

## Rationale

A small explicit state machine is easier to audit than scattered version
comparisons. Separating availability, integrity, semantic compatibility, and
authorization preserves the distinctions already established by the
methodology and avoids turning a missing source into an implicit allow.

## Discarded alternatives

- **Infer compatibility from equal version numbers.** Rejected because it
  hides contract and package divergence.
- **Treat an unknown result as compatible.** Rejected because it grants
  permission without evidence.
- **Put the complete decision only in `UPGRADE.md` or `MIGRATIONS.md`.**
  Rejected because those documents answer remediation, not the gate result.
- **Require a published package lock for every existing operation immediately.**
  Deferred as a separate adoption and distribution decision.

## Status

Accepted on 2026-08-31. Implementation is tracked by Change Set
`0058-compatibility-contract`.
