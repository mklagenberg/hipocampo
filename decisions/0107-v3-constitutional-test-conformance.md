# 0107 — V3 constitutional test conformance

**Status:** Accepted for the unreleased V3 candidate

## Context

The V3 test package was created before the project Constitution was adopted.
Its deterministic validators prove execution and structural completeness, and
its semantic package records reviewed dispositions, but neither package
required an explicit constitutional or Decision Record basis for every case.

## Decision

Adopt a constitutional conformance layer for V3 verification:

1. every deterministic matrix case must bind to an executable validator command
   and an observable assertion;
2. every semantic case must declare the applicable Constitution clauses,
   Decision Records, authority scope and whether an exception is involved;
3. a rule that conflicts with the Constitution without an accepted scoped
   Decision Record is blocked;
4. a constitutional amendment creates a rejudgment obligation, and affected
   rules remain `review-required` until adjudicated;
5. semantic validators verify the completeness and integrity of this envelope,
   not the truth of a semantic conclusion.

## Rationale

The prior package could be structurally green while leaving the normative
reason for a case implicit. Explicit bindings make deterministic coverage
auditable; explicit constitutional and Decision Record references make
semantic review reproducible without pretending that meaning is mechanically
provable.

## Discarded alternatives

- Treating a green command as proof that every named deterministic case ran was
  rejected because the prior matrix stored labels without executable bindings.
- Treating `decision_basis` prose as sufficient normative traceability was
  rejected because it could not be checked against the Constitution or accepted
  Decision Records.
- Automatically accepting a bounded constitutional exception was rejected
  because scope, risk, privacy and authority remain semantic and human-gated.

## Boundaries

This decision changes the verification package for the unreleased V3
candidate. It does not publish V3, alter V2.2, migrate vaults, authorize
remote writes or turn the Constitution into a Record mutation route.

## Acceptance

Accepted by the project operator on 2026-09-14 as execution of the approved
constitutional revalidation plan.
