---
name: hipocampo
description: >
  Operates an instance of the Hipocampo methodology (agentic second brain: git + markdown
  + AI rituals) via the GitHub MCP. Trigger when the user asks to consult,
  save, log, update, archive, or organize knowledge in any
  personal or corporate Hipocampo repository; to run the frontmatter audit, the
  REM ritual, or the weekly structural audit; to instantiate a new vault from
  a scaffold profile (`scaffold/profiles/`); to resolve `$alias:path.md`
  cross-repository; to run the Bootstrap mechanic when no personal anchor vault is
  discovered yet; or at the start of a session, to check whether a new version of the
  methodology has been published. Generic template — does not hardcode the name of any personal or
  corporate repository; requires a local anchor pointer before first real use (see
  `references/personalization.md`).
---

# Hipocampo Skill

Operates any instance of the [Hipocampo](https://github.com/mklagenberg/hipocampo) methodology via the GitHub MCP. Published as a generic template at `hipocampo/skill/SKILL.md` — **never use it without a configured local anchor pointer.**

**Hipocampo version this copy follows:** ^2.1.0 (see `hipocampo/CHANGELOG.md`). Confirm it matches the instance manifest. See also `manifest.yaml`, in this same directory, for the machine-readable compatibility range.

This file is just the router — each section below says when to act and points to the reference file with the full procedure. The norms themselves (schema, rules, rationale) live in `hipocampo/SPEC.md` and the Decision Records — this skill never re-explains them, it only operates them.

## Before first use: local anchor state

This copy only knows one universal repository (`mklagenberg/hipocampo`) — no personal or corporate repository. Read **`references/personalization.md`** and record the one thing that stays genuinely local: `anchor_repository`, the address of the user's own personal anchor vault. Store it only in the host adapter's local-state file, never in this source file or a repository. Everything else is discovered from registered addresses in that anchor at session start.

## Discovering vaults and entities (session start)

Before operating on any real knowledge, read the manifest of the user's own anchor vault. Read every address in its `discovery.registered_repositories` list, then read each target manifest for entity, role, scope, and identity metadata. Cache the result only in sensory memory for the session. If no anchor vault is recorded, Bootstrap is triggered; if an existing anchor cannot be read, report the unavailable source rather than treating it as Bootstrap. Full procedure: `hipocampo/SPEC.md`, section 12-A.

## Registering an invited vault

An invitation does not establish trusted discovery. Read the invited repository's manifest first, present its address and declared scope, and write only its address into the personal anchor's `discovery.registered_repositories` after the user explicitly confirms. Never copy entity, role, or scope into the anchor and never infer registration from access alone.

## Bootstrap: first-time instantiation

When discovery above finds no personal anchor vault: walk the user through creating one first, even if what actually brought them here was an invitation to someone else's entity — a personal anchor is always the prerequisite, never optional. Four actions in order: Select, Orient (conversational, first vault only), Instantiate (skeleton), Interview (`profile.md`, then Instantiate content, through the usual write gate). Full procedure: `hipocampo/SPEC.md`, section 12-B; `decisions/0045-bootstrap-mechanic-and-profile-md.md`.

## Checking for a new release (session start)

Compare the version declared in this instance's `AGENTS.md`/`hipocampo.yaml` against the version published in `mklagenberg/hipocampo/SPEC.md`. If there is a difference: report both versions, and point to **[`hipocampo/UPGRADE.md`](https://github.com/mklagenberg/hipocampo/blob/main/UPGRADE.md)** as the next step — a cumulative, idempotent checklist of what the instance needs to become conformant, already classified into Mandatory/Recommended/Informative. Never summarize the `CHANGELOG.md` on the spot trying to reconstruct that synthesis work — `UPGRADE.md` already exists exactly for that (decision 0024). Never apply the update on your own — point the decision to the user, citing `MIGRATIONS.md` if it is MAJOR. If the instance already has a `hipocampo.yaml` (decision 0033), record the check result in that file's `state` field, instead of just stating the result in conversation.

## Updating this skill

This skill has its own version, independent from the methodology compatibility range. Check update availability through the canonical `skill/manifest.yaml`; verify an offered package only from the immutable release tag named there, using `skill/package-lock.yaml` and its SHA-256 hashes. Do not use `source_commit` as a self-referential update hash, do not install unverified `main` content, and never self-update. Report the version/hash difference and wait for the operator's confirmation before changing client-local files.

## Creating an invite

When the user asks to invite someone into a vault (e.g., "create an invite for [name] to access [entity/vault]"): fill in the appropriate variant from `hipocampo/docs/invite-template.md` — the user doesn't need to open that file by hand. Default the invite's language to the target vault's own declared `instance.language` (`hipocampo.yaml`), never to the language of the conversation asking for it or to English by default; only use a different language on explicit request. This produces text for the human to send elsewhere — it writes nothing to any repository, so it doesn't go through invariant 5's write-confirmation gate, though presenting the filled-in text before the user copies it elsewhere is still good practice. Full procedure: `hipocampo/docs/invite-template.md`.

## Instantiating a new vault

When the user asks to create a new content repository: read the corresponding profile at `hipocampo/scaffold/profiles/pessoal.yaml` or `hipocampo/scaffold/profiles/empresa.yaml`, collect the declared inputs (repository name, `curation_level`, owner identity) directly from the user, and generate the declared outputs via the GitHub MCP — never copying someone else's file without review, always presenting the full plan before any write (invariant 5). The profile supplies the manifest's `policy_profile`; never duplicate it in `AGENTS.md`. This is the **Instantiate (skeleton)**/**Instantiate (content)** portion of the Bootstrap mechanic above when it's a user's very first vault; the same procedure, called directly, for any later one. Full procedure: **`references/instantiation.md`**.

## Reading and writing documents (CRUD)

When consulting, creating, updating, or archiving any document: read the frontmatter first, the body only when necessary; every read validates frontmatter and staleness in real time, even outside a scheduled ritual. Full procedure and example: **`references/crud-frontmatter.md`**.

For new content and content touched by CRUD or REM, enforce the current privacy rule: never retain credentials or non-public financial values; a public financial value needs its public URL and date citation. Do not interpret a methodology update as authorization to inspect every historical document — flag on READ and remediate only through a confirmed UPDATE or REM plan.

## Maintenance rituals (frontmatter audit, REM, structural audit)

When running (or the user asks to run) any of the three recurring rituals — daily (frontmatter audit → REM) or weekly (structural audit) — always scoped to one repository at a time, always presenting the plan before any write. Full procedure, execution order, and examples: **`references/routines.md`**.

## Resolving cross-repository `related`

When a document references `$alias:path.md`, resolve it by consulting the `registry.md` of the least restricted repository in the relevant scope (`hipocampo/SPEC.md`, section 6). Never edit an existing registry line when a renamed repository is found — always append a new line, preserving the old one.

## Invariants

Never override, in any instance, under any request. List and the reasoning behind each one: **`references/invariants.md`**. Full normative detail: `hipocampo/SPEC.md`, section 8.
