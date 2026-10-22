# Change Set 0136 — V3 remote ingress and profile write eligibility

**Class:** normative · **SemVer:** minor · **Status:** proposed

## Intent

Clarify direct-target ingress without a personal anchor, distinguish profile
eligibility from technical capability and authorization, establish scoped
representative grants for `entity` writes, and require runtime-independent
canonical CRUD checks with atomic idempotency receipts. Reconcile prior
decisions prospectively without editing their historical text.

## Decision and scope

See [Decision 0121](../../decisions/0121-v3-remote-ingress-and-profile-write-eligibility.md).
The public V3 Record schema remains compatible with stable 3.0.0. New manifest
fields apply to new or explicitly adopted vaults. Legacy manifests retain their
prior versioned authorization and CRUD rules; no profile or new eligibility is
inferred. This preserves existing conformance and supports a MINOR
classification under Decision 0023, targeting the unpublished 3.1.0 release.
No vault migration is required for reading or preserving valid legacy writes.
Using the new profile policy or recording representative grants on legacy
manifests requires separately authorized adoption. If evidence shows any
previously conforming instance becomes invalid, reclassify before release.
For authorized legacy reads, the existing vault identifier may be recovered
from an authenticated Collection registry at the same remote HEAD as the
manifest and access proof. A mismatch or missing proof blocks that route;
this recovery does not silently adopt a profile or change write eligibility.

## Review requirements

- Verify parity across SPEC, compatibility metadata, onboarding, upgrade,
  migration, release gates, taxonomy and vocabulary.
- Exercise no-anchor, least-privilege, entity grant, revocation and route parity
  cases in deterministic validation and semantic review.
- Keep remote observation and publication evidence distinct from local checks.
- Exercise same-HEAD legacy identity recovery, stale registry, wrong entity,
  wrong account and missing verifier as positive and negative cases.
- Verify key-hash lookup, request/context mismatch rejection, exact result-state
  replay, drift reporting, different-key non-deduplication and atomic
  Record/receipt commit. Confirm no target commit SHA is stored in its own
  receipt and source identity is required for real persistence.

## Out of scope

ACL changes, real vault Record writes, skill installation, merge, tag, release,
and changes to historical Decision Records. The integration branch and PR
publish only this methodology candidate for human review.
