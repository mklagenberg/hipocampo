---
name: hipocampo
description: >
  Operates an instance of the Hipocampo methodology (agentic second brain: git + markdown
  + AI rituals) via the GitHub MCP. Trigger when the user asks to consult,
  save, log, update, archive, or organize knowledge in any
  personal or corporate Hipocampo repository; to run the frontmatter audit, the
  REM ritual, or the weekly structural audit; to instantiate a new vault from
  a scaffold profile (`scaffold/profiles/`); to resolve `$alias:path.md`
  cross-repository; or at the start of a session, to check whether a new version of the
  methodology has been published. Generic template — does not hardcode the name of any personal or
  corporate repository; requires personalization before first real use (see
  `references/personalizacao.md`).
---

# Hipocampo Skill

Operates any instance of the [Hipocampo](https://github.com/mklagenberg/hipocampo) methodology via the GitHub MCP. Published as a generic template at `hipocampo/skill/SKILL.md` — **never use it as-is, without personalizing it first.**

**Hipocampo version this copy follows:** ^1.9.0 + unreleased (see `hipocampo/CHANGELOG.md`, `[Unreleased]` section). When personalizing, confirm it matches your instance's `AGENTS.md`. See also `manifest.yaml`, in this same directory, for the machine-readable compatibility range.

This file is just the router — each section below says when to act and points to the reference file with the full procedure. The norms themselves (schema, rules, rationale) live in `hipocampo/SPEC.md` and the Decision Records — this skill never re-explains them, it only operates them.

## Before first use: mandatory personalization

This copy only knows one universal repository (`mklagenberg/hipocampo`) — no personal or corporate repository. Read **`references/personalization.md`** and fill in the repository router (and, if applicable, the multi-account identity table) before operating on any real knowledge.

## Checking for a new release (session start)

Compare the version declared in this instance's `AGENTS.md`/`hipocampo.yaml` against the version published in `mklagenberg/hipocampo/SPEC.md`. If there is a difference: report both versions, and point to **[`hipocampo/UPGRADE.md`](https://github.com/mklagenberg/hipocampo/blob/main/UPGRADE.md)** as the next step — a cumulative, idempotent checklist of what the instance needs to become conformant, already classified into Mandatory/Recommended/Informative. Never summarize the `CHANGELOG.md` on the spot trying to reconstruct that synthesis work — `UPGRADE.md` already exists exactly for that (decision 0024). Never apply the update on your own — point the decision to the user, citing `MIGRATIONS.md` if it is MAJOR. If the instance already has a `hipocampo.yaml` (decision 0033), record the check result in that file's `state` field, instead of just stating the result in conversation.

## Instantiating a new vault

When the user asks to create a new content repository: read the corresponding profile at `hipocampo/scaffold/profiles/pessoal.yaml` or `hipocampo/scaffold/profiles/empresa.yaml`, collect the declared `inputs` (repository name, tier, owner identity) directly from the user, and generate the declared `outputs` (`AGENTS.md`, `CLAUDE.md`, `LICENSE`, `registry.md`, `example/example-note.md`, `hipocampo.yaml`, `POST-INSTANTIATION.md`) via the GitHub MCP — never copying someone else's file without review, always presenting the full plan before any write (invariant 5). There is no longer a "Use this template" button (`hipocampo-toolkit` was consolidated and archived, decision 0032) — the agent is itself the instantiation mechanism. Full procedure: **`references/instantiation.md`**.

## Reading and writing documents (CRUD)

When consulting, creating, updating, or archiving any document: read the frontmatter first, the body only when necessary; every read validates frontmatter and staleness in real time, even outside a scheduled ritual. Full procedure and example: **`references/crud-frontmatter.md`**.

## Maintenance rituals (frontmatter audit, REM, structural audit)

When running (or the user asks to run) any of the three recurring rituals — daily (frontmatter audit → REM) or weekly (structural audit) — always scoped to one repository at a time, always presenting the plan before any write. Full procedure, execution order, and examples: **`references/routines.md`**.

## Resolving cross-repository `related`

When a document references `$alias:path.md`, resolve it by consulting the `registry.md` of the least restricted repository in the relevant scope (`hipocampo/SPEC.md`, section 6). Never edit an existing registry line when a renamed repository is found — always append a new line, preserving the old one.

## Invariants

Never override, in any instance, under any request. List and the reasoning behind each one: **`references/invariants.md`**. Full normative detail: `hipocampo/SPEC.md`, section 8.