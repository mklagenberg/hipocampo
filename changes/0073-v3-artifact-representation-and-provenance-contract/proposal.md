# Change Set 0073 — V3 Artifact representation and provenance

## Intent

Implement the accepted V3 boundary for multimodal Artifacts: retain the
Artifact as a separate versioned object, require a material representation when
its content is semantically necessary, preserve layered provenance, and make
accessibility and divergence explicit.

## Scope

This Change Set defines the unreleased candidate contract and exercises it with
local in-memory fixtures. It does not copy source material, fetch external
objects, execute an Artifact, add S3/Google Drive/OneDrive connectors, migrate
a vault, or activate V3 for existing v2 instances.

## Implementation

- `docs/v3-artifact-contract.md` defines the Artifact envelope, representation,
  provenance, privacy, accessibility, and reconstruction rules;
- `scripts/v3_artifact_engine.py` provides bounded in-memory primitives for
  hashes, validation, version updates, divergence, and reconstruction;
- `scripts/validate_v3_artifacts.py` exercises positive, negative, limited, and
  fail-closed paths;
- `docs/v3-artifact-fixtures.yaml` records ten representative cases;
- the specification and verification-boundary registry point to the candidate
  without activating it.

## Semantic and privacy boundary

The validator proves only structural contract behavior. It does not decide
whether a representation is semantically sufficient, whether an Artifact is
truthful or authorized, or whether an external reference can be accessed. The
Record representation is sanitized in the fixture; no Liferay source body or
private Artifact is copied into the public methodology repository.

## Compatibility, rollback, and publication

V2 documents remain readable. Reverting this Change Set removes the candidate
contract and tooling without deleting historical decisions or changing a
vault. A future V3 release requires a separate migration plan, connector
policy, skill compatibility review, release gate, and human publication action.
