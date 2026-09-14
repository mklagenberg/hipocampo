# 0101 — V2.2 release-line metadata correction

**Status:** Accepted for the unreleased V3 candidate

## Context

The repository's published `v2.2.0` tag is the historical V2.2 baseline, but
the candidate checkout still declared `2.1.1` in several current-release
surfaces. The mismatch makes the active compatibility tuple, specification,
conformance profile and release history appear older than the published tag.

## Decision

Treat the published `v2.2.0` release as the active released methodology line
for the candidate checkout. Correct current-release declarations to `2.2.0`
in the README, specification, roadmap, compatibility contract, MODA metadata,
conformance metadata and V3 boundary documents. Add the missing historical
`[2.2.0]` changelog section covering Change Sets `0058`–`0069`.

Keep the `v2.2.0` tag and its objects immutable. Preserve `2.1.1` when it is
an explicit historical reference, a fixture input, a compatibility lower
bound, a version-lineage reference or a migration-history statement. This is
a release-line metadata correction, not a vault migration, skill publication,
V3 activation or compatibility-range tightening.

## Rationale

The published tag establishes the historical release identity. Current
canonical surfaces must agree with that identity, while compatibility ranges
and regression fixtures must retain their meaning. Separating these cases
removes ambiguity without claiming that V3 has been released or that any real
vault has been migrated.

## Consequences

- `2.2.0` is the active released methodology version in the candidate tree.
- V2.2 remains a readable regression baseline under V3 sovereignty.
- Existing `2.1.1` fixtures and historical evidence remain intentionally
  unchanged.
- V3 remains unreleased and still requires its own release tuple, LTE and
  human publication gates.

## Discarded alternatives

- Rewriting the published `v2.2.0` tag was rejected because release identity
  and historical evidence must remain immutable.
- Globally replacing every `2.1.1` reference was rejected because fixtures,
  compatibility lower bounds and historical upgrade evidence have distinct
  meanings.
- Tightening all compatibility ranges to `^2.2.0` was rejected because this
  correction does not introduce a migration requirement for existing V2
  vaults.

## Validation plan

- Verify all current-release declarations agree on `2.2.0`.
- Verify the `[2.2.0]` changelog section covers Change Sets `0058`–`0069`.
- Verify the V2.2 tag content and object identity are unchanged.
- Run the complete repository and V3/V2.2 validator suite twice.
- Confirm no vault cache or real vault is modified.
