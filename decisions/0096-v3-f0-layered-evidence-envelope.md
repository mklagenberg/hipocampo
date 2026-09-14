# 0096 — V3 F0 layered evidence envelope

**Status:** Accepted for the unreleased V3 candidate

## Context

Operational events must support traceability without becoming a content mirror
or storing credentials and sensitive knowledge.

## Decision

Use a common evidence envelope with operation-specific extensions for rule
revision, proof scope, result, coverage, limits, correlation, evidence,
redaction and retention.

## Rationale

The layered model keeps events comparable without forcing irrelevant fields or
turning operational evidence into a content mirror.

## Consequences

Event families remain comparable while retaining relevant differences. The
envelope remains operational evidence and never becomes knowledge authority.

## Discarded alternatives

- A fixed envelope was rejected as wasteful and potentially overexposing.
- Free-form per-script logs were rejected as difficult to audit consistently.

## Validation plan

Validate CRUD, Package, deterministic validation and revocation events against
the common envelope and sensitive-content boundary.
