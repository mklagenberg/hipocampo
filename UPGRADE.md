# Hipocampo — Instance Upgrade Guide

**Cumulative and idempotent** checklist: what an instance should have, today, to be conformant with the current version of the methodology — no matter which old version it started from. Unlike `CHANGELOG.md` (chronological history of what changed) and `MIGRATIONS.md` (only MAJOR change steps, which break compatibility), this document is the practical "what to do now" list, always relative to the present. See `decisions/0024-upgrade-md-cumulative-checklist.md`.

## How to use

1. Open `AGENTS.md` (or `CLAUDE.md`, if the instance hasn't migrated yet) and check the declared version.
2. Go through the list below, item by item. Each one states whether it's **Mandatory** (invariant or safety — rare), **Recommended** (functional, but nothing breaks without it), or **Informative** (reading, no action on the repository).
3. Repeat for each repository you operate — upgrading is always per instance, never "global" (even if you have several repositories, each one advances whenever it makes sense for it).

This document is updated with every methodology release (mandatory step of the release routine, `decisions/0014` + `decisions/0024`) — always cumulative, never rewritten from scratch.

## Checklist

### Canonical file and skill

- [ ] **[Recommended, since SPEC section 11]** `AGENTS.md` is the instance's canonical instruction file — not `CLAUDE.md`. If your instance still only uses `CLAUDE.md`, create `AGENTS.md` with the complete content (invariants, scope, local extensions) and leave `CLAUDE.md` as a thin, few-line pointer. See `decisions/0015-agents-md-canonical-instruction-file.md`.
- [ ] **[Recommended, since SPEC section 11 + 2-A]** The "Scope of this repository" block in `AGENTS.md` declares the **Instance type** (`corporativa` or `pessoal`) — the criterion the structural audit uses to know which variant of the sensitive-data policy applies. See `decisions/0022-instance-type-declared-in-agents-md.md`.
- [ ] **[Mandatory, since unreleased v1.9]** This repository **does not have** its own `skill/` folder. The skill always runs client-side, per person/AI environment — never per repository (see `decisions/0025-skill-is-client-side-never-per-repository.md`). If your instance still carries a `skill/` folder (inherited from the old "Use this template"), delete it — it never had a functional effect, and keeping it suggests a wrong mental model ("each repo has its own skill").
- [ ] **[Recommended, since v1.7.0]** The skill installed in your AI environment is the real, personalized version (`skill/SKILL.md` + `skill/references/`, now inside `hipocampo` itself — the old `hipocampo-toolkit` was consolidated and archived, `decisions/0032`) — not the "stub" from versions before v1.7.0. Reinstall via `save_skill` (or your tool's equivalent mechanism) if your copy is old.
- [ ] **[Recommended, since SPEC section 11 / unreleased v1.9]** The repository router (`skill/references/personalization.md` in your personal skill copy) lists **every** repository you operate — including the rarely-touched ones. It's the list any future version audit will use.
- [ ] **[Recommended, if applicable — SPEC section 12]** If you operate more than one git account resolving to the same human author (e.g., personal and one tied to an employer), that relationship is recorded in the personal instance's `AGENTS.md` and in the personalized skill's router — never in the generic copy. See `decisions/0020-multi-account-author-identity.md`.
- [ ] **[Recommended, since unreleased v1.9]** This repository has a `hipocampo.yaml` manifest at its root (`decisions/0033-hipocampo-yaml-per-vault-manifest.md`), with `instance.domain`/`instance.tier` filled in and the provenance of the scaffold that generated it (`scaffold.profile`, `scaffold.source_commit`). If your instance doesn't have one, generate one from `scaffold/skeleton/hipocampo.yaml` and fill in the fields — no automatic action does this retroactively for you.
- [ ] **[Informative]** The "Instance type" field in `AGENTS.md` (`corporativa`/`pessoal`) uses different vocabulary from the `hipocampo.yaml` `instance.domain` field (`pessoal`/`empresa`, `decisions/0029`). The divergence is known, documented in `decisions/0033-hipocampo-yaml-per-vault-manifest.md`, and deliberately not yet harmonized — no action needed beyond being aware.
- [ ] **[Informative]** The skill now publishes a machine manifest (`skill/manifest.yaml`, inside `hipocampo`) — version, compatibility, and update channel queryable by tooling. No practical effect on an existing content instance; it's only about the skill itself.

### Licensing

- [ ] **[Mandatory]** The repository's `LICENSE` is not the Apache-2.0 inherited from the template — it's the `LICENSE-pessoal` or `LICENSE-corporativo` from `scaffold/license-templates/` (the old `hipocampo-toolkit/license-templates/` was consolidated and archived, `decisions/0032`). Common bug in older instances — see `docs/FAQ-AND-COMMON-ERRORS.md`.

### Maintenance rituals

- [ ] **[Recommended, since SPEC section 5-B / unreleased v1.9]** Frontmatter audit (daily, deterministic) running before the REM ritual of the same cycle — cadence declared in `AGENTS.md`, "Maintenance rituals" section. See `decisions/0017-deterministic-frontmatter-audit-ritual.md`.
- [ ] **[Recommended, since SPEC section 5-A]** REM ritual (daily, two functions: consolidating `inbox/` + updating old memories) — same section of `AGENTS.md`. See `decisions/0008-rem-ritual-and-memory-layers.md` and `decisions/0016-short-term-memory-sanitization.md`.
- [ ] **[Recommended, since SPEC section 5-C / unreleased v1.9]** Structural audit (weekly: atomicity, placement, sensitive-data leakage) — same section of `AGENTS.md`. See `decisions/0019-weekly-structural-audit.md`.

### Privacy

- [ ] **[Informative]** There's a formal, narrow exception to the "a document is never physically deleted" invariant, for the legal obligation to erase personal data (LGPD Art. 16 / GDPR Art. 17) — always a human decision, never the agent's. See `decisions/0010-legal-deletion-exception.md`. No action needed unless the case actually occurs.

## Recommended reading, no action needed on the repository

`BEST-PRACTICES.md`, `docs/AI-MODELS.md`, `docs/PERFORMANCE-AND-GRAPH.md`, `docs/MULTI-TOOL-USAGE.md`, `docs/FAQ-AND-COMMON-ERRORS.md`, `DISCLAIMER.md` — context and best practices that don't structurally change anything in an existing instance.

## Backward-incompatible changes (MAJOR)

None so far. When a MAJOR change is accepted (criterion in `decisions/0023-operational-criterion-for-semver-scope.md`), the mandatory migration steps go into `MIGRATIONS.md`, not this file.