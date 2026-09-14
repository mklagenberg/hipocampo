# 0105 — V3 Learning & Evolution engine

**Status:** Accepted for the unreleased V3 candidate

## Context

The logical engine catalog can organize known behavior, but V3 also needs a
controlled way to discover missing cases from repeated operational signals,
audit findings, validator outcomes, incidents and lessons learned. Frequency
alone is not evidence that a new rule is correct, and an automatic test
generator could activate behavior without governance.

## Decision

Add Learning & Evolution as a logical engine. It consumes bounded, sanitized
signals and reviewed lessons, fingerprints and deduplicates them, identifies
the responsible engine, and produces a candidate use case or a recommendation
to classify the signal as a duplicate, bug, documentation gap, decision or
lesson-only item.

The engine never writes a Record, changes a contract, activates a test or
publishes a release. An approved candidate must pass semantic review, become a
Change Set when methodology behavior changes, receive deterministic and
semantic fixtures, and pass verification before incorporation into the
catalog.

Operational events show what happened; lessons learned explain what should
change. Neither is treated as semantic truth without review.

## Rationale

This creates a feedback loop from real operation to methodology evolution while
preserving provenance, privacy, human direction and the exclusive CRUD Record
mutation boundary.

## Discarded alternatives

- Automatically promoting repeated log patterns into rules was rejected because
  recurrence does not establish correctness or applicability.
- Treating Learning & Evolution as part of the CRUD engine was rejected because
  case discovery and Record persistence have different authority and lifecycles.
- Writing raw logs into the candidate queue was rejected because logs may carry
  credentials, private content or unreviewed interpretations.

## Consequences

- V3 now has eleven logical engines, while its physical module organization
  remains unchanged.
- Candidate states and semantic review become explicit.
- A new use case is traceable from signal or lesson to fixture, Change Set and
  verification result.
- Semantic learning remains review-bound rather than being disguised as
  deterministic truth.

## Validation

Run `scripts/validate_v3_learning_engine.py --root .`,
`scripts/validate_v3_engine_catalog.py --root .`,
`scripts/validate_v3_engine_suite.py --root .` and the complete repository
suite twice. No real vault, cache or external service is required.
