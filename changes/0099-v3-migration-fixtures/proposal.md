# Change Set 0099 — V3 migration fixture gate

## Intent

Turn the candidate `2.x -> 3.0` migration boundary into a repeatable,
synthetic preflight gate before any real-vault migration is considered.

## Scope

Add sanitized migration fixtures, a deterministic evaluator, and the related
Decision Record and documentation links.

This Change Set does not read or modify real vaults, fetch external artifacts,
transport packages, install a skill, publish a release or activate V3.

## Acceptance criteria

- complete, incomplete, ambiguous, privacy-unknown, rollback-missing,
  approval-missing and unsafe-fallback cases are represented;
- each case has an expected typed outcome;
- the validator checks all cases deterministically;
- the validator is included in the F0 script inventory;
- the V2.2-to-V3 matrix points to the fixture and validator;
- no fixture contains real knowledge, credentials or sensitive content.
