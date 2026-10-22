# Change Set 0137 — Skill package version boundary

## Problem

PR #63 changed bundled skill instructions while keeping skill version 2.1.0.
The package lock changed but the manifest, compatibility tuple and examples
did not. This allowed different 2.1.0 packages and made update availability
ambiguous. External methodology documents are a different boundary: their
changes alone should not force a skill version change.

## Proposed correction

Apply Decision 0122 to the already merged package: bump the skill candidate
to 2.2.0 (MINOR for the new V2 read capability), keep methodology target
3.1.0 and V3 vault range unchanged, synchronize all current-version surfaces
and recalculate the lock. Add a differential CI gate that detects changes to
bundled files under `skill/` and requires a strictly higher skill version.
The lock alone is excluded from this content-change trigger. Historical
release records and non-bundled methodology references remain separate.

## Acceptance

- The original PR #63 diff is rejected by the new gate because bundled skill
  bytes changed without a version increase.
- A versioned 2.1.0-to-2.2.0 bundle passes; an external documentation-only
  change does not require a skill bump.
- Manifest, package lock, compatibility tuple, docs, review routing and
  installed examples agree on 2.2.0; lock hashes match the exact package.
- Existing repository, runtime and release regression gates still pass.
  No historical receipt is reused for the new payload.

## Scope, SemVer and recovery

This Change Set is a PATCH correction to the unpublished methodology 3.1.0
candidate's packaging and quality gate. The independent skill change is
MINOR, 2.1.0 to 2.2.0, reflecting the earlier new bundled capability. No
vault migration, host installation or stable release is implied. Revert this
branch if the correction is rejected; do not retag or rewrite historical
releases.
