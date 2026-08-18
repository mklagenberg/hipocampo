# 0031 — Adoption of the Change Set mechanism (MODA)

**Status:** Accepted

## Context

Major finding 5 from the 2026-08-17 MODA audit (`audits/moda/2026-08-17-v1.0.0-self-audit.md`): Hipocampo had no formal proposal+impact mechanism before implementing an operational/normative change — `decisions/0014` (release routine), `decisions/0021` (cadence), `decisions/0023` (SemVer criterion) cover cadence and scope classification, but don't declare triggers, affected surfaces, or per-change validation before implementing. MODA itself formalizes this mechanism (their `docs/change-management.md`, `changes/<id>/`) as part of the repository contract (MODA SPEC, sections 4.16 and 5.5).

## Decision

Adopt MODA's Change Set mechanism, adapted to Hipocampo in `docs/change-management.md`: `editorial`/`operational`/`normative` classes (MODA vocabulary, kept in English — see rationale); a mandatory Change Set in `changes/<change-id>/` (`proposal.md` + `impact.yaml`) for `operational`/`normative` changes; a trigger table adapted to Hipocampo's real vocabulary (`normative_rule`, `frontmatter_schema`, `cross_repository_mechanism`, `sensitive_data_policy`, `release`) instead of literally copying MODA's triggers — `package_contract`, for example, has no real equivalent in Hipocampo today, because the concept of a packaged and distributed package doesn't exist in this repository yet.

Change Set doesn't replace Decision Record — the two keep coexisting with different scopes (Change Set = the impact of this specific change; DR = the durable choice itself, the same distinction of purpose already in use between Decision Record and `type: decision`, `SPEC.md` section 7).

First exercise of the mechanism: retroactive backfill of `changes/0026-0028-fact-account-opinion-memory-taxonomy-and-cross-repo-lifecycle/` covering PR #22 (already merged before this mechanism existed) — validates the template against real, already-reviewed work, before requiring it prospectively. PRs #23 and #24 (also merged before this mechanism existed) don't get a backfill — only PR #22 serves as the template-validation exercise, proportional to the goal of validating the mechanism, not of retroactively rewriting the entire recent history.

## Rationale

Closing major finding 5 without inventing a mechanism from scratch — reusing MODA's design (which already solved exactly this problem, with trigger rules and impact statuses tested in their own adoption) is cheaper and more consistent than designing something new. Adapting (not copying) the trigger table avoids declaring surfaces that don't exist in Hipocampo today (`schemas/`, `scripts/`, `skill/` as folders of the repository itself — the skill lives in `hipocampo-toolkit`, outside this repository, until Phase D consolidates it).

## Discarded alternatives

- **A custom mechanism, designed from scratch.** Discarded — it would reinvent a problem MODA already solved, without real gain; MODA's vocabulary (`editorial`/`operational`/`normative`) is already precise enough.
- **Translate the classes into Portuguese.** Discarded — "operacional"/"normativo" translate well, but "editorial" in Portuguese carries a connotation of opinion/commentary that doesn't exist in the original term (a wording/formatting change); keeping the technical term in English avoids that noise, even with the rest of the repository in Portuguese (this will be revisited when Phase E translates the entire repository).
- **Retroactive backfill of all PRs merged so far (#22, #23, #24).** Discarded — disproportionate to the goal of validating the template; only PR #22 was explicitly chosen as the exercise in the 2.0.0 release plan.
