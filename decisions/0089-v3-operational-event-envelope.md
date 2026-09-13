# 0089 — V3 operational event envelope

**Status:** Accepted for the unreleased V3 contract

## Context

MRL-0006 needs deterministic operational transparency without turning logs into
a second knowledge store.

## Decision

Implement the D6.1 layered event envelope with transient session, authorized
sensory capture and bounded durable operational layers. Redact secrets and
content bodies before persistence.

## Rationale

The envelope proves occurrence and limits, not semantic truth, and preserves
the distinction between events, ledgers, Packages and knowledge.

## Consequences

Every X6 event declares layer, target, proof scope, rule revision, retention
and limits. Compensating events correct the trail without silent deletion.

## Discarded alternatives

- Minimal unstructured result logs.
- Content-rich execution diaries.

## Validation plan

Exercise success, failure, unavailable, redaction and regression fixtures.
