# 0092 — V3 operational correlation

**Status:** Accepted for the unreleased V3 contract

## Context

CRUD, Package, validation, evaluation and retraction need deterministic links
without centralizing content or leaking inaccessible vaults.

## Decision

Implement D6.3/D6.2 correlation through IDs, fingerprints, causation,
evidence references, rule revision and explicit inaccessible frontiers.

## Rationale

Structured correlation is more auditable than free text and safer than a
central content-bearing graph.

## Consequences

Correlation never changes Package authority, ledger authority or knowledge
content. An inaccessible frontier remains unresolved.

## Discarded alternatives

- Free-form text as the primary correlation mechanism.
- A global operational graph containing content.

## Validation plan

Exercise CRUD → Package → validation → receipt → retraction with an
inaccessible vault.
