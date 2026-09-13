# 0088 — V3 surface authority, offline behavior and external references

**Status:** Accepted for the unreleased V3 contract

## Context

The methodology, skill, vault documentation and external references have
different authority roles. Offline operation must remain safe when a source is
missing, stale or contradictory.

## Decision

The canonical SPEC and accepted Decision Records remain normative. The skill
is a procedural adapter and cannot silently replace an unavailable or newer
canonical source. Offline operation is limited to locally proven behavior;
missing, stale or conflicting normative sources are disclosed and block the
dependent operation. External references may be labelled comparison,
inspiration, research or context, but are not adopted authorities,
dependencies or formats without a separate Decision Record.
## Rationale

An explicit surface hierarchy makes offline behavior explainable and prevents
recent copies, README prose or external frameworks from silently overriding
the canonical contract.

## Discarded alternatives

- Treating the newest accessible copy as authoritative.
- Making external frameworks implicit dependencies.
- Continuing a normative operation when its required source is unavailable.
