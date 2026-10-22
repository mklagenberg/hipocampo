# Change Set 0138 — V3 minor vault adoption guidance

## Problem and evidence

The four existing V3 vault manifests declare `^3.0.0` and retain an exact
V3.0.0 `verified_against` source. The 3.1.0 candidate preserves the V3.0.0
Record/Chunk/CRUD baseline. A compatible range does not, by itself, update
historical verification or prove a host's permissions and operations. Existing
vault validation scripts also pin the V3.0.0 methodology bytes and therefore
cannot be repurposed as validators of the 3.1.0 source.

## Decision and scope

Document a no-migration adoption procedure for compatible V3.0.0 vaults.
Retain manifest compatibility, verified source, historical links, Records and
instance restrictions. Verify each remote manifest and the candidate tuple;
record operation-level capability and authority separately. This is an
operational clarification of the existing compatibility contract and requires
no new vault schema or Decision Record. The four named remote results belong
in the private management evaluation, not this public Change Set.

## Acceptance

- The procedure distinguishes version-range compatibility, historical
  verification, source-age WARNING, host capability and authorization.
- All four remote manifest blobs pass the canonical compatibility validator
  under the explicit experimental 3.1.0 candidate; blob identity is checked.
- A later direct-target ingress implementation is checked against legacy
  manifests and existing Collection registries; inability to assemble a
  verified vault ID is an operation-level gap, not a reason to rewrite the
  vault or declare its version range incompatible.
- No vault Record, manifest, ACL, local cache or installed client is changed
  merely to make the range pass.
- Repository documentation and Change Set validation pass. External host
  operation tests and final release review keep their own gates.

## Recovery

Revert this documentation Change Set if its guidance is rejected. No vault
rollback is required because this Change Set performs no vault mutation.
