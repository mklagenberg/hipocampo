# Change Set 0134 — V3 release marker reconciliation

## Problem

V3.0.0 and skill 2.0.0 were published on 2026-10-08, but the public source at
that exact tag still labels the methodology `prepared-unreleased`. The changelog,
README, upgrade guide and skill instructions also say publication is pending.
That contradiction caused a Claude invitation to stop before installing the
already-published package. The tag's contents cannot be corrected without
rewriting a published release.

## Proposed change and acceptance criteria

- Preserve the published v3.0.0 tag and all of its bytes as historical evidence.
- Prepare a PATCH follow-up: methodology 3.0.1 and skill package 2.0.1, retaining
  the V3.0.0 baseline and `^3.0.0` vault compatibility range.
- Reconcile current publication language to the verified v3.0.0 release, while
  retaining separate gates for vault migration, restoration/LTE, installation
  consent, authorization, privacy/scope and host runtime capability.
- Correct the current `SPEC.md` version/status projection and active V3 contract
  page headers; leave historical Decision Records, Change Sets and review
  snapshots intact.
- Reconcile taxonomy and vocabulary headings that described V3.0.0 concepts as
  unreleased; distinguish their published V3 status from their exclusion from
  the legacy V2.2.0 contract. Synchronize scaffold activation instructions to
  use the manifest-declared skill package version.
- Implement accepted Decision 0053’s “immutable release tag and lock” as a
  GitHub Release that reports `immutable: true`, with the tag resolving to its
  target commit and all locked package hashes verified. This maps the accepted
  integrity requirement to GitHub’s immutable release control; it does not
  relax or replace Decision 0053. See [GitHub immutable releases](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases).
- Make skill provenance instructions resolve the published versioned release
  and tag to the exact commit, then verify all locked package hashes. Treat
  `COMPATIBILITY.yaml:methodology.release_state` as the preparation state of
  that source snapshot, not current publication proof; an independently
  verified release object and matching tag target are authoritative. A
  immutable GitHub Release (`immutable: true`), confirm its tag resolves to the
  exact release target, pin that commit and verify package hashes. Keep the
  source-snapshot marker distinct from external publication proof. Explain why
  `source_commit: null` is not a substitute for external provenance and is not
  itself a contradiction.
- Recompute the skill 2.0.1 package lock and keep the package/compatibility
  versions synchronized.
- Require fresh primary AI semantic review, an independent challenge and human
  approval bound to the new package fingerprint; do not reuse 2.0.0 approvals.
- Run the declared structural, documentation, package, contract, Change Set and
  conformance validators; do not claim v3.0.1 is published before the operator
  creates its tag and GitHub Release together after main integration.

## Alternatives, risks and recovery

Editing tag v3.0.0 would rewrite a published release and make prior package
hash evidence ambiguous, so it is rejected. Changing only the README would
leave the failing markers in the compatibility contract and skill package.
Removing all authorization, migration or capability gates would exceed the
requested correction and weaken the V3 boundary. The change is recoverable by
reverting this patch; v3.0.0 remains available at its existing tag.

## Compatibility and migration

Operational, PATCH-class correction under Decision 0023: no schema, V3.0.0
contract, or vault compatibility range changes. Existing vaults require no
action for this marker correction; their V2-to-V3 migration remains separately
governed and explicitly approved per vault.

## Status

Proposed. The v3.0.1 publication, merge and human review remain separate gates.
