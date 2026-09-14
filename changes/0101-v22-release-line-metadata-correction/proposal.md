# Change Set 0101 — V2.2 release-line metadata correction

## Intent

Align current canonical methodology metadata with the already published
`v2.2.0` release while preserving historical, fixture and compatibility-range
references to `2.1.1`.

## Scope

Correct the current-release declarations in the README, specification,
roadmap, compatibility and MODA metadata, conformance profile, V3 boundary
documents and contract validator. Add the missing historical `[2.2.0]`
changelog section and close the corresponding row in the V2.2-to-V3 matrix.

This Change Set does not rewrite the `v2.2.0` tag, tighten compatibility
ranges, migrate a vault, change the local vault caches, publish V3, install a
skill or activate V3 behavior.

## Acceptance criteria

- current-release declarations agree on methodology version `2.2.0`;
- the changelog contains a historical `[2.2.0]` section covering Change Sets
  `0058`–`0069`;
- intentional `2.1.1` references are limited to history, fixtures, lineage or
  compatibility lower bounds;
- the matrix marks `v22-release-line-metadata` as `incorporated` and points to
  the decision and corrected authorities;
- the published tag remains byte-for-byte and object-identical;
- the full validator suite passes twice.
