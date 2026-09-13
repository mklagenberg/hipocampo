# Change Set 0080 — V3 transfer and retraction

## Problem

Delivery, acceptance, current use and retraction must not collapse into one
operation. A received Package needs a local pending representation, and a
retraction must preserve the evidence trail while stopping current use.

## Proposed contract

Implement the distinction between selective Package delivery and publication,
with source and destination provenance, destination acceptance, `new`/
`pending_rem`, bilateral ledger pairing and additive retraction/tombstone
events. A Package remains delivery, never automatic promotion.

## Risks and compatibility

This remains an unreleased V3 candidate. It does not transport data, migrate
vaults, delete history or activate current use in existing instances.

## Acceptance criteria

- selected content, purpose, source, generator, destination, version and
  fingerprint are retained;
- receipt is not curation;
- sent and received records can be paired;
- retraction blocks current use without deleting history;
- partial and rejected deliveries are covered by fixtures.

