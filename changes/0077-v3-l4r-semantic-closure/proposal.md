# Change Set 0077 — V3 L4R semantic closure

## Problem

The selective Package candidate passed its deterministic fixtures but still
represented authority as physical active/inactive state, lacked a durable
Package assembly identity, and could not prove bilateral circulation through
local copies when the origin vault was unavailable. It also did not preserve a
clear REM boundary for received material.

## Proposed contract

1. Resolve authority logically by entity, scope, origin and ordered succession;
   access is an operation context, not a persisted authority state.
2. Bind Package authority to the generating vault and derive a deterministic
   Package identity and fingerprint from the assembly selection and context.
3. Require contextual conciliation sources and preserve selected Chunks and
   Artifacts in the Package envelope.
4. Create a destination-local `new`/`pending_rem` representation on receipt;
   it is not curated or current knowledge until REM and semantic validation.
5. Record paired `packages-sent` and `packages-received` events locally.
6. Audit the graph backward and forward with orthogonal coverage, integrity,
   circulation and governance results.
7. Alert on missing bilateral counterparts, but fail closed on deterministic
   identity, fingerprint, selection, authorization or privacy mismatches.

## Discarded alternatives

- duplicating active/inactive authority state in every local copy;
- blocking all local use when an origin vault is inaccessible;
- using a centralized ledger as a universal source of truth;
- forcing semantic conciliation or curation through deterministic rules;
- silently deleting revoked Packages and their circulation history.

## Risks and compatibility

This is an unreleased, normative V3 candidate. It does not activate V3 for v2
instances and does not perform migration, remote transport, connector work,
publication, or tag creation. The principal risk is over-reading deterministic
traceability as semantic correctness; the contract explicitly preserves the
human/agent semantic boundary.

## Acceptance criteria

- logical authority rejects persisted active/inactive states and represents
  inaccessible origins as partial frontiers;
- Package identity changes when selection or assembly context changes;
- generator vault, source authority, destination and fingerprint are present;
- received material is `new` and `pending_rem`;
- sent and received ledgers pair by delivery, Package version and fingerprint;
- backward and forward audit identifies complete, partial, alert and mismatch
  states;
- anonymized personal, company and client entity fixtures cover the composed chain;
- all declared repository and V3 validators pass after correction.
