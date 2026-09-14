# Change Set 0071 — V3 record state and separated queues

## Intent

Implement the accepted V3 planning decisions as a bounded candidate contract:
independent processing/maturity/epistemic/staleness dimensions, three
maintenance queues, a deterministic frontmatter normalizer, and an explicit
response boundary.

## Scope

This Change Set defines the unreleased V3 contract and provides local scripts
and fixtures to exercise it. It updates the skill-facing operational guidance
only through the contract references; it does not migrate a real vault, change
the released v2.1.1 contract, create external connectors, or implement the
Record CRUD package.

## Implementation

- `docs/v3-contract.md` defines the candidate envelope, response matrix,
  queue schema, cadence, and migration boundary;
- `scripts/scan_v3_queues.py` scans frontmatter and deterministic TTL findings;
- `scripts/normalize_frontmatter_queue.py` applies only supported vocabulary
  corrections and blocks staleness/semantic queues;
- `scripts/validate_v3_queues.py` exercises the full deterministic path in a
  temporary vault;
- `docs/v3-queue-fixtures.yaml` covers positive and negative queue behavior;
- the public specification points to the candidate without claiming the V3
  release is active.

## Semantic boundary

The scripts do not decide truth, authority, merge/split adequacy, privacy
intent, promotion, or disposition of stale content. Semantic findings remain
for REM or human review. The Liferay exercise remains management evidence and
is not copied into this repository.

## Compatibility, rollback, and publication

V2 documents remain readable. No migration runs. Reverting this Change Set
removes the candidate tooling and documentation without deleting Decision
Records or changing a vault. A future V3 release requires a separate release
gate, migration plan, skill compatibility decision, and human publication
action.
