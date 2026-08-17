# 0023 — Operational criterion for SemVer scope (MAJOR/MINOR/PATCH)

**Status:** Accepted

## Context

SPEC.md, section 9, defines MAJOR/MINOR/PATCH in abstract terms (breaks compatibility / new compatible capability / clarification-correction), but never offered a practical test for applying that definition to a concrete change — each release decided the scope by loose judgment. This became evident when exercising, for the first time, a real upgrade guide (see DR0024): to classify each change between v1.3.0 and v1.9.0 as "action required" or "informational only," it was necessary to apply a test that wasn't written down anywhere — it only existed informally in the head of whoever was deciding.

## Decision

Every change accepted into the methodology is classified by this test, before entering the release routine (DR0014):

- **MAJOR:** an existing instance, without any action, becomes formally **incompatible** with the new version (required field renamed/removed, mechanism eliminated, a rule the instance was already following stops being valid).
- **MINOR:** new, additive capability — an existing instance **remains valid without any action**, even if it stays "behind" relative to the new capability available (real example: section 11, `AGENTS.md` as the canonical file, is MINOR — no instance still using only `CLAUDE.md` is broken by this).
- **PATCH:** clarification or correction that doesn't change the schema nor introduce new behavior (real example: DR0022, which closes a traceability gap without creating new capability).

This test is applied as the first step of the mandatory release routine (DR0014), before any other step — the scope classification determines, among other things, whether the change needs an entry in `MIGRATIONS.md` (MAJOR only) and/or in `UPGRADE.md` (MINOR/PATCH with recommended action, see DR0024).

## Rationale

Inconsistent scope classification between different releases propagates error forward: if a MINOR change is treated as MAJOR, it generates disproportionate migration work; if a change that should generate an upgrade recommendation is treated as "informational only," it never reaches `UPGRADE.md` and no existing instance learns it should adopt it. The "does it break, or does it just fall behind?" test is simple enough to apply consistently without requiring case-by-case judgment.

## Discarded alternatives

- **Leave it open, decide case by case.** Discarded — it was exactly this ambiguity that motivated the review that originated this DR.
- **A fourth scope level (e.g., "strong MINOR" vs. "weak MINOR") to capture the difference between trivial and structural new capabilities (like `AGENTS.md`).** Discarded for now: the three-level SemVer is already sufficient as long as `UPGRADE.md` (DR0024) carries the granularity of "how recommended" each item is — it doesn't need a formal fourth level in the versioning itself.
