# Change Set — 0049: Onboarding templates (three scenarios) and the Create Invite action

## Summary

Revalidates and rewrites the onboarding surface (`docs/invite-template.md`, `docs/getting-started-non-technical.md`) against three concrete cases: a total novice discovering Hipocampo on their own, a novice invited into someone else's vault, and an existing Hipocampo user invited into someone else's vault. Adds a cold-start prompt for the first case (no `[owner/repo]` to reference), collapses the other two into one invite template (Bootstrap's own **Select** action already branches on whether the recipient has a personal vault), and expands the getting-started script to cover GitHub account creation, connecting Claude/ChatGPT to GitHub with the right permission scope, and installing the skill so it persists globally rather than needing to be re-read every conversation. Adds a new discretionary, ungated **Create Invite** action any operator can ask their agent for, defaulting to the target vault's declared language. Scope this round: Claude and ChatGPT only — Codex and GitHub Copilot need a differently-shaped (working-directory/IDE-first, not chat-first) onboarding flow, deliberately deferred.

Two incidental defects fixed transparently while cross-referencing tool-connection instructions: `docs/MULTI-TOOL-USAGE.md` still pointed at the archived `hipocampo-toolkit/skill/SKILL.md` path, and still said "five invariants" after Lote D added a sixth.

See `decisions/0049-onboarding-templates-and-create-invite-action.md` for the full reasoning, including why the repository-creation-permission-fallback case needed no new rule (`SPEC.md` §14's existing "Unavailable tool" clause already covers it) and why Create Invite isn't added to `SPEC.md`'s formal taxonomy.

## Class

**operational** — expands execution guidance and reference content (what to say, how to connect the tools, how to install the skill persistently) without changing any normative obligation. No new invariant, no new schema field, no new cross-repository mechanism, no new sensitive-data rule. Still `Required` per `docs/change-management.md`'s class table.

## Semver

**minor** — purely additive reference/onboarding content plus a small `skill/SKILL.md` addition (a new "Creating an invite" section) and two incidental corrections. No existing instance becomes formally incompatible with no action, per `decisions/0023`'s operational test.

## Triggers fired

| Trigger | Triggered? | Note |
|---|---|---|
| `regra_normativa` | No | No `SPEC.md` edit — Create Invite is deliberately documented outside the formal taxonomy, see `decisions/0049`. |
| `schema_frontmatter` | No | No frontmatter field added or changed. |
| `mecanismo_cross_repositorio` | No | Sections 6 and 13 unchanged in substance. |
| `politica_dados_sensiveis` | No | Section 2-A unchanged. |
| `release` | Reserved | Evaluated at the v2.0.0 release closing. |

Change Set required by the `operational` class itself, independent of the trigger table above.

## Impact

See `impact.yaml`.

## Known, not addressed here

- **Codex and GitHub Copilot.** Deliberately out of scope this round — both are working-directory/IDE-first rather than chat-first, and forcing them into this revision's paste-a-prompt pattern would misrepresent how they actually work. See `decisions/0049`, Discarded alternatives.
- **No automated check that Claude/ChatGPT's connector UI still matches what's described.** Both product surfaces change independently of this repository's release cadence — `docs/getting-started-non-technical.md` already flags this explicitly and points at the nearest equivalent label ("Connectors," "Skills," "Custom Instructions") as the fallback when exact wording drifts.
- **No automated staleness check for `docs/invite-template.md`, `docs/getting-started-non-technical.md`, or the new `skill/SKILL.md` section.** Same limitation already flagged for other reference docs in Lote E1 — manually maintained.
