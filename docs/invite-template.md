# Invite and onboarding templates

Static, public text covering the three ways someone starts using Hipocampo: discovering it on their own with nothing set up yet, or being invited into someone else's vault — with or without a personal vault of their own already. None of these three is an action or a mechanic itself (`SPEC.md`, section 5-D) — they're content whose only job is to trigger the Bootstrap mechanic (`decisions/0045`) in whoever receives them, and to make the agent that receives them read the canonical operational docs rather than re-deriving instructions from scratch. See `decisions/0049-onboarding-templates-and-create-invite-action.md` for why this document is shaped the way it is.

**Scope of this revision: Claude (Cowork, Claude.ai, Claude Code) and ChatGPT only.** A tool that operates from a working directory or IDE context rather than a chat a user pastes text into — Codex, GitHub Copilot — needs a different onboarding shape, not a variant of this one; deliberately out of scope here, see `decisions/0049`, Discarded alternatives. `docs/MULTI-TOOL-USAGE.md` still covers the full tool list for an already-running instance.

Fill in the bracketed placeholders before sending any of the three. Every prompt below ends with the same instruction, deliberately: **have the actual conversation in whatever language the recipient is writing in, not necessarily English.** This document itself stays in English (`decisions/0034`) because it's operational content an agent reads, not the literal words a user reads — the agent is expected to interpret it and act accordingly, including translating its own conversational behavior, never a hardcoded language for the human on the other end.

## Scenario 1 — Starting from zero, no invite

For someone who found out about Hipocampo on their own (a link, a friend, a search) and has nothing set up yet — no invite, quite possibly no GitHub account either. Referenced from `GETTING-STARTED.md`.

> I just found out about a methodology called Hipocampo — it gives an AI agent durable memory by storing what it learns as files in a private GitHub repository, instead of losing everything between conversations. I don't have anything set up yet: no repository, and I'm not sure whether I already have a GitHub account.
>
> Read `https://github.com/mklagenberg/hipocampo/blob/main/skill/SKILL.md`, `https://github.com/mklagenberg/hipocampo/blob/main/AGENTS.md`, and `https://github.com/mklagenberg/hipocampo/blob/main/docs/getting-started-non-technical.md`. Then walk me through getting set up from scratch, one step at a time: a GitHub account if I don't already have one, connecting yourself to it with the right permissions, saving these instructions so you still have them in our next conversation (not just this one), and creating my own personal vault — that part always comes first, even before anything else I might eventually want Hipocampo for.
>
> Explain things simply, assume I'm not technical, and don't skip a step just because it seems obvious — but keep each explanation short. Have this whole conversation in the language I'm writing to you in.

## Scenarios 2 and 3 — Invited into someone else's vault

For someone invited into an existing entity's vault — for example, a teammate being brought into a company's vault — whether or not they already use Hipocampo themselves. The two scenarios collapse into one template because the Bootstrap mechanic already branches on this by itself (`SPEC.md` section 12-B, action **Select**): a recipient with no personal anchor vault yet gets the full first-time walkthrough; a recipient who already has one skips straight to registering the new entity. Neither variant below needs to know in advance which case applies — the receiving agent works it out.

### Variant A — for a chat message (Slack, Teams, email)

> Hi [name] — I'd like to give you access to [entity/repository name]'s Hipocampo knowledge base. It's a private repository an AI agent reads from and writes to, so it doesn't have to be explained fresh every conversation.
>
> To get set up:
> 1. Accept the GitHub invite to `[owner/repo]` (you'll get one separately, or ask [inviter name] to send it).
> 2. Tell your AI agent (Claude or ChatGPT — whichever you use day to day) something like: "I've been invited to a Hipocampo repository at `[owner/repo]` — help me get set up." The agent takes it from there, including creating your own personal vault first if you don't already have one — that part isn't optional, it's how the methodology keeps your own knowledge separate from [entity name]'s.
>
> Questions before then — just ask me.

### Variant B — to paste directly into Claude or ChatGPT

> I've been invited to a Hipocampo repository at `[owner/repo]` (or: I've been told to set up Hipocampo, starting with this repository). Read `https://github.com/mklagenberg/hipocampo/blob/main/skill/SKILL.md` and `https://github.com/mklagenberg/hipocampo/blob/main/AGENTS.md`, then help me get set up — including creating my own personal vault first if I don't already have one, and saving these instructions so you still have them in future conversations, not just this one. If anything about GitHub accounts, permissions, or what a "personal vault" even is isn't already clear to me, also read `https://github.com/mklagenberg/hipocampo/blob/main/docs/getting-started-non-technical.md` and walk me through it — don't assume I already know.
>
> Have this conversation in the language I'm writing to you in.

## Creating an invite (for an existing Hipocampo operator)

Anyone already operating a Hipocampo vault can ask their own agent to fill in and produce one of the two invite variants above for a specific person — no separate tool, no template file to open by hand. This is a discretionary, ungated action (`docs/step-classification.md`): it only produces text for the human to send elsewhere, it doesn't write anything to any repository, so none of Invariant 5's write-confirmation gate applies to it. It is deliberately not added to `SPEC.md`'s formal Dispatcher/Routine/Mechanic/Action taxonomy for the same reason — see `decisions/0049`, Discarded alternatives.

To trigger it: ask your agent something like *"create an invite for [name] to access [entity/vault]."* The agent should:

1. Fill in `[owner/repo]`, `[entity/repository name]`, `[name]`, and `[inviter name]` from what it already knows about the target vault and the conversation.
2. **Default the language to the target vault's own declared `instance.language`** (`hipocampo.yaml`, `decisions/0033`/`0034`) — not the language of the conversation asking for the invite, and not English by default. Only use a different language when the person asking explicitly requests one (e.g., "write it in Spanish instead").
3. Present the filled-in text before handing it over — this is content generation, not a repository write, so it doesn't need Invariant 5's explicit confirmation gate, but showing the result before the human copies it elsewhere is still good practice.
4. Remind the human that sending the actual GitHub collaborator invite is a separate, manual action this mechanism doesn't automate (see notes below).

## Notes for whoever is sending any of these

- **Personal bootstrap always comes first**, even if the entity someone is being invited into is the only reason they're here right now (`decisions/0040`, premise 3; `decisions/0045`, "personal bootstrap is a prerequisite"). Don't reword any variant to skip that step — the fallback-with-tag mechanism (`SPEC.md` section 2-D) has nowhere to land for a user with no personal anchor yet.
- **Sending the actual GitHub collaborator invite** (Scenarios 2/3) is a separate, manual action outside anything Hipocampo automates — these templates only cover what to say, not the invite mechanism itself.
- **Repository-creation permission can be too narrow.** If the recipient's Claude/ChatGPT connection to GitHub is scoped to specific pre-existing repositories rather than all of them, the agent will hit a permission wall the moment it tries to create the new vault. This isn't a bug in these templates — it's `SPEC.md` section 14's existing "Unavailable tool" behavior applying to this specific step: the agent names exactly what's missing and hands the human a concrete fix (usually: go back to the connector's settings and either grant broader access or add the newly-needed repository to the existing grant) instead of getting stuck silently. `docs/getting-started-non-technical.md` covers this step by step.
