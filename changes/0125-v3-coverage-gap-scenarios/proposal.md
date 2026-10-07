# Change Set 0125 — V3 cross-engine coverage-gap scenarios

## Problem

The integrated V3 suite executes each engine validator and checks that
deterministic cases have bindings. It did not exercise several cross-engine
failure sequences identified during the final review: authorization revoked
between candidate discovery and CRUD Read, a restricted Chunk inside an
otherwise readable Record, a repeated destination acceptance, and an
interrupted migration preflight. The suite also lacked a mutation check for
unknown or misdirected scenario bindings and a synthetic case for an
instructions-only skill host without the required capability.

The review also found that the V3 skill changelog entry said six primary
semantic cases although the accepted review covers seven.

## Proposed contract

Add six deterministic synthetic scenarios and three semantic assessment
scenarios in a supplemental cross-engine suite. Execute each deterministic
scenario through its declared handler and assertion identifier. Mutation
checks must reject unknown case IDs, unknown assertion IDs, and a wrong runner
or handler.

For the existing 63 engine bindings, record the exact command string beside
`command_index`, validate the canonical assertion ID for each case, and reject
mutations that substitute an unknown assertion or point the index at a
different command. The integrated suite executes the declared engine command
set and keeps the existing cases labeled as assigned to passing commands,
because the legacy validators do not emit an individual assertion transcript.

Search must exclude a restricted Chunk from relevance calculation, selected
Chunk output, and L4 expansion, even when its parent Record is readable.
Migration preflight must fail closed for any execution state other than
`not_started`; the existing migration component is a preflight evaluator and
does not implement rollback or resume.

Semantic assessments preserve scope, epistemic state, and source lineage. They
are recorded as AI assessments with an adversarial self-challenge and remain
pending human confirmation. The new cases supplement the existing canonical
33-case semantic baseline; they do not rewrite that baseline or claim
deterministic semantic truth.

The supplemental runner is integrated into the 12-engine suite. Its result
distinguishes the six newly executed scenario assertions from the 63 existing
cases that remain assigned to engine commands.

## Alternatives considered

1. Fold the scenarios into the historical semantic baseline — rejected because
   this would rewrite its versioned 28+5 review result instead of recording an
   additive delta.
2. Implement migration execution, rollback, and resume here — rejected because
   no such runtime capability exists in the current candidate, and adding it
   would exceed a test-coverage change.
3. Claim that text-based skill checks prove host authorization — rejected
   because the candidate is instructions-only and no runtime host adapter is
   available in this task.

## Risks and recovery

The authorization-revocation case uses a synthetic CRUD adapter that revokes
between the Search snapshot and the CRUD read. The skill capability case
checks candidate instructions and a synthetic unavailable-capability input;
it does not prove a real host will enforce the stop. The interrupted-migration
case proves preflight blocks an already-started state; rollback and resume
remain untested until an execution/recovery engine exists. The semantic
assessments are not independently reviewed and require human confirmation.

The Change Set is reversible by reverting its branch. It does not alter the
published V2 package, active compatibility tuple, real vaults, or release
state.

## Acceptance criteria

- all six deterministic cases execute individually and fail if their case,
  assertion, runner, or handler binding is mutated;
- the 63 existing case IDs retain canonical assertion IDs and exact command
  targets, and mutations of an assertion ID or command index fail;
- revoked authorization returns no body, Chunk, or expanded content and causes
  no CRUD mutation;
- restricted Chunk content affects neither ranking nor L3/L4 disclosure;
- a lost transfer acknowledgment followed by replay creates one Record and one
  CRUD event;
- interrupted migration state is blocked without changing the source fixture;
- unavailable skill capability and missing authorization remain unavailable,
  with no read or write implied;
- all three semantic assessments include rationale, countercheck, evidence,
  Constitution and Decision Record references, and remain human-pending;
- integrated engines, supplemental scenarios, skill workflow, package, docs,
  contracts, repository structure, and Change Set validation pass;
- release mode remains blocked until its existing release gates are met.

## Compatibility and migration

No released behavior or compatibility tuple changes. The restricted-Chunk
filter and interrupted-state block implement existing V3 candidate boundaries.
No migration or runtime host adapter is introduced.

## Status

Implemented on `work/v3-coverage-gap-scenarios`. Deterministic and structural
validation passed. The three semantic assessments remain human-pending; no PR,
merge, tag, release, skill installation, or V3 activation is claimed.
