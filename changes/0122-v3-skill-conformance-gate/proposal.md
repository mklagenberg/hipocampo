# Change Set 0122 — V3 skill conformance gate

## Problem

The current V3 validation flow has deterministic package, documentation,
compatibility and engine checks, plus AI/human semantic review for engine
cases. It has no release gate that evaluates whether the client-side skill
itself guides V3 operations correctly. Package integrity and a compatible
version range do not prove that behavior.

## Current contract

The V3 engine catalog assigns deterministic and semantic boundaries to
methodology engines. `validate_skill_docs.py`,
`validate_skill_package.py` and `validate_compatibility.py` verify text/scaffold
consistency, package hashes and declared version tuples. They do not execute
the skill's V3 operating guidance against V3 scenarios.

## Proposed contract

Add a V3 skill conformance gate with deterministic synthetic compatibility
cases, an AI semantic assessment, an AI challenge pass, and final human
approval. Bind AI evidence to the exact skill package-lock fingerprint. CI
validates the case and evidence envelope; the release checklist requires the
full gate. The deterministic script does not certify semantic conclusions.

The current skill package remains release-blocked for V3 because it declares
`^2.1.0` compatibility and has no V3 semantic case execution. This Change Set
establishes the gate; it does not claim that the V3 skill itself is complete.

## Alternatives considered

1. Treat existing package/compatibility validators as sufficient — rejected;
   they do not evaluate operational interpretation.
2. Add only a manual checklist — rejected; it would not enforce case coverage,
   provenance, package binding or fail-closed deterministic outcomes.
3. Automate semantic approval in a script — rejected; a script can validate
   review evidence and sequence, not semantic truth or human risk acceptance.

## Risks and recovery

The AI review can be wrong or incomplete; the AI challenge and human review
remain explicit. A stale review could be reused after package changes; the
package-lock fingerprint makes that stale state a deterministic blocker.
Reverting the Change Set removes the gate without changing the released V2.2
contract or any vault.

## Acceptance criteria

- synthetic deterministic cases cover compatible, incompatible, inaccessible
  and package-integrity states;
- semantic cases cite the governing V3 contracts and cover authorization,
  migration, multi-vault boundaries, staleness/conflict and the V3.0 baseline;
- the AI review and AI challenge precede the human gate and bind to the exact
  package lock;
- CI validates the gate specification and evidence envelope;
- the release checklist requires the full gate;
- current V2-compatible skill is reported blocked for V3 without claiming
  semantic execution of a V3 skill;
- no real vault is read or modified.

## Compatibility and migration

No released V2.2 behavior changes. The current V3 candidate gains a release
process gate. The future V3 skill package must update its declared
methodology-compatibility range and be reviewed against these cases before
release.
