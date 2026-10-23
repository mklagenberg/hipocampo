# 0142 — Bounded cleanup for synthetic Windows preflight fixtures

## Problem

The experimental V3.1.0 preflight can fail after the interrupted-migration
scenario has passed its Git assertions. On Windows, removal of its empty
synthetic repository intermittently raises `WinError 32` while another process
briefly holds the directory. This was reproduced in the installed distribution;
the same directory was removable after the transient lock cleared. A passing
direct engine run does not make a failed aggregate preflight pass.

The distribution guide also names skill 2.3.0 although the bundled skill and
compatibility contract name 2.4.0.

## Proposed change

Retry removal of only the scenario-owned synthetic repository for bounded
Windows sharing violations. Keep all Git assertions, scenario bindings and
other errors blocking. Test transient, persistent and unrelated cleanup errors
without relying on an intermittent filesystem race. Correct the stale skill
version sentence and record this candidate tooling fix in the changelog.

## Compatibility and migration

This is an operational test-harness fix and an editorial synchronization of a
version reference. It changes no V3 Record format, instance contract, skill
contents, scaffold output or vault behavior. No vault migration, skill version
bump or global installation follows from this Change Set.

## Risks and recovery

Retries could conceal a persistent lock if made unbounded or treated as a pass.
The implementation accepts only Windows sharing violations, uses a short fixed
attempt limit and re-raises the final error. The fixture path is created inside
the runner's selected synthetic root; no unrelated directory is removed. The
change is reversible by reverting its branch. Final review, host observations,
human approval, merge, tag and release retain their separate gates.

## Acceptance and validation

- A transient sharing violation is retried and then succeeds.
- A persistent sharing violation and an unrelated error remain failures.
- The interrupted-migration scenario still executes its Git assertions.
- Repeated installed-engine and aggregate experimental preflights pass on the
  frozen candidate with an exact payload fingerprint and no real-vault access.
- Repository, package, Change Set and contract validators pass; final-only
  readiness evidence remains reported as experimental warnings.
