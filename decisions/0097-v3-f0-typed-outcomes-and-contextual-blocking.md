# 0097 — V3 F0 typed outcomes and contextual blocking

**Status:** Accepted for the unreleased V3 candidate

## Context

Some proof gaps are semantic or outside the host's reach. Absence of proof is
not automatically false, but some purposes cannot proceed without it.

## Decision

Record typed outcomes such as `partial`, `observational`,
`authorization_required`, `unavailable` and `blocked`. Block only when the
missing proof is required by the applicable purpose and phase.

## Rationale

This preserves transparency for semantic limits while retaining fail-closed
behavior where privacy, authority, publication or migration risk requires it.

## Consequences

Semantic limits remain transparent, while privacy, authority, publication and
migration risks can remain fail-closed when necessary.

## Discarded alternatives

- Always failing closed was rejected because it confuses semantic uncertainty
  with falsity.
- Warning and continuing by default was rejected because critical risks could
  be silently carried forward.

## Validation plan

Exercise inaccessible sources, unproven remote deletion, incomplete semantic
revalidation and publication without destination privacy proof.
