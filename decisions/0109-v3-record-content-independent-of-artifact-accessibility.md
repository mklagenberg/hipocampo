# 0109 — V3 Record content independent of Artifact accessibility

**Status:** Accepted for the unreleased V3 candidate

**Date:** 2026-09-15

**Parent:** 0073-v3-artifact-representation-and-provenance-contract

## Context

The V3 model separates a Record from an Artifact. The Record is the governed,
content-bearing Markdown unit; the Artifact is the referenced informational
object that supplies origin, representation context, version and provenance.
Most referenced Artifacts may be unavailable to the consumer, especially when
they remain in an external, private or otherwise inaccessible location.

The existing Artifact contract correctly rejects a pointer-only Record, but its
conditional representation rule and its use of reconstruction language leave
an unsafe ambiguity: a consumer could treat Artifact availability as a
precondition for reading the Record. The Search runtime currently makes that
ambiguity observable by treating an inaccessible source as a reason to return
`L0`.

## Decision

For the unreleased V3 candidate:

1. A Record is always a content-bearing unit. When it represents or is derived
   from an Artifact, its persisted body must contain a human-readable prose
   representation of the represented content. A reference alone is never a
   valid substitute for the Record's content.
2. Artifact accessibility and Record-content accessibility are independent
   dimensions. An Artifact may be `unavailable` or `restricted` while the
   authorized Record remains readable and disclosable at the level permitted
   by the Record's own privacy, authority, epistemic, state and disclosure
   gates.
3. An inaccessible Artifact produces an explicit provenance, verification,
   freshness or reconstruction limitation. It does not, by itself, force the
   Record to `L0`, block its prose, or authorize a consumer to reconstruct the
   Artifact in order to display the Record.
4. Artifact reconstruction is an optional bounded operation for integrity,
   version, audit or revalidation checks only. It is never a prerequisite for
   reading, searching, rendering or disclosing the Record's persisted prose.
5. Structured metadata, manifests or other Artifact descriptors may accompany
   the prose representation, but they cannot replace it as the Record's
   content-bearing representation.
6. A changed, divergent, missing or inaccessible Artifact remains explicit and
   may route the Record to staleness, provenance or semantic review. It does
   not silently rewrite, erase or invalidate the Record's persisted content.
7. If the Record itself is inaccessible, privacy-blocked or fails its own
   governing read contract, the ordinary Record and disclosure gates still
   apply. This is distinct from an inaccessible referenced Artifact.

## Rationale

This preserves the intended Record–Artifact separation without making the
Record a pointer or an implicit retrieval instruction. The Record carries the
knowledge representation that the system governs; the Artifact reference
preserves provenance and enables later verification when access exists.

The rule also matches the privacy-first boundary: inaccessible external
material is not fetched or reconstructed by inference, while already governed
Record content is not unnecessarily hidden merely because its original
representation cannot be opened. Limitations remain visible, and a request
for currentness, exact version verification or Artifact-dependent analysis can
still be limited or routed for review.

## Discarded alternatives

- **Treat Artifact availability as a prerequisite for Record disclosure:**
  rejected because it makes the Record a pointer, over-blocks the normal case
  and confuses provenance verification with content availability.
- **Reconstruct the Artifact whenever the Record is read:** rejected because
  reading must not depend on unavailable external material and reconstruction
  may exceed the authorized access boundary.
- **Allow a reference-only Record:** rejected because it loses the governed
  content whenever the Artifact is unavailable.
- **Store the full Artifact bytes in every Record:** rejected because it
  increases duplication, exposure, coupling, cost and divergence risk.
- **Silently ignore Artifact unavailability:** rejected because provenance,
  freshness and verification limitations must remain visible.

## Consequences

- Search and progressive disclosure read the Record and its Chunks as the
  content-bearing surface.
- Artifact availability must be represented separately from Record read
  availability in contracts, fixtures, validators and runtime fields.
- Existing Artifact reconstruction tests remain valid only as bounded
  provenance or audit tests; they must not imply a content-recovery path.
- The inaccessible-Artifact semantic case must preserve Record prose while
  exposing its limitation; a separate inaccessible-Record case must cover the
  actual blocking behavior.
- `DEC-0024`, `WRK-0028`, Decision 0073, the V3 Artifact contract and the
  Search Change Sets require synchronized follow-up clarification.

## Boundaries

This Decision Record applies only to the unreleased V3 candidate. It does not
activate V3, alter the released v2.2.0 specification, read real vault caches,
introduce external connectors, authorize MCP access, migrate content or permit
remote writes. Adoption in the deliverable requires a follow-up normative
Change Set with contract, taxonomy/compatibility review where applicable,
fixtures, validators, runtime changes and human review.

## Approval

Accepted by the project operator on 2026-09-15 as the normative V3
clarification for the Record–Artifact and Search boundaries.
