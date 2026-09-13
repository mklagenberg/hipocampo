# Hipocampo V3 Artifact and representation contract — unreleased candidate

This document defines the Artifact boundary for the unreleased `v3.0.0`/LTE
candidate. It does not activate V3 for existing v2 instances.

## Artifact envelope

```yaml
artifact:
  artifact_id: "art-001"
  role: "supporting-material"
  version: 1
  reference: "non-secret-reference"
  source_kind: "url | conversation | internal | external-storage"
  source_hash: "sha256-of-referenced-version"
  accessibility: "available | unavailable | restricted"
  checked_at: "2026-09-05T12:00:00Z"
  visibility: "internal"
  external_destination:
    provider: "s3 | google-drive | onedrive | other"
    reference: "opaque-provider-reference"
```

`external_destination` is a reference only. It is not a connector, a
credential, an authorization grant, or proof that the object can be fetched.

## Material representation

When `semantic_required: true`, the Record link must carry a representation:

```yaml
artifact_link:
  artifact_id: "art-001"
  role: "evidence"
  version: 1
  source_hash: "sha256-of-referenced-version"
  semantic_required: true
  representation:
    kind: "summary"
    content: "Sanitized minimal representation of the relevant contribution."
    artifact_version: 1
    artifact_hash: "sha256-of-referenced-version"
    generated_at: "2026-09-05T12:00:00Z"
    visibility: "internal"
  limitation: "Original bytes are not stored here."
```

Allowed representation kinds are `summary`, `excerpt`, `transcription`,
`preview`, `structured_description`, and `manifest`. The content must be
present when the Artifact is semantically necessary, but need not reproduce
the full Artifact. The representation must identify the exact Artifact
version/hash it describes and keep a limitation visible when the original is
unavailable, restricted, partial, or externally hosted.

## Provenance and privacy rules

- `artifact_id + version` addresses the Artifact version used by the Record;
- `source_hash`, when present, is calculated over the referenced version and
  is reproducible from that version's bytes or canonical representation;
- hash presence does not prove truth, quality, authority, or permission;
- representation visibility cannot be weaker than the Record or Artifact
  visibility;
- `unavailable` and `restricted` are explicit states, not inferred as
  `available` from a URI or hash;
- an Artifact version change marks divergence/review-required and never
  silently updates the Record or its representation;
- reconstructing the version used by a Record resolves the linked version and
  verifies its hash when a hash is recorded; mismatch or unavailability blocks
  reconstruction;
- provenance retains source reference, capture/generation time, version/hash,
  availability, and known limitations without copying restricted source
  material.

## Validation and migration boundary

`scripts/validate_v3_artifacts.py` exercises the contract with local in-memory
fixtures. It does not fetch external objects, prove authorization, perform
OCR/transcription, migrate a vault, or implement S3/Google Drive/OneDrive
connectors. V2 instances remain readable and require a separate migration
Change Set before any V3 fields are adopted.

See `decisions/0073-v3-artifact-representation-and-provenance-contract.md`,
`decisions/0071-v3-record-state-and-queue-contract.md` and
`decisions/0072-v3-record-chunk-crud-contract.md`.
