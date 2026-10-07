# 0119 — V3 release contract and stable skill packaging

**Status:** Proposed; implementation preparation authorized, final acceptance pending

**Date:** 2026-10-07

## Context

V3 engines and reviewed candidate contracts coexist with a V2.2 root
specification, a V2 skill and scaffold, and validators pinned to old versions.
Three explicitly accepted local pilot conversions passed fresh reload and
preservation checks. This does not establish complete vault adoption or
universal host enforcement. The operator requested release closure before
migrating the remaining knowledge.

## Decision

Prepare methodology 3.0.0 and canonical skill 2.0.0 for separate human release
approval. Make SPEC the V3 authority, retain V2 normative text as an immutable
historical snapshot and preserve section anchors as V3 routing surfaces.
Preserve the separately reviewed 2.0.0-rc.1 candidate unchanged. A new package
requires fresh primary AI review, independent AI challenge and human approval.

The release scope is the portable methodology and instructions, deterministic
local engines, and explicitly bounded local adapter. Other host adapters are
instructions-only unless their operation-specific capability is verified.
Installation, ACL changes, bulk migration, remote transfer and publication are
excluded. New-vault scaffolding creates governance/proposal structure; only
canonical CRUD can persist a Record. An illustration is not an active Record.

Declaration of a release target is not proof that its tag exists. Preserve
unreleased/prepared state until publication is independently checked. Release
preparation validation must distinguish package readiness, human approval,
remote integration, and actual tag/release existence. It cannot turn any
unknown or blocked state green by substituting metadata.

## Rationale

Separating methodology publication from existing-vault adoption allows a
coherent major contract without silently asserting that legacy content is
compatible. Existing V2 operation remains attached to its immutable release.

## Discarded alternatives

- Bump only version numbers: leaves contradictory schemas and bootstrap paths.
- Edit the approved candidate in place: invalidates its historical review.
- Declare universal runtime support from three local pilots: unsupported.
- Infer final human approval from the request to prepare: violates AI-first review.

## Impact and compatibility

Change Set 0132. MAJOR: V2 tuples require governed migration before V3 writes.
The V3.0.0 baseline must remain supported by later V3 minor/patch packages.
Privacy, uncertainty, provenance, canonical CRUD, exact-ticket recovery and
per-item approvals remain mandatory. No constitutional exception is proposed.

## Validation

Repository, Change Set differential, package, tuple, scaffold/proposal,
negative-fixture and V3 engine checks; AI semantic review and independent
challenge bound to the final package hash; human review of the frozen content.
An evidence-only commit follows the content commit. No agent-created tag.

## Approval

Preparation is authorized by the operator's 2026-10-07 request to execute the
ForgeFlow loop through release preparation. This record remains proposed until
the exact final content, package fingerprint, reviews and residual risks are
presented and explicitly accepted. Merge remains human-reviewed.
