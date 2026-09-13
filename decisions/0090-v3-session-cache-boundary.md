# 0090 — V3 session and cache boundary

**Status:** Accepted for the unreleased V3 contract

## Context

Transient conversation context and cache must not silently become durable
knowledge or a sensory capture.

## Decision

Implement D6.1/D6.5 session disposition: discard transient context unless
capture was explicitly authorized; keep cache, capture and durable events
distinct and disclose host limitations.

## Rationale

The boundary protects privacy while allowing an explicit, reviewable capture
path.

## Consequences

Interruption and restart do not create Records. Host retention that cannot be
controlled is observational or unavailable.

## Discarded alternatives

- Automatically persisting session context.
- Treating every cache entry as an operational log.

## Validation plan

Exercise interrupted, restarted, unauthorized and explicitly authorized
sessions.
