# Change Set 0127 — V3 synthetic branch and request gates

## Problem

The coverage-gap suite blocked preflight after an interrupted migration but did
not prove the Git-based recovery boundary accepted by the operator: partial
versioned work must remain on a dedicated task branch while `main` stays at its
baseline until validation. The skill capability case checked instructions and
a missing-capability example, but did not exercise the request outcomes across
capability and authorization states.

## Proposed change

Extend the existing synthetic migration scenario to create a temporary Git
repository, commit a baseline, and create a partial migration on a dedicated
branch. Assert that the partial files and commit remain on that branch and that
`main` retains its original SHA before validation. Keep the migration evaluator
fail-closed for interrupted execution; do not add a migration recovery engine.

Extend the existing skill capability scenario with a synthetic Search/CRUD
adapter. Before I/O, it gates on declared capability and authorization. The
matrix covers `proven`, `observational`, `unavailable`, and
`authorization_required`, with missing and valid authorization. Denied cases
must expose no Record content and perform no Read or Write. The authorized case
must use exactly one canonical CRUD Read. Retain the revocation-between-snapshot
and-Read assertion.

These adapters are deterministic test doubles. They do not demonstrate that a
real host implements capability discovery, enforces its authorization rules,
or has no side effects outside the Git repository.

## Acceptance criteria

- an interrupted partial migration remains on its dedicated branch;
- the temporary repository's `main` SHA and contents remain unchanged before
  validation, with no merge performed;
- preflight still blocks an interrupted execution state and makes no source or
  target promotion;
- missing authorization and non-proven capabilities return a typed stop before
  snapshot access, canonical Read, or Write;
- the proven and authorized case reaches Search through exactly one canonical
  CRUD Read and makes no mutation;
- revocation after candidate discovery returns no content and makes no mutation;
- the integrated suite runs the expanded scenarios and reports their synthetic
  proof boundary explicitly;
- existing semantic assessment results and human dispositions remain unchanged.

## Compatibility and boundaries

This is an operational, additive test-coverage change with no SemVer impact.
It changes neither the published V2 package nor the active compatibility tuple.
All test data is synthetic and the Git repository is temporary. No vault is
read, changed, migrated, or used as a fixture.

## Status

Implemented in the local candidate branch after deterministic and integrated
validation. This Change Set does not authorize real-vault preflight, remote
merge, release, installation, or activation.
