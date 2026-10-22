# 0122 — Bundled skill content and independent versioning

**Status:** Accepted direction from the operator on 2026-10-22

## Context

Change Set 0136 and PR #63 added `skill/references/legacy-read.md` and changed
`skill/SKILL.md` and `skill/references/v3-operation.md`, but retained skill
version 2.1.0. The package lock correctly recorded different bytes; the
manifest and compatibility contract still gave those bytes the same version
as the earlier installed package. A user could therefore see 2.1.0 in both
places while only one package included the new V2 read instructions.

## Decision

The independently versioned skill includes `skill/SKILL.md` and every other
distributable file under `skill/` listed by its package lock. A content or
instruction change in that bundle requires a higher skill version. A
compatible new skill capability is MINOR; corrections without new capability
are PATCH. The V2 read route added by PR #63 is a compatible new capability,
so the candidate skill moves from 2.1.0 to 2.2.0. Methodology target 3.1.0
and its `^3.0.0` vault compatibility range do not change for this correction.

A document elsewhere in the methodology repository that the skill merely
references is outside the distributable skill package. Its change alone does
not require a skill version bump. The lock proves exact package bytes but does
not substitute for the manifest version. PR validation compares bundled-file
changes with the previous and current skill versions, rejecting reuse or
downgrade of a version. Release and installation approvals remain separate.

## Rationale

Package consumers and update checks need both a meaningful SemVer identity
and byte integrity. The new V2 route changes what the installed skill tells an
agent to do, even though it leaves the V3 data contract intact. Applying the
same rule to external methodology documents would needlessly couple the
independent package version to every repository edit.

## Discarded alternatives

- Keep 2.1.0 and rely only on a new package-lock hash: hides behavior change
  from version checks and creates two packages with the same identity.
- Bump the skill for every external `SPEC.md` or `docs/` edit: confuses the
  package boundary with the methodology source boundary.
- Treat the V2 read capability as a PATCH: it adds an operation to the skill.

## Consequences and validation

Synchronize the skill manifest, lock, declared package version, compatibility
tuple, installation examples and review routing. Add differential CI cases for
bundled `SKILL.md`/reference changes, unchanged external documents and
monotonic versions. Historical release evidence remains unchanged. No client
installation or vault update follows automatically from this decision.

This applies FF-CON-0001 clauses 1.5–1.7 and 2.7, 2.10–2.11; it requires no
constitutional exception. Human review judges MINOR versus PATCH when the
changed behavior is consequential. This decision refines the existing
independent skill SemVer and lock rule in Decision 0053.
