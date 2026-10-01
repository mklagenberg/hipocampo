# Change Set 0118 — V3 Search authorized disclosure with unresolved conflict

## Intent

Implement Decision `0112` for `SPD-S-005`: explicitly authorized disclosure
may reach the requested level while preserving unresolved epistemic conflict,
source provenance and the review requirement.

## Scope

Clarify the Search contract and changelog; add the Decision Record, semantic
confirmation, constitutional test basis, fixture, deterministic binding and
sanitized runtime validation. The local read-only engine now exposes operation
status separately from interpretation status and makes unresolved conflict
visible in default prose.

## Authority and compatibility

This Change Set implements candidate Decision `0112` under Constitution
clauses `2.2`, `2.4`, `2.5`, `2.7`, `2.8`, `2.9` and section `4`. It changes
only the unreleased V3 candidate; it does not alter released v2.2.0.
Classification is normative within the candidate; SemVer remains `none` until
release classification.

## Acceptance criteria

- explicit authorization and passing gates permit the requested L4 content;
- conflicting Records and their evidence references remain separate;
- each conflicting result and the overall response preserve
  `interpretation_status: needs_review`;
- operation `status: accepted` is not presented as epistemic acceptance;
- default prose identifies the unresolved interpretation and says no
  conclusion was consolidated;
- sanitized fixtures and the integrated V3 engine suite pass.

## Recovery

Reverting this Change Set removes the candidate clarification and its
executable evidence. Released behavior, real vaults and Record data are
unchanged.
