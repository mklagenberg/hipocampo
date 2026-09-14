# Change Set 0106 — V3 semantic validation

## Intent

Execute the semantic evaluation boundary for the unreleased V3 candidate
against sanitized fixtures and read-only metadata from the four authorized
local vault caches.

## Scope

This Change Set records semantic evaluation evidence. It does not change the
released V2.2 contract, migrate a vault, publish V3, or write a Record. The
evaluation covers the 22 cases in the logical engine matrix plus the two
additional Learning & Evolution cases declared by its engine-specific case
file.

The evidence package stores only sanitized summaries, logical source labels,
and SHA-256 references. Local vault content remains outside this repository.

## Method

Each case receives a primary semantic evaluation and an adversarial second
pass. The second pass challenges epistemic classification, provenance,
scope, temporal validity, negative behavior and authority boundaries. A
disposition of `needs_review`, `blocked`, `provisional` or `rework_required`
is a valid result; it is not silently converted to approval.

## Acceptance criteria

- all 24 semantic cases are explicitly evaluated;
- the 22/24 scope discrepancy is reconciled;
- every case has primary and adversarial dispositions;
- all case outcomes retain the expected human or host review boundary;
- the Learning & Evolution recurrence case cannot be auto-accepted;
- no Record, vault cache, external service, contract, test or release is
  mutated by the evaluation;
- the evaluation package passes its deterministic completeness validator;
- any semantic mismatch becomes a correction, rework item or human gate.

## Finding corrected during execution

`LEARN-S-001` was declared `accepted` in the engine-specific case file but
`needs_review` in the matrix. The matrix and the engine policy are semantically
correct: recurrence is a signal for review, not proof that a new rule is
correct. The engine-specific case was corrected to `needs_review`, and
`LEARN-S-003` and `LEARN-S-004` were added to the canonical matrix.

## Recovery

Remove this evidence Change Set and revert only its documentation and
validator changes. No real-vault or external state is affected.
