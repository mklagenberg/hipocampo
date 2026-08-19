# Change Set — 0044–0045: Vault/entity discovery and the Bootstrap mechanic

## Summary

Resolves the forward reference `SPEC.md` section 2-C left open ("the procedure an agent uses to discover this at runtime is specified separately") and formalizes first-time instantiation as a named mechanic, closing two gaps Lote A/B (`decisions/0040`–`0043`) deliberately left for a later lote.

Adds `SPEC.md` section 12-A, "Vault and entity discovery": no repository router is stored anywhere, generic or personal — the agent reads the user's own anchor vault's manifest at session start, discovers every entity/vault address and identity field it declares, and caches the result in sensory memory for that session only. Rejects both hub-spoke and full-mesh sibling-pointer designs (both assume reciprocal access no participant is actually guaranteed) in favor of no graph between sibling vaults at all — each vault self-declares only its own `entity`/`role`/`scope_description`. See `decisions/0044-vault-and-entity-discovery.md`.

Adds `SPEC.md` section 12-B, "Bootstrap mechanic: instantiation and profile.md": classifies first-time instantiation as a fourth mechanic (`SPEC.md` section 5-D), event-triggered on "discovery attempted, nothing found" rather than scheduled. Four actions — Select, Orient (conversational, first vault only), Instantiate (the existing scaffolding procedure, `skill/references/instantiation.md`), Interview — with personal-anchor-first enforced as the mechanic's own first step, not just a stated premise (`decisions/0040`). Introduces `profile.md`, a fixed-schema identity file (name, preferred name, emails, GitHub handles per entity, last-updated date) that replaces the multi-account identity table `skill/references/personalization.md` used to hold. See `decisions/0045-bootstrap-mechanic-and-profile-md.md`.

Retires the generic skill's hand-filled repository router and multi-account identity table (`skill/references/personalization.md`) — both were a second source of truth for information discovery now resolves from the vaults themselves. The one piece of information genuinely irreducible to discovery — which repository is the user's own anchor vault — remains local, but this Change Set does not name where it lives; that stays an explicitly open item.

Adds two new reference artifacts, consumed by the Bootstrap mechanic rather than read standalone: `docs/getting-started-non-technical.md` (conversational onboarding content for the Orient action, including platform-specific installation notes) and `docs/invite-template.md` (static text for bringing someone into an entity, triggering Bootstrap in the recipient).

Updates every direct consumer of the retired router: `GETTING-STARTED.md` (section 2, instantiation steps — also corrects stale `domain`/deprecated-`tier`-value wording left over from before Lote A fully propagated), `docs/FUNDAMENTALS.md` (replaces the dead "Use this template" step-by-step with the current agent-driven flow), `skill/SKILL.md`, `skill/references/instantiation.md`, and `scaffold/skeleton/POST-INSTANTIATION.md` (also corrects a stale `instance.domain`/`instance.tier` reference to the current `instance.entity`/`instance.role` fields, a Lote A propagation gap found while editing the same section).

This is Lote C of the v2.0.0 taxonomy revision sequencing (`decisions/0040` through `0043` are Lotes A and B). Depends on both landing first — section 5-D's mechanic taxonomy (Lote B) and section 2-C's entity/vault vocabulary (Lote A) are referenced throughout `decisions/0044`/`0045` and the new `SPEC.md` sections.

## Class

**normative** — introduces a new runtime procedure (discovery) and a new mechanic (Bootstrap) with its own trigger condition, a new file schema (`profile.md`), and retires an existing operational mechanism (the router table) in favor of it.

## Semver

**minor** — no existing instance's manifest or document frontmatter becomes invalid with no action. `profile.md` is a wholly new, opt-in file; nothing currently declares it, so nothing currently lacks it in a way the schema now rejects. The retired router table lives only in each user's personal skill copy, outside this repository's own validity (`decisions/0025` — the generic `skill/` folder here has no functional effect on any content repository, per prior lotes' Change Sets). Per `decisions/0023`'s operational test, this is MINOR, not MAJOR.

## Triggers fired

| Trigger | Triggered? | Note |
|---|---|---|
| `regra_normativa` | Yes | Two new `SPEC.md` sections (12-A, 12-B), a fourth mechanic added to section 5-D, and a resolved forward reference in section 2-C. |
| `schema_frontmatter` | Yes | `profile.md` is a new, fixed-schema file, formally specified in `SPEC.md` section 12-B — not document frontmatter proper (section 2), but the same schema-field discipline applies, per the precedent set by `changes/0040-0041-multi-vault-entity-model/` for `hipocampo.yaml`. |
| `mecanismo_cross_repositorio` | No | Sections 6 (Registry) and 13 (Promote/Depromote/Redbutton) are unchanged — section 12's multi-account-identity sentence is edited, but that section is outside this trigger's defined scope (sections 6/13 only). |
| `politica_dados_sensiveis` | No | Section 2-A is unchanged. |
| `release` | Reserved | Evaluated at the v2.0.0 release closing, not in this isolated Change Set. |

## Impact

See `impact.yaml`.

## Known, not addressed here

- **The bootstrap-seed pointer's name and storage location.** Explicitly left open by both `decisions/0044` and `decisions/0045` — `skill/references/personalization.md` documents a stopgap (a plain line in the file), not a designed mechanism.
- **`docs/FAQ-AND-COMMON-ERRORS.md`'s instantiation-error entries.** Still describe the pre-`decisions/0032` "Use this template" flow end to end (wrong LICENSE inherited from a template, router not filled in after using the template). A real, pre-existing staleness this Change Set's direct-consumer sweep did not extend to — the entries need a fuller rewrite than a router-reference swap, out of scope here.
- **`skill/references/instantiation.md`'s worked example.** Still uses the pre-Lote-A `domain: company`/"Instance type: corporate" vocabulary in its illustrative walkthrough. Not touched by this Change Set — a Lote A propagation gap independent of discovery/bootstrap, flagged rather than silently fixed or silently left unmentioned.
