# Getting started, for someone who has never heard of Hipocampo

Content the agent draws on for the **Orient** action of the Bootstrap mechanic (`SPEC.md`, section 12-B; `decisions/0045-bootstrap-mechanic-and-profile-md.md`) — presented conversationally, as part of a back-and-forth with the user, not handed over as a link to go read alone. This document is the script/reference the agent consults; it is not itself what the user reads.

This is different in kind from [`GETTING-STARTED.md`](../GETTING-STARTED.md) and [`docs/FUNDAMENTALS.md`](FUNDAMENTALS.md), which are written for solo reading by someone already willing to work through a document. This one exists because a first-time user's actual entry point is usually a conversation with an AI agent, not a documentation site — the content here needs to hold up when spoken, a few sentences at a time, with room for the user's own questions in between.

Kept as a separate document, deliberately outside the Bootstrap mechanic's own definition in `SPEC.md`, because it changes on a different rhythm than the mechanic itself: platform installation steps shift whenever Claude, ChatGPT, Cursor, or another tool changes how it manages skills/tools — far more often than the mechanic's four actions are expected to change.

## What Hipocampo is, in one or two sentences

An AI agent's memory doesn't normally survive between conversations. Hipocampo is a way to give it durable memory: files that live in a private repository the agent reads from and writes to, so what it learns about you (or your work) is still there next time — recognizable, versioned, and readable with any plain text editor, not locked inside one product.

## Why a repository, specifically

Two reasons worth saying out loud to someone hearing this for the first time:

- **It's not locked to one AI product.** The knowledge lives as plain markdown files, not inside a chat history. If you switch tools, or a product changes, the knowledge is still there.
- **Privacy is a real technical setting, not just a promise.** A private repository is only visible to people explicitly invited to it — access is enforced by the hosting platform itself (see `docs/FUNDAMENTALS.md` for the fuller version of this), not by anyone's good intentions.

## What happens next, concretely

The agent creates the repository for the user — there is no template button to click, no separate setup tool to install first. The user answers a short round of questions (what to call the repository, whether this is personal or tied to an organization), confirms the plan the agent presents before anything is written (this confirmation step is not optional — it happens before every durable write Hipocampo ever makes, not only this first one), and the repository exists a few moments later.

## Platform-specific installation notes

How the skill itself gets installed varies by AI product — this section is the part expected to need updates as platforms change; treat everything below as current as of this writing, not as a permanent fact.

**Claude (Cowork, Claude Code, API/Desktop).** The skill is saved directly from `hipocampo/skill/SKILL.md` via the platform's own skill-saving mechanism (for example, `save_skill` in Cowork). No separate account or install step beyond what the AI product itself already requires.

**ChatGPT, Cursor, and other tools with GitHub MCP support.** The same skill file works anywhere the tool can reach a GitHub MCP connection — the operational content in `skill/SKILL.md` and `skill/references/` doesn't assume any one product. See `docs/MULTI-TOOL-USAGE.md` for the fuller, standalone comparison across tools; this section only needs to say enough for a first-timer to get moving, not repeat that document.

**Anything not listed here yet.** If the user's tool isn't one of the above, the general requirement is only: the tool needs some way to read and write files in a GitHub repository (a GitHub MCP connection, or an equivalent). If it can do that, Hipocampo works there.

## What this section doesn't cover

Multi-vault structure, the entity model, cross-repository references — none of that belongs in a first-timer's Orient conversation. It's real depth a user grows into once they're actually using their first vault, not something to front-load before they've written a single document. If the conversation naturally goes there, point to `GETTING-STARTED.md` and `SPEC.md` rather than trying to compress it into this script.
