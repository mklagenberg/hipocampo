# Change Set 0130 — Fingerprinted legacy and canonical recovery

## Problem

Reviewed legacy lacks an evidenced effective V2.2 version, and canonical CRUD
cannot restore a migrated Record to its exact original bytes. Version
relabeling and direct-file restoration would violate provenance or CRUD.

## Proposed change

Implement the source contract and internal ticket-bound recovery defined in
Decision 0118. Preserve the source body and all parsed legacy fields. Keep
every existing item approval gate and the reviewed skill package unchanged.

## Acceptance criteria

- The direct route requires explicit source evidence and decision references;
  unknown version remains unknown and malformed headers are held.
- Canonical migration validates exact body and legacy metadata before write.
- Immutable local tickets are created before canonical persistence and bind
  source, target, proposal, vault/entity/branch and originating commit.
- Canonical recovery validates exact ticket approval and accepted review,
  preserves unrelated changes, refuses target drift or later versions and
  restores byte-exact CRLF, Unicode, fields and relations in synthetic Git.
- Interrupted effects are reconciled in a new process; source-present is
  reported without claiming a write. Recovery and migrate stay outside MCP.
- No real Record write, source-version promotion or privacy assertion is
  caused by preparing pilot proposals.
- Queue scanning uses vault-relative excluded-directory checks so a legitimate
  operational copy nested inside its own Git administration is not invisible.

## Compatibility and recovery

Normative extension of the scoped unreleased candidate, no released SemVer or
installation change. Existing V2 route retains its behavior. Rollback is
restricted to the exact unchanged migration result and approved ticket;
subsequent edits require a separately reviewed forward recovery.

## Risks and limits

Ticket hashes establish integrity, not semantic truth or authenticated human
approval. The current adapter implements one-file atomic replacement, not a
whole-vault transaction. A surviving write lock requires its own diagnosis.
Synthetic success is not a real-vault pilot or recovery result.

## Status

Scoped direction authorized; implementation completed in the local experiment.
The new regression validator passed 41 synthetic checks with actual Git. The
engine suite passed 25 deterministic commands and its semantic revalidation
command. Package validation passed without changing the released or candidate
skill package; two recorded release gates remain. Scope and Change Set
validators are required again against the checkpointed diff.
The implemented contract and four concrete pilot sheets remain reviewable
before any real migration. Accepted Change Sets 0128 and 0129 stay frozen.
