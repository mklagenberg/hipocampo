# Change Set 0132 — V3 release contract and packaging

## Problem

The V3 candidate cannot be released while the root specification, canonical
skill, scaffold and package checks still declare V2 contracts. Historical
candidate approval is not approval of a stable package with different bytes.

## Proposed change and acceptance criteria

- Prepare a coherent 3.0.0 contract and 2.0.0 skill, preserving immutable V2
  history and the approved rc.1 candidate.
- Synchronize normative routing, package/tuple metadata, bootstrap proposals,
  migration and recovery guidance, changelog and conformance declarations.
- Replace fixed old-version checks with actual tuple/package consistency and
  adversarial regressions; keep human and publication gates fail-closed.
- Separate local proof from host capability, remote operation and bulk adoption.
- Freeze content, assess the exact package with two AI passes, then obtain
  human approval. Verify a subsequent evidence-only commit.

## Alternatives, risks, migration and recovery

Metadata-only promotion and overwriting approved history were rejected.
Risk: incomplete normative projection; review the V3 contracts and run the
integrated engine suite. V2 compatibility is intentionally broken for V3
writes, while immutable V2 packages remain usable on compatible V2 instances.
Use per-vault mappings, accepted privacy/Collection gates, canonical migration
and exact-ticket recovery. No automatic adoption or direct Record rewrite.

## Status

Implementation preparation authorized; acceptance, merge and publication are
pending exact final review. This Change Set is not frozen as accepted.

## Recorded acceptance

Accepted by explicit operator response on 2026-10-07 for frozen content cd95e955,
final skill lock 2462816441e5e829579014207403dbf8342c6c500bdb4691792a5d8a4aa84f9b
and both FINAL-003 AI reviews. Preparation-time pending status above is historical.
Integration is authorized through a PR to main after CI/content verification;
publication is human-only. A post-acceptance test-fixture correction separates
synthetic pending-human input from the actual approved envelope, so the test
continues to reject missing approval without requiring a real decision to stay
pending forever. It changes neither package bytes nor the normative gate.
