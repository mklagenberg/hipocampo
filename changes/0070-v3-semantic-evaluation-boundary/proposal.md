# Change Set 0070 — V3 semantic evaluation boundary

## Intent

Create the first executable evaluation surface for the planned V3 work. The
surface makes the boundary between deterministic validation and semantic or
human review explicit, and provides sanitized fixtures that can be exercised
against an authorized local corpus without copying that corpus into the
methodology repository.

## Current contract

The current normative specification is v2.1.1. Its deterministic validators
cover repository structure, contracts, compatibility, package integrity, and
other declared boundaries, but they do not establish semantic truth or a V3
Record/Chunk contract. The V3 planning decisions therefore remain management
artifacts until a later normative Change Set defines their fields and
migration.

## Proposed operational contract

1. A semantic fixture declares an input shape, the expected epistemic and
   maturity guard, the required provenance behavior, and the negative behavior
   that must not occur.
2. The fixture validator checks only schema completeness, unique identifiers,
   allowed result vocabulary, and the presence of declared human-review
   boundaries. It does not decide whether a claim is true.
3. A corpus exercise may reference local source paths and record sanitized
   findings, hashes, and limitations, but must not copy raw or sensitive source
   content into this repository.
4. A passing fixture validator is evidence that the evaluation package is
   structurally usable; semantic adequacy remains a human or agent-reviewed
   result and is never inferred from the validator's green status.

## Scope

This Change Set adds the reusable fixture format, its structural validator,
and a documentation of the verification boundary. It does not change the
frontmatter schema, implement CRUD, change the REM mechanism, introduce a
projection layer, migrate v2 instances, or publish a V3 release.

## Discarded alternatives

- Treating semantic cases as deterministic pass/fail rules — rejected because
  epistemic classification, conflict resolution, and adequacy require context
  and can be wrong while remaining structurally valid.
- Copying the Liferay knowledge base into the public methodology repository —
  rejected by the privacy, provenance, and repository-boundary rules.
- Waiting for the complete V3 contract before exercising any semantic cases —
  rejected because the evaluation boundary is itself useful preparation and
  can expose unresolved contract questions early.

## Risks and limits

The fixture language can be complete while a semantic conclusion is wrong.
The local-corpus exercise cannot prove remote source reachability, freshness,
authorization, or production enforcement. The exercise records these limits
explicitly and keeps the source read-only.

## Acceptance criteria

- the fixture validator passes positive and negative fixture sets;
- every fixture declares a semantic/human boundary;
- no fixture stores raw corpus content or credentials;
- the Liferay exercise is stored outside the public deliverable as sanitized
  management evidence;
- the Change Set and validation boundary are linked and reviewable;
- V3 remains clearly marked as unreleased and not yet a normative contract.

## Compatibility and recovery

The change is operational and has no effect on existing Hipocampo instances.
Removing the validator and fixture documentation restores the prior evaluation
surface without changing any instance or deleting any historical evidence.

