# Change Set — 0049: Onboarding templates (three scenarios) and the Create Invite action

## Summary

Revalidates and rewrites the onboarding surface (`docs/invite-template.md`, `docs/getting-started-non-technical.md`) against three concrete cases: a total novice discovering Hipocampo on their own, a novice invited into someone else's vault, and an existing Hipocampo user invited into someone else's vault. Adds a cold-start prompt for the first case (no `[owner/repo]` to reference), collapses the other two into one invite template (Bootstrap's own **Select** action already branches on whether the recipient has a personal vault), and expands the getting-started script to cover GitHub account creation, connecting Claude/ChatGPT to GitHub, and installing the skill so it persists globally rather than needing to be re-read every conversation. Adds a new discretionary, ungated **Create Invite** action any operator can ask their agent for, defaulting to the target vault's declared language, and a fourth template — three orienting questions a Scenario 2/3 recipient can paste once their agent confirms a new vault is registered. Introduces a light **homologation status** concept: the methodology stays platform-agnostic by design, but this repository's onboarding walkthrough is only concretely written and checked for specific tools — currently Claude (including Cowork) and ChatGPT. Scope this round: Claude and ChatGPT only — Codex and GitHub Copilot need a differently-shaped (working-directory/IDE-first, not chat-first) onboarding flow, deliberately deferred.

**Correction made before this Change Set merged, not after:** the version first opened for review framed a missing repository-creation capability as a too-narrow permission grant, and told the user to broaden it. That's wrong for the two tools this revision covers — the standard Claude.ai/Claude Desktop and ChatGPT connectors don't create repositories at all, regardless of scope, and ChatGPT's standard connector can't write files at all, only read. Caught by checking Mauricio's own prior first-hand technical notes on GitHub Apps' authorization model before finalizing this Change Set, per his standing instruction to consult that first. `docs/getting-started-non-technical.md` now also documents the actual GitHub-side page for managing repository access (`github.com/settings/installations`, not linked from either product's settings) and a concrete manual-repository-creation fallback, and adds a welcome message the agent presents once Bootstrap finishes — closing the "nothing is ever said at the end of the conversation" gap this Change Set had originally left open.

Four incidental defects fixed transparently while cross-referencing tool-connection instructions: `docs/MULTI-TOOL-USAGE.md` still pointed at the archived `hipocampo-toolkit/skill/SKILL.md` path, and still said "five invariants" after Lote D added a sixth; `docs/FAQ-AND-COMMON-ERRORS.md`'s "Use this template" instantiation-error entry described a mechanism `decisions/0032` had already retired, and its Apache-2.0-license entry described a bug only that same retired mechanism could cause.

See `decisions/0049-onboarding-templates-and-create-invite-action.md` for the full reasoning, including why the repository-creation-permission-fallback case needed no new rule (`SPEC.md` §14's existing "Unavailable tool" clause already covers it, once applied to the corrected understanding of what's actually unavailable) and why Create Invite isn't added to `SPEC.md`'s formal taxonomy.

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
- **No automated check that Claude/ChatGPT's connector UI, or their exact repository-creation capability, still matches what's described.** Both product surfaces change independently of this repository's release cadence, and connector capability specifically is exactly the kind of claim that already needed one correction before this Change Set merged — `docs/getting-started-non-technical.md` flags this explicitly and points at the nearest equivalent label ("Connectors," "Skills," "Custom Instructions") as the fallback when exact wording drifts, but a future capability change (e.g., a connector gaining write or create access) would need a human to notice and update this document; nothing here detects that automatically.
- **No automated staleness check for `docs/invite-template.md`, `docs/getting-started-non-technical.md`, or the new `skill/SKILL.md` section.** Same limitation already flagged for other reference docs in Lote E1 — manually maintained.
- **`docs/FUNDAMENTALS.md` and `decisions/0032` still state, without qualification, that "the agent creates the repository for you... you don't click anything on github.com yourself."** True for Cowork/Claude Code, not for the standard Claude.ai/Desktop or ChatGPT connectors this Change Set now documents accurately elsewhere. Found while researching the correction above; left alone here to keep this Change Set's diff scoped to the files it already touches — flagged for a future pass rather than fixed opportunistically.
- **`docs/FAQ-AND-COMMON-ERRORS.md` still references the archived `hipocampo-toolkit` repository in several other entries** (git-host independence, methodology licensing, migrated-file question) beyond the two fixed here. Pre-existing staleness, same category as the two entries this Change Set did fix, left for a future pass to keep this diff scoped to the authorization/permissioning topic Mauricio specifically asked about.
