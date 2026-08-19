# Mandatory personalization — the bootstrap seed

This generic skill (`hipocampo/skill/SKILL.md`) only knows one universal repository, the same for any user: `mklagenberg/hipocampo` (the methodology itself — spec, decisions, scaffold). It **does not** know any personal or corporate repository — hardcoding one would break the ability of any person or company to adopt the same skill.

**This file no longer holds a repository router or a multi-account identity table.** Both were retired (`decisions/0044-vault-and-entity-discovery.md`) — every entity/vault address, and every git-handle identity fact, is now discovered at the start of each session from the user's own anchor vault's manifest (`SPEC.md`, section 12-A) and, for identity specifically, from `profile.md` (`SPEC.md`, section 12-B) — never hand-filled here, and never a second source of truth that could drift from what the repositories themselves declare.

## What actually needs personalizing

One thing, and only one: which repository is the user's own personal anchor vault. This is the one piece of information discovery cannot bootstrap itself from, because it is the address of the very first manifest to read. Until a user has instantiated their personal anchor vault (`SPEC.md` section 12-B, the Bootstrap mechanic), there is nothing yet to point at.

**This is an open item, not yet resolved by the methodology.** `decisions/0044` and `decisions/0045` both note that this pointer's exact name and where it lives (a config field in this skill copy, an environment value, something else) haven't been designed. Until that's decided, whoever personalizes this copy should record the anchor vault's address in whatever form their own AI environment supports remembering between sessions — a line at the top of this file is a reasonable stopgap:

```
My personal anchor vault: [fill in: owner/repo]
```

Once the anchor vault exists and is recorded this way, every other repository — additional personal vaults, any corporate entity's vaults — is discovered automatically from there. Nothing else in this file needs to be filled in by hand.

## First use, with nothing filled in yet

If this copy has no anchor vault recorded and the user hasn't instantiated one yet, that is exactly the condition that triggers the Bootstrap mechanic (`SPEC.md` section 12-B) — the skill doesn't ask the user to fill in a table first; it walks them through creating their personal anchor vault, then records its address here.

## Example

> User: "save this decision about project X in my second brain"
>
> The agent reads the user's anchor vault manifest (discovered from the pointer above), finds which entity/vault "project X" belongs to from what that manifest declares, and confirms with the user if more than one candidate fits — it never guesses when a `scope_description` doesn't resolve the ambiguity by itself (`SPEC.md` section 12-A; section 14, "insufficient evidence").
