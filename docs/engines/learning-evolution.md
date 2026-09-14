# Learning & Evolution Engine

**Status:** unreleased V3 candidate; logical capability boundary.

Learning & Evolution discovers candidate use cases from bounded operational
signals and sanitized lessons learned. It may read events, audits, validator
results and reviewed lessons, but it does not turn frequency into truth or
write a Record, contract or test suite directly.

## Signal sources

- repeated deterministic blocks or unexpected outcomes;
- audit mismatches, retractions and inaccessible frontiers;
- recurring semantic review findings;
- false positives and false negatives;
- manual overrides and repeated reprocessing;
- sanitized lessons learned from incidents or retrospectives.

## Flow

```text
signal -> sanitize -> fingerprint/deduplicate -> triage
       -> candidate -> semantic review -> Change Set -> tests -> verification
```

The engine distinguishes an existing-case duplicate, an implementation bug, a
documentation gap, a new deterministic case, a new semantic case, a policy
decision and a lesson that should remain local. Only an approved candidate can
produce a proposed case, and activation always requires a Change Set and
verification.

## Boundaries

Deterministic validation proves signal identity, privacy envelope, lineage,
deduplication and activation preconditions. Semantic review decides whether a
signal reveals a real methodological gap, whether the lesson generalizes, which
engine owns it and what expected disposition is appropriate.

The implementation is in `scripts/v3_learning_engine.py`; its executable cases
are in `docs/engines/learning-evolution-cases.yaml` and
`scripts/validate_v3_learning_engine.py`.
