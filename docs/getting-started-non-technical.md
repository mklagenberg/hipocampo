# Getting started, for someone who has never heard of Hipocampo

Content the agent draws on for the **Orient** action of the Bootstrap mechanic (`SPEC.md`, section 12-B; `decisions/0045-bootstrap-mechanic-and-profile-md.md`) — presented conversationally, as part of a back-and-forth with the user, not handed over as a link to go read alone. This document is the script/reference the agent consults; it is not itself what the user reads. Every prompt in `docs/invite-template.md` that a first-timer might paste points here.

This is different in kind from [`GETTING-STARTED.md`](../GETTING-STARTED.md) and [`docs/FUNDAMENTALS.md`](FUNDAMENTALS.md), which are written for solo reading by someone already willing to work through a document. This one exists because a first-time user's actual entry point is usually a conversation with an AI agent, not a documentation site — the content here needs to hold up when spoken, a few sentences at a time, with room for the user's own questions in between.

**Scope of this revision: Claude and ChatGPT only** (`decisions/0049`). Both are chat-first tools a user pastes text into to begin; a working-directory/IDE-first tool like Codex or GitHub Copilot needs a differently-shaped onboarding script, deliberately not attempted here. `docs/MULTI-TOOL-USAGE.md` covers the full tool list for an instance that's already running.

Kept as a separate document, deliberately outside the Bootstrap mechanic's own definition in `SPEC.md`, because it changes on a different rhythm than the mechanic itself: platform installation steps shift whenever Claude or ChatGPT changes how it manages connectors or persistent instructions — far more often than the mechanic's four actions are expected to change. Treat every concrete menu path below as current as of this writing, not as a permanent fact — if it doesn't match what the user sees, look for the nearest equivalent (usually still called "Connectors," "Skills," or "Custom Instructions") rather than assuming the whole flow changed.

## What Hipocampo is, in one or two sentences

An AI agent's memory doesn't normally survive between conversations. Hipocampo is a way to give it durable memory: files that live in a private repository the agent reads from and writes to, so what it learns about you (or your work) is still there next time — recognizable, versioned, and readable with any plain text editor, not locked inside one product.

## Why a repository, specifically

Two reasons worth saying out loud to someone hearing this for the first time:

- **It's not locked to one AI product.** The knowledge lives as plain markdown files, not inside a chat history. If you switch tools, or a product changes, the knowledge is still there.
- **Privacy is a real technical setting, not just a promise.** A private repository is only visible to people explicitly invited to it — access is enforced by the hosting platform itself (see `docs/FUNDAMENTALS.md` for the fuller version of this), not by anyone's good intentions.

## Before you begin: a GitHub account

Hipocampo's knowledge lives in a GitHub repository, so this comes first if the user doesn't already have one. Go to [github.com](https://github.com) and sign up — a free account is enough; every plan, including free, allows creating private repositories, and Hipocampo's knowledge repositories are always private (`SPEC.md`, invariant 1). Nothing else about the account needs deciding up front.

## Connecting your AI tool to GitHub, with the right permissions

The agent needs to read and write files in GitHub repositories on the user's behalf — that connection is what lets it operate Hipocampo at all, not an optional extra.

**Claude.** In Claude's settings, look for **Connectors** (sometimes under a "Customize" section). Add or connect the GitHub connector, sign in to GitHub when prompted, and authorize it. A connector, once added, stays saved in your account for future conversations — but it still needs to be turned on inside each individual conversation (a "+" or "Connectors" control near the message box), it doesn't attach itself automatically.

**ChatGPT.** In ChatGPT's settings, look for **Connectors**. Find GitHub, select Connect, and authorize through GitHub. Like Claude, the connection itself is saved to your account, but you still need to turn the GitHub connector on for each new chat where you want to use it (a dropdown near the message box lists your connected apps).

**The permission that actually matters here: which repositories the connection can reach.** During authorization, GitHub asks whether to grant access to *all* repositories or only *selected* ones. Hipocampo creates new repositories as part of normal use (your personal vault, and later any additional ones) — if you grant access only to repositories that already exist, the agent will hit a wall the moment it tries to create a new one. Granting "all repositories" access avoids this. If you'd rather keep access scoped narrowly, that's fine too — just expect the agent to sometimes tell you it needs you to go back to GitHub's connector settings and add a newly-created repository to the allowed list before it can continue. Either way this isn't an error to panic about: it's expected behavior when a permission is missing (`SPEC.md`, section 14), and the agent will say exactly what it needs.

## Installing the Hipocampo skill so it's always available

Reading `SKILL.md` once gets the agent through a single conversation. For it to behave the same way next time without you re-explaining anything, it needs to be saved somewhere persistent — this is different per tool.

**Claude.** Claude has a native Skills feature. In settings, look for **Skills** (often under "Customize"), add a new skill, and provide the contents of `skill/SKILL.md` and the files under `skill/references/` (this repository's canonical copies). Once saved and turned on, Claude applies it automatically in future conversations without needing to be told to. (In Cowork specifically, the equivalent is saving it via the platform's own skill-saving mechanism, e.g. `save_skill`.)

**ChatGPT.** ChatGPT doesn't have an equivalent "skill" concept, and its closest global mechanism — **Custom Instructions** (Settings → Personalization) — has a character limit (in the low thousands), too small to hold the full skill content, and pasting it in verbatim would also go stale the moment `SKILL.md` changes on GitHub. Instead, save a short pointer as a custom instruction, along these lines:

> Whenever Hipocampo, a "second brain," or a personal/work knowledge repository comes up, first fetch and follow `https://github.com/mklagenberg/hipocampo/blob/main/skill/SKILL.md` and `https://github.com/mklagenberg/hipocampo/blob/main/AGENTS.md` (using the GitHub connector or a raw URL fetch) before doing anything else — treat those as your live operating instructions for that conversation, not something to remember verbatim from before.

Custom instructions apply to every new chat immediately, so this only needs to be set once.

Either way, this step matters: without it, every new conversation starts from zero and the user has to re-paste onboarding text each time.

## What happens next, concretely

The agent creates the repository for the user — there is no template button to click, no separate setup tool to install first. The user answers a short round of questions (what to call the repository, whether this is personal or tied to an organization), confirms the plan the agent presents before anything is written (this confirmation step is not optional — it happens before every durable write Hipocampo ever makes, not only this first one), and the repository exists a few moments later. If the connector's permission is too narrow to create it (see above), the agent says so specifically and states the concrete fix, rather than failing silently or pretending it succeeded.

## Your first vault, and what comes later

This first repository is always the user's own **personal anchor vault** — never a company's or anyone else's, even if what actually brought them to Hipocampo was an invitation to someone else's vault. That's not a formality; nothing else Hipocampo does (finding other vaults later, falling back gracefully when something's unreachable) has anywhere to work from without it (`SPEC.md`, section 2-D).

From there, nothing further needs installing or reconfiguring to gain access to more vaults later — say, being invited into a company's knowledge base. The user accepts the GitHub invite when it comes, tells their agent about it (`docs/invite-template.md`, Scenarios 2/3), and the agent registers it using the same connection and the same saved skill already set up here. The full model behind this — how vaults, entities, and access relate to each other — is real depth a user grows into once they're actually using their first vault, not something to front-load now; when it comes up naturally, point to `SPEC.md` sections 2-C, 2-D, and 12-A rather than trying to compress it into this conversation.

## What this section doesn't cover

The full entity/vault model, cross-repository references, the Promote/Depromote/Redbutton actions — none of that belongs in a first-timer's Orient conversation. It's real depth a user grows into once they're actually using their first vault, not something to front-load before they've written a single document. If the conversation naturally goes there, point to `GETTING-STARTED.md` and `SPEC.md` rather than trying to compress it into this script.
