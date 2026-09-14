# Change Set 0103 — V3 canonical CRUD mutation boundary

## Intent

Make the CRUD gateway the sole Record mutation boundary and apply the complete
V3 governed CRUD use-case suite through a logical MCP adapter.

## Scope

Separate semantic Record review from deterministic structural commit; add the
in-memory CRUD gateway and MCP adapter; harden Artifact divergence, processed
ingress, received-package promotion, migration version preflight and bilateral
fingerprint audit; route the legacy deterministic Record-document normalizer
through the CRUD module; and add 18 sanitized use cases.

This Change Set does not migrate a vault, alter the four local vault caches,
copy an Artifact, connect S3/Google Drive/OneDrive, publish V3 or activate V3
behavior for existing V2.2 instances.

## Acceptance criteria

- every V3 Record mutation is committed by the canonical CRUD gateway;
- semantic review completeness and deterministic structure are separate gates;
- the logical MCP adapter exposes only CRUD operations;
- all 18 use cases pass, including negative bypass cases;
- existing Artifact, ingress, transfer, migration and audit validators pass;
- V2.2 remains the active published line and V3 remains unreleased;
- no real vault, cache, remote object or external connector is changed.

## Recovery

Revert the candidate branch commit. The implementation is fixture-backed and
in-memory; no real vault content or external Artifact is affected.
