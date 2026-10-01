# 0114 — AI-first V3 skill conformance review

**Status:** Accepted

**Date:** 2026-10-01

## Context

The V3 skill is a client-side operational package. Package integrity and
declared compatibility can be checked deterministically, but those checks do
not establish that an agent interprets V3 authority, privacy, staleness,
migration and compatibility rules correctly when operating the skill.

The V3 engine semantic suite already records reviewed dispositions, but it
does not exercise the V3 skill as an operator. The current canonical skill
package is version 1.3.0 and declares methodology compatibility `^2.1.0`; no
V3-compatible skill package is available yet.

## Decision

Before a V3 skill release is approved:

1. deterministic synthetic cases validate the skill/methodology/vault tuple
   and fail-closed outcomes;
2. an AI reviewer assesses every semantic skill-conformance case against the
   exact package and cited V3 contracts;
3. an AI challenge pass reviews the first AI assessment for omissions,
   unsupported assumptions and boundary violations, records the challenged
   review identifier, and runs in a separate AI review session;
4. a human reviews both AI assessments and records a later, timestamped final
   decision linked to the two review identifiers.

The deterministic validator may establish case coverage, package identity,
provenance and review order. It must not claim that semantic truth is
deterministic. An AI pass cannot approve its own release, replace human review,
or turn an unreviewed or incompatible skill package into a compatible one.
Any package change invalidates the AI review until it is repeated against the
new package-lock fingerprint.

The gate is about the skill version and its methodology/vault compatibility.
It does not require a named AI host and uses synthetic cases only. Adapter-
specific claims remain separately bounded by the adapter's own evidence.

## Rationale

This places an explicit AI review stage before human review while preserving
the constitutional distinction between deterministic proof and semantic
interpretation. Binding the review to the package lock prevents a review of
one skill version from being reused for another. Synthetic cases avoid using
real vault content as test data.

## Consequences

- `docs/v3-skill-conformance-gate.md` defines the stages and limits.
- `docs/v3-skill-conformance-cases.yaml` defines deterministic and semantic
  synthetic cases.
- `scripts/validate_v3_skill_conformance.py` validates the workflow envelope
  and release prerequisites.
- CI validates the gate definition; the release checklist requires complete
  AI and human review for the exact V3 package.
- The current skill package is not release-ready for V3 because its declared
  methodology compatibility remains `^2.1.0`.

## Discarded alternatives

- **Treat package hashes and compatibility fixtures as proof of skill
  behavior:** rejected because they establish integrity and tuple state, not
  semantic operation.
- **Let an AI review approve the V3 skill release:** rejected because semantic
  review remains subject to human decision and risk acceptance.
- **Require one named AI host:** rejected because host choice is not the
  methodology compatibility contract and would narrow portability without
  evidence.

## Validation

- Run `python scripts/validate_v3_skill_conformance.py --root . --mode
  workflow` in CI.
- Run the `release` mode only after a V3-compatible package and its AI review
  evidence exist; it must remain blocked otherwise.

## Approval

The operator explicitly requested this AI-first, human-final release gate and
authorized implementation, validation and correction on 2026-10-01.
