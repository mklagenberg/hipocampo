# 0091 — V3 CRUD operational events

**Status:** Accepted for the unreleased V3 contract

## Context

CRUD and exceptional actions need an audit trail without making the trail a
copy of Record, Chunk, Artifact or Package content.

## Decision

Implement D6.3 bounded CRUD events for governed actions, with target, actor,
entity, scope, result, approval, retention and redaction metadata.

## Rationale

Operational audit and content history are different concerns and must remain
separable.

## Consequences

Reads are not automatically durable knowledge events; only defined auditable
reads or exceptional actions emit events.

## Discarded alternatives

- Logging every read as durable knowledge.
- Storing full content snapshots in operational events.

## Validation plan

Exercise create, governed read, update, archive, retraction, failure and
unavailable target cases.
