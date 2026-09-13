# 0093 — V3 host capabilities and revocation reach

**Status:** Accepted for the unreleased V3 contract

## Context

Host logging, retention, cache invalidation and revocation capabilities vary.
The methodology must not claim global guarantees it cannot prove.

## Decision

Implement D6.4/D6.5 capability states and a revocation reach matrix. Classify
capabilities as proven, observational, unavailable or authorization-required;
record what was invalidated and block dependent use outside proven reach.

## Rationale

The matrix is transparent and portable while preserving Privacy First and the
distinction between deterministic traceability and semantic truth.

## Consequences

TTL is not proof of revocation. External backups and inaccessible caches are
declared rather than silently treated as removed. Derived projections remain
non-authoritative.

## Discarded alternatives

- Presuming host capabilities.
- Requiring synchronous global revocation on every host.

## Validation plan

Exercise proven, partial and unavailable hosts with Package, cache, index and
context revocation cases.
