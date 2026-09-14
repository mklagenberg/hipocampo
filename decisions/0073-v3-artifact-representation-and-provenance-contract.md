# 0073 — V3 Artifact representation and provenance contract

**Status:** Accepted for the unreleased V3 contract

**Date:** 2026-09-05

**Parent:** 0072-v3-record-chunk-crud-contract

## Context

The V3 CRUD contract keeps Artifacts separate from Records, but a Record can
depend on an image, document, dataset, script, spreadsheet, or other material
whose contribution cannot be understood from a reference alone. The contract
therefore needs a bounded representation rule that preserves context without
copying the original bytes or silently changing the Record when an Artifact is
replaced.

## Decision

An Artifact reference in a Record identifies `artifact_id`, semantic `role`,
`version`, non-secret `reference`, `source_hash` when available, and an
explicit accessibility state. The hash identifies the referenced version; it
does not establish truth, quality, authorization, or availability.

When the Artifact is semantically necessary to understand the Record, the
Record stores a material representation with a declared kind (`summary`,
`excerpt`, `transcription`, `preview`, `structured_description`, or
`manifest`), the represented content, the represented Artifact version/hash,
and its generation or capture time. A reference alone is invalid for this
case. The representation is not required to contain the Artifact bytes in
full.

The representation has its own visibility and must not be less restrictive
than the Record or the represented Artifact. An unavailable or restricted
Artifact remains explicit; its last permitted representation may be retained
with that limitation and cannot be treated as proof that the current Artifact
is available.

Updating an Artifact creates or selects a new Artifact version and marks the
Record link as divergent/review-required. It does not rewrite the Record's
representation or version automatically. Reconstruction of a Record's used
Artifact must resolve the exact linked version and fail closed when that
version is unavailable or its hash diverges.

External destinations are represented only as provider-agnostic references in
this release candidate. S3, Google Drive, OneDrive, and other connectors are
future adapters; a destination reference never grants access or replaces
provenance, integrity, privacy, or availability checks.

## Consequences

- Records remain understandable when an Artifact is temporarily unavailable;
- large or sensitive originals are not duplicated into the Record by default;
- version drift is visible and cannot silently rewrite governed knowledge;
- a hash and a reference remain evidence of identity, not of truth;
- external storage can be added later without making one provider normative;
- consumers must preserve the representation's limitations and access scope;
- the implementation must retain enough metadata to reconstruct the version
  that the Record actually used.

## Rationale

This is the smallest contract that satisfies `DEC-0023` and `DEC-0024` while
preserving the Record–Chunk boundary from `DEC-0026`. It makes semantic
dependence testable, treats provenance as layered evidence, and keeps the
external transport question outside the V3 LTE.

## Discarded alternatives

- **Store only a reference or URI:** rejected because the Record loses the
  Artifact's semantic contribution when the source is unavailable.
- **Copy the full Artifact into every Record:** rejected because it increases
  exposure, cost, coupling, and divergence risk.
- **Refresh the Record whenever the Artifact changes:** rejected because an
  Artifact version change is not authorization to rewrite governed knowledge.
- **Treat a hash as proof of truth or permission:** rejected because hashes
  identify bytes, not authority, quality, or access.
- **Implement provider connectors in this Change Set:** rejected because
  connector policy and external authorization are future boundaries.

## Approval

Accepted by the operator on 2026-09-05 as the normative V3 candidate detail
for `WRK-0028`.
