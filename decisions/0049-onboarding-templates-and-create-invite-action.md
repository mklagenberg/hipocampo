# 0049 — Onboarding templates: three scenarios, global skill install, and the Create Invite action

**Status:** Accepted

## Context

`docs/invite-template.md` and `docs/getting-started-non-technical.md` (Lote C, `decisions/0044`/`0045`) already existed, but a revalidation against three concrete cases — a total novice discovering Hipocampo on their own, a novice invited into someone else's vault, and an existing Hipocampo user invited into someone else's vault — surfaced real gaps rather than just missing polish:

- No variant covered someone who found Hipocampo on their own, with no `[owner/repo]` to reference — every existing prompt assumed a specific invite already existed.
- Nothing covered creating a GitHub account, connecting Claude or ChatGPT to GitHub, or the permission scope that connection needs — `docs/FUNDAMENTALS.md` and the old "platform-specific installation notes" both assumed these were already in place.
- "Installing the skill" only ever meant reading it for the current conversation. Nothing addressed making it persist across future conversations, which is a different, tool-specific mechanism per platform.
- There was no way for an existing operator to generate a filled-in, correctly-localized invite for a specific person without hand-editing the template file directly.

Separately, walking through what happens when the agent's GitHub connection lacks permission to create a new repository (a real, likely scenario if the user scoped the connector narrowly) turned out to already be covered: `SPEC.md` section 14's "Unavailable tool" clause explicitly names "a write permission is missing" as one of its own worked examples, and already prescribes the exact fallback needed — name what's missing, complete what doesn't depend on it, hand the human a concrete pending step. No new rule was needed there, only applying the existing one concretely to this step.

## Decision

**Three onboarding scenarios, not two.** `docs/invite-template.md` now covers: (1) starting from zero, no invite, self-discovered; (2)/(3) invited into someone else's vault, with or without an existing personal vault — collapsed into one template because Bootstrap's own **Select** action (`SPEC.md` section 12-B) already branches on this, so the invite text doesn't need to know in advance which applies.

**Scope narrowed to Claude and ChatGPT.** Both are chat-first tools a user pastes text into to begin. Codex and GitHub Copilot operate from a working directory or IDE context instead — a structurally different onboarding shape, not a variant of this one. Deliberately excluded from this revision; see Discarded alternatives.

**`docs/getting-started-non-technical.md` now covers, step by step:** creating a GitHub account, connecting Claude/ChatGPT to GitHub via each tool's connector mechanism, the repository-access scope Hipocampo needs (and what happens when it's too narrow — the existing `SPEC.md` §14 behavior above, not a new rule), and installing the skill so it persists globally rather than needing to be re-read every conversation (Claude's native Skills feature; for ChatGPT, a short pointer saved as a Custom Instruction rather than the full skill content, since Custom Instructions has a character limit the full skill text would exceed, and an embedded copy would go stale the moment `SKILL.md` changes). It also gains a short, appropriately shallow paragraph on the personal-anchor-first / entities-come-later model, linked to `SPEC.md` for depth rather than compressed into the script.

**`GETTING-STARTED.md`** gains a pointer near the top to the cold-start prompt, so a first-timer who lands there directly (rather than via a pasted prompt) can still find it.

**The Create Invite action.** Documented in `docs/invite-template.md` as something any existing operator can ask their own agent to do — fill in and produce a Scenario 2/3 invite for a specific person, defaulting the language to the target vault's own declared `instance.language` (`decisions/0033`/`0034`), only overridden on explicit request. **Not added to `SPEC.md`'s formal Dispatcher/Routine/Mechanic/Action taxonomy** — it produces text for the human to send elsewhere, writes nothing to any repository, and needs no gate; see Discarded alternatives for why formalizing it anyway would be disproportionate.

**Incidental fix.** `docs/MULTI-TOOL-USAGE.md` still referenced the archived `hipocampo-toolkit/skill/SKILL.md` path from before the Fase D consolidation (`decisions/0032`) — corrected to `hipocampo/skill/SKILL.md`. Found while cross-referencing tool-connection instructions for this DR, same category as the `decisions/0034`/`0035` title-template fix from Fase G and the six `Proposed`→`Accepted` status fixes from the Lote D cycle: a real, incidental defect, fixed transparently rather than left for a separate pass.

## Rationale

Revalidated against three concrete cases before writing anything — the same discipline `decisions/0048`'s step-classification scheme used, testing against real cases rather than adopting a scheme first and hoping it holds. Two of the three cases turned out to already be handled correctly by an existing rule (`SPEC.md` §14) once applied concretely to this specific step, which is itself evidence the exercise was worth doing before writing: it prevented inventing a new rule where an existing one already worked, and it surfaced the pieces (GitHub account creation, tool permissioning, global skill persistence) that genuinely had no home anywhere yet.

Narrowing scope to Claude and ChatGPT this round, rather than trying to cover every tool at once, follows the same proportionality already used elsewhere in this methodology (`decisions/0029`'s "don't structure before the real need appears," `decisions/0048`'s scoped classification) — Codex and Copilot's structurally different onboarding shape deserves its own design pass, not a forced-fit variant that would misrepresent how those tools actually work.

## Discarded alternatives

- **Formalizing Create Invite as a fifth Bootstrap action, or its own new mechanic.** Discarded — it has no durable write of its own and needs no gate; adding it to `SPEC.md`'s taxonomy for the sake of completeness would be exactly the kind of premature structure `decisions/0025` and `decisions/0029` already argue against elsewhere in this methodology.
- **Embedding the full skill content into ChatGPT's Custom Instructions.** Discarded — exceeds the field's character limit, and even if it fit, an embedded copy would silently drift out of date the moment `SKILL.md` changes on GitHub. A live pointer instruction avoids both problems at the cost of one extra fetch per conversation.
- **Covering Codex and GitHub Copilot in this same revision.** Discarded — both are working-directory/IDE-first, not chat-first; onboarding them properly means designing a different flow (how does a user with literally nothing set up yet get a first conversation started with a tool that expects to already be running inside a repository?), not writing a third variant of the same paste-this-prompt pattern. Deferred to a future revision.
