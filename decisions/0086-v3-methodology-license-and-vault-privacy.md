# 0086 — V3 methodology license and vault privacy boundary

**Status:** Accepted for the unreleased V3 contract

## Context

The legal license of the methodology repository and the privacy contract of a
vault answer different questions. Conflating them could expose vault content
or imply permissions that were never granted.

## Decision

The methodology repository's legal license governs use of the methodology and
its tooling. Knowledge operated inside a vault is governed by that vault's
privacy, access, purpose, circulation and retention contract. V3 does not
invent a generic `content_license` field for every Record, Chunk, Artifact or
Package. Applicable third-party notices remain possible and do not grant
vault access.

## Compatibility note

This is a future V3 boundary. The active v2.1.1 contract is not silently
migrated by this candidate.
## Rationale

Keeping legal licensing at the methodology boundary and privacy at the vault
boundary makes permissions explicit and prevents a generic record-level
license from bypassing destination restrictions.

## Discarded alternatives

- Applying the repository license automatically to vault content.
- Introducing a generic `content_license` as a default record field.
- Treating access to one vault as permission to export another vault's data.
