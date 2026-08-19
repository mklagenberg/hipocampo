# Invite template

Static, public text for inviting someone else into a Hipocampo entity — for example, a teammate being brought into a company's vault. Not an action or a mechanic itself (`SPEC.md`, section 5-D) — it's content whose only job is to trigger the Bootstrap mechanic (`decisions/0045`) in whoever receives it. Referenced from `SPEC.md`, section 12-B.

Fill in the bracketed placeholders before sending either variant. Neither variant assumes the recipient has ever used Hipocampo before — that's what the Bootstrap mechanic's Orient action (`docs/getting-started-non-technical.md`) is for, once they act on the invite.

## Variant 1 — for a chat message (Slack, Teams, email)

> Hi [name] — I'd like to give you access to [entity/repository name]'s Hipocampo knowledge base. It's a private repository an AI agent reads from and writes to, so it doesn't have to be explained fresh every conversation.
>
> To get set up:
> 1. Accept the GitHub invite to `[owner/repo]` (you'll get one separately, or ask [inviter name] to send it).
> 2. Tell your AI agent (Claude, ChatGPT, or whatever you use day to day) something like: "I've been invited to a Hipocampo repository at `[owner/repo]` — help me get set up." The agent will take it from there, including creating your own personal vault first if you don't already have one — that part isn't optional, it's how the methodology keeps your own knowledge separate from [entity name]'s.
>
> Questions before then — just ask me.

## Variant 2 — to paste directly into an AI agent's prompt

> I've been invited to a Hipocampo repository at `[owner/repo]` (or: I've been told to set up Hipocampo, starting with this repository). Read `https://github.com/mklagenberg/hipocampo/blob/main/skill/SKILL.md` and `https://github.com/mklagenberg/hipocampo/blob/main/AGENTS.md`, then help me get set up, including creating my own personal vault first if I don't already have one.

## Notes for whoever is sending an invite

- The recipient's own personal anchor vault always comes first, even if the entity they're being invited into is the only reason they're here right now (`decisions/0040`, premise 3; `decisions/0045`, "personal bootstrap is a prerequisite"). Don't reword either variant to skip that step — it's not a formality, the fallback-with-tag mechanism (`SPEC.md` section 2-D) has nowhere to land for a user with no personal anchor yet.
- Sending the GitHub invite itself (the actual collaborator invite on the target repository) is a separate, manual action outside anything Hipocampo automates — this document only covers what to say, not the invite mechanism itself.
