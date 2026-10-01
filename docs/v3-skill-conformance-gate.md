# V3 skill conformance gate

**Status:** required for the unreleased V3 skill release; the current installed
package remains V2-compatible and is not a V3 candidate.

## Purpose

Verify that the canonical skill package guides an agent to operate according
to the frozen V3.0.0 contract and preserves the V3.0.0 baseline in later V3
minor and patch releases. This gate is about the skill and its declared
methodology compatibility; it does not select a required AI host or access a
real vault.

## Review order

1. Run the deterministic cases in `v3-skill-conformance-cases.yaml`.
2. An AI reviewer assesses the exact skill package against every semantic
   scenario and the cited V3 contracts. The AI records dispositions, reasons,
   evidence references, uncertainty and findings in
   `v3-skill-conformance-ai-review.yaml`.
3. A second AI pass challenges the first review for missed cases, unsupported
   assumptions, privacy or authority violations, and confusion between
   deterministic proof and semantic interpretation. It records the identifier
   of the first review, its own review-session identifier, timestamp and
   package fingerprint, and whether the first review should stand or be
   revised. The challenge must come from a separate AI review session.
4. A human reviews the AI assessment and the underlying evidence, resolves
   findings, and records the identifiers of both AI reviews and a later
   timestamp with the final decision. Human approval cannot be inferred from a
   passing script or an AI disposition.

The AI passes are semantic evaluations, not proofs of truth. The deterministic
validator checks case coverage, provenance, package binding and review order;
it does not certify that an AI conclusion is correct. Any change to the skill
package invalidates its semantic review until the AI passes are repeated for
the new package-lock fingerprint.

## Deterministic cases

The suite checks package/methodology/vault compatibility states and fail-closed
behavior, including a V2-compatible skill presented with a V3.0 vault, an
intact V3-compatible tuple, a V2 vault requiring migration, unavailable
sources, and package-integrity failure.

## Semantic cases

The suite asks whether the skill correctly handles V2.2 source diagnosis,
V3.0 operations, authorization scope, multi-vault/entity boundaries, stale or
conflicting source material, and later V3 releases that must preserve the raw
V3.0 contract through an adapter or facade. These cases use synthetic inputs
only. The skill candidate is not exercised against real vault content.

## Commands and gates

- CI runs `python scripts/validate_v3_skill_conformance.py --mode workflow`.
  This validates the suite, deterministic outcomes, the isolated package at
  `candidates/skill-v3/`, its file lock, review-envelope consistency and
  package binding without claiming V3 release readiness.
- The release checklist runs
  `python scripts/validate_v3_skill_conformance.py --mode release` after the
  V3 skill candidate and AI review exist. Release readiness requires a V3
  compatible package, complete AI and AI-challenge coverage for the exact
  package, and recorded human approval.

The V2 skill at `skill/` remains the released package and is unchanged. The
isolated `2.0.0-rc.1` V3 candidate has a primary AI semantic review recorded;
its independent AI challenge and human decision remain pending. It is not
installable and real-vault operation remains blocked until V3.0.0 is released,
the AI challenge passes, and human approval is recorded.
