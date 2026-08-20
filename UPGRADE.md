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
- [ ] **[Recommended, since v2.1.0]** `hipocampo.yaml` declares `instance.policy_profile` (`personal` or `corporate`) — the sole criterion the structural audit uses to select the sensitive-data policy. A legacy `AGENTS.md` “Instance type” declaration remains readable until this manifest field is added; never keep both as active sources of truth.
- [ ] **[Mandatory, since v2.0.0]** This repository **does not have** its own `skill/` folder. The skill always runs client-side, per person/AI environment — never per repository (see `decisions/0025-skill-is-client-side-never-per-repository.md`). If your instance still carries a `skill/` folder (inherited from the old "Use this template"), delete it — it never had a functional effect, and keeping it suggests a wrong mental model ("each repo has its own skill").
- [ ] **[Recommended, since v2.1.0]** The installed skill is version 1.1.0 or newer and keeps only `anchor_repository` in host-local state. It does not maintain a repository router or identity table.
- [ ] **[Recommended, since v2.1.0]** The personal anchor's manifest registers each externally invited repository as an address in `discovery.registered_repositories`, only after the operator confirms the target manifest and scope.
- [ ] **[Recommended, if applicable — SPEC section 12]** If you operate more than one git account resolving to the same human author, that relationship is recorded in the personal instance's `AGENTS.md`/`profile.md`, never in a local skill router.
- [ ] **[Recommended, since v2.1.0]** This repository has a `hipocampo.yaml` manifest at its root with `instance.entity`, `instance.role`, `instance.policy_profile`, `instance.curation_level`, and scaffold provenance. If it predates v2.1.0, `instance.tier` remains valid until you explicitly replace it with `curation_level`.
- [ ] **[Mandatory, since v2.0.0, breaking]** If your instance's `hipocampo.yaml` still declares `instance.domain` (the pre-v2.0 field), it no longer satisfies the current schema — migrate to `instance.entity`/`instance.role`/`instance.scope_description`. See `MIGRATIONS.md`, "Entity model replaces `domain`", and `decisions/0041-entity-model-and-vault-vocabulary.md`.
- [ ] **[Recommended, since v2.0.0]** This repository's `hipocampo.yaml` declares `instance.language` — the BCP-47 tag for the language this vault's content is actually written in. This is independent of `hipocampo`'s own language (English, `decisions/0034-repository-and-vault-language-policy.md`) — most real vaults are not English. If your instance's `hipocampo.yaml` predates this field, add it now with the vault's real content language, not the scaffold's `"en"` default.
- [ ] **[Recommended, since v2.1.0]** After `instance.policy_profile` is present, remove the duplicate “Instance type” declaration from `AGENTS.md` in the same confirmed update. Do not remove it first from a v2 manifest that has no policy profile.
- [ ] **[Informative]** The skill now publishes a machine manifest (`skill/manifest.yaml`, inside `hipocampo`) — version, compatibility, and update channel queryable by tooling. No practical effect on an existing content instance; it's only about the skill itself.

### Licensing

- [ ] **[Mandatory]** The repository's `LICENSE` is not the Apache-2.0 inherited from the template — it's the `LICENSE-pessoal` or `LICENSE-corporativo` from `scaffold/license-templates/` (the old `hipocampo-toolkit/license-templates/` was consolidated and archived, `decisions/0032`). Common bug in older instances — see `docs/FAQ-AND-COMMON-ERRORS.md`.

### Maintenance rituals

- [ ] **[Recommended, since SPEC section 5-B / v2.0.0]** Frontmatter audit (daily, deterministic) running before the REM ritual of the same cycle — cadence declared in `AGENTS.md`, "Maintenance rituals" section. See `decisions/0017-deterministic-frontmatter-audit-ritual.md`.
- [ ] **[Recommended, since SPEC section 5-A]** REM ritual (daily, two functions: consolidating `inbox/` + updating old memories) — same section of `AGENTS.md`. See `decisions/0008-rem-ritual-and-memory-layers.md` and `decisions/0016-short-term-memory-sanitization.md`.
- [ ] **[Recommended, since SPEC section 5-C / v2.0.0]** Structural audit (weekly: atomicity, placement, sensitive-data leakage) — same section of `AGENTS.md`. See `decisions/0019-weekly-structural-audit.md`.

### Privacy

- [ ] **[Recommended, progressive since v2.1.0]** Apply the current privacy rules to every new document immediately and to existing documents when they are read, updated, or processed by REM. Do not launch a repository-wide inspection merely because the methodology was updated. A finding is reported first; any remediation remains explicitly confirmed. In particular, never retain credentials or non-public financial values, and retain a public financial value only with its public URL and date citation.
- [ ] **[Informative]** There's a formal, narrow exception to the "a document is never physically deleted" invariant, for the legal obligation to erase personal data (LGPD Art. 16 / GDPR Art. 17) — always a human decision, never the agent's. See `decisions/0010-legal-deletion-exception.md`. No action needed unless the case actually occurs.

## Recommended reading, no action needed on the repository

`BEST-PRACTICES.md`, `docs/AI-MODELS.md`, `docs/PERFORMANCE-AND-GRAPH.md`, `docs/MULTI-TOOL-USAGE.md`, `docs/FAQ-AND-COMMON-ERRORS.md`, `DISCLAIMER.md` — context and best practices that don't structurally change anything in an existing instance.

## Backward-incompatible changes (MAJOR)

**v2.0.0** — one breaking schema change: `hipocampo.yaml`'s `instance.domain` → `instance.entity`/`instance.role`/`instance.scope_description` (`decisions/0041`). This is what makes v2.0.0 a MAJOR release under `decisions/0023-operational-criterion-for-semver-scope.md`'s test — every other change-set accepted in this cycle is `minor` (see each `changes/*/impact.yaml`). See `MIGRATIONS.md`, "1.x → 2.0", for the migration steps.
