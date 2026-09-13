# 0095 — V3 F0 phase verification matrix

**Status:** Accepted for the unreleased V3 candidate

## Context

Execution, review, publication, migration and retraction carry different risks
and cannot share an undifferentiated gate.

## Decision

Use a phase matrix with required checks, blocking results and evidence for each
of the five contexts.

## Rationale

Controls should be proportional to lifecycle risk without allowing a later
phase to silently skip a required proof.

## Consequences

Local execution may have a smaller proof burden than publication or migration.
Operations crossing phases must satisfy all applicable phase requirements.

## Discarded alternatives

- A universal gate was rejected as excessive and context-blind.
- Minimal checks only at execution were rejected as insufficient for publication
  and migration.

## Validation plan

Exercise local execution, Package receipt, publication, migration and
retraction fixtures with both complete and missing proof.
