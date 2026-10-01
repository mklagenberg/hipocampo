# 0115 — Isolated V3 skill candidate

**Status:** Proposed

**Date:** 2026-10-01

## Context

The released skill package is version 1.3.0 and supports the active V2.2
methodology contract. V3.0.0 remains an unreleased candidate. Replacing the
published package in `skill/` or changing the active `COMPATIBILITY.yaml`
tuple before V3 release would make candidate guidance look current and would
break the existing compatibility contract.

## Decision

Keep the released V2 skill package and active methodology tuple unchanged.
Develop the V3 skill as a complete, separately locked package under
`candidates/skill-v3/`, with candidate package version `2.0.0-rc.1`, method
compatibility `^3.0.0`, and explicit unreleased status. Run the V3 skill
conformance gate against that exact package and package-lock fingerprint.

The candidate is not installable or authorized for real-vault operations.
Promotion into the released `skill/` package requires the methodology's V3
release/compatibility gates, a passing primary AI semantic review, a passing
challenge from a separate AI session, human approval, and a separate release
decision. Tool or host adapters remain outside the methodology/skill/vault
version tuple; runtime capability claims require their own evidence.

## Rationale

Separate packaging keeps the released V2 contract intact while allowing a
complete skill candidate to be evaluated against raw V3.0.0. It also makes the
review fingerprint unambiguous and prevents an unreleased candidate from being
installed by consumers following the current manifest.

## Discarded alternatives

- **Replace the active package in `skill/` now:** rejected because V3 is not
  released and the active compatibility contract remains V2.2.
- **Declare the active package compatible with both V2 and V3 before review:**
  rejected because the current deterministic compatibility contract does not
  establish that claim and no semantic review existed when this choice arose.
- **Review only an overlay or prose delta:** rejected because it would not
  provide a complete package whose installed behavior and hashes can be
  evaluated as one unit.

## Constitutional and contract impact

Compatible with `FF-CON-0001:2.7`–`2.11` and section 4. It separates
deterministic integrity, semantic interpretation and human authority; preserves
uncertainty and least privilege; and keeps the change reversible and traceable.
It does not amend V3 CRUD, compatibility, migration or LTE contracts and does
not authorize vault access or activation.

## Validation

Run the V3 conformance validator against `candidates/skill-v3/`, verify every
package-lock entry and its fingerprint, run the skill documentation and
repository validators, and require release mode to remain blocked until all
gates pass. A text-based semantic review does not prove runtime behavior,
authorization enforcement or real-vault readiness.

## Approval

Proposed with implementation for human review in the associated Change Set.
