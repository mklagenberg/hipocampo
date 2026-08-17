# 0021 — Release cadence policy: accumulate before shipping, hotfix for urgency

**Status:** Accepted

## Context

The mandatory release routine (DR0014, v1.6.0) already defines what needs to happen with each new version (migration check, toolkit synchronization), but says nothing about how frequently new versions should be cut. In practice, between 2026-07-27 and 2026-07-29, the methodology published ten versions (v1.0.0 through v1.9.0) within a few hours of continuous work — every MINOR bump immediately became a published tag and release. This had a concrete, already-observed consequence: real content instances (`hipocampo-company`, `hipocampo-concepts`, `hipocampo-personal-vault`) got stuck on `^1.0.0` for nine entire versions, because keeping up with that publication pace is not realistic for someone who only consumes the methodology.

## Decision

Work on the methodology (a new Decision Record, a SPEC.md change, a new doc) accumulates on `main` via a normal PR, without necessarily becoming a tag/release right away. A release (tag + published GitHub Release) is only cut when there is accumulated critical mass, or at a natural pause in work, at the discretion of whoever maintains the methodology. `CHANGELOG.md` gains an `[Unreleased]` section at the top, which accumulates entries until release time — only then do those entries become a real versioned section.

A genuinely urgent change (fixing an error that disrupts current use, not new capability) ships as a PATCH, outside the normal accumulation cycle — an immediate release, without waiting for the next publication window.

## Rationale

SemVer communicates to consumers whether something changed in a way that needs attention — this presupposes that a published version had some life before the next one exists. Publishing ten versions in a few hours does not send that signal; it sends the opposite signal (change so fast that keeping up is unfeasible), and this has already caused the real problem of outdated instances. Reserving the PATCH path for genuine urgency preserves the ability to fix quickly when needed, without requiring every small change to become an isolated release.

## Discarded alternatives

- **Keep the pace of tagging every change:** discarded due to the concrete evidence already observed (nine versions of lag in real instances).
- **Only allow manual release, with no urgency path at all:** discarded — it would create unnecessary friction for fixing a real error that cannot wait for the next accumulated batch.
