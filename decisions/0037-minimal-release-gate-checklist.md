# 0037 — Minimal release-gate checklist

**Status:** Accepted

## Context

Minor finding 2 from the 2026-08-17 MODA audit (`audits/moda/2026-08-17-v1.0.0-self-audit.md`): Hipocampo's Git/release flow (`decisions/0014`, `decisions/0021`, `decisions/0023`) is materially simpler than MODA's own release gates — acceptable at the current one-person scale, but worth a minimal checklist closer to that standard, per the audit's own words. Today `decisions/0014` lists three routine steps (migration check, `hipocampo-toolkit` synchronization, tag + Release) but nothing ties scope classification (`decisions/0023`), release cadence (`decisions/0021`), and the release routine into a single concrete run-through actually executed at the moment a release is cut. Separately, `decisions/0032` consolidated `hipocampo-toolkit` into this repository (`scaffold/` + `skill/`) — `decisions/0014`'s step 2 ("`hipocampo-toolkit` synchronization") no longer names a real target, and nothing formally updated that step to reflect the consolidation.

## Decision

Add `RELEASE-CHECKLIST.md` at the repository root: a single, concrete checklist run at release-cut time, expanding `decisions/0014`/`0021`/`0023` rather than replacing them. It covers, in order: scope classification recorded (`decisions/0023`'s test, applied and written down even when "obvious"); the `scripts/validate_hipocampo.py` validation gate (`decisions/0036`) green on the release branch; no newly introduced or worsened blocking MODA-audit `major` finding; `CHANGELOG.md`'s `[Unreleased]` section dated into a real version heading; `README.md`'s declared version bumped to match; the migration check from `decisions/0014` item 1; `UPGRADE.md` reviewed for new cumulative items; a **skill/scaffold self-sync** step succeeding the now-obsolete "`hipocampo-toolkit` synchronization" step; Change Sets accounted for (`decisions/0031`); tag + GitHub Release cut together (`SPEC.md`, section 9); and a final step confirming the merge actually landed on `main`.

## Rationale

Closes minor finding 2 proportionally to a one-person project, exactly as the audit itself asked for ("sem burocracia desproporcional a um projeto de uma pessoa") — this is not MODA's full ten-gate release process, and it does not declare a branch-protection requirement, since no tool available in this working environment can configure that GitHub repository setting (flagged as a manual follow-up for Mau, the same category of item as archiving `hipocampo-toolkit`). The final checklist item — confirming a merge actually reached `main`, not just its immediate base branch — codifies a real mistake from this repository's own history: PR #28 was opened with base = PR #27's branch (not `main`), and merging both PRs in sequence still left PR #28's commits off `main` until a third PR (#29) closed the gap. That is worth a permanent, boring line item rather than trusting the next release to remember it by chance.

## Discarded alternatives

- **Edit `decisions/0014` directly to add these items.** Discarded — every other Decision Record in this repository is treated as an accepted, durable statement of the historical decision, not a living checklist that gets appended to over time; a new DR that expands a prior one in prose, with the actual checklist living in a separate operational document, keeps that distinction intact — the same separation of purpose already established between Decision Record and Change Set (`docs/change-management.md`).
- **Adopt MODA's full release-gate model as-is.** Discarded — proportionality was the audit's own explicit criterion for this finding; a ten-gate process for a project with one maintainer and, per `decisions/0021`, intentionally infrequent releases, would be friction without a matching benefit.
