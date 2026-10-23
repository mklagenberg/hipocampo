# Hipocampo — Instance Upgrade Guide

## Skill 2.4.0 candidate

The V3.1.0 methodology candidate now pairs with skill 2.4.0. The skill version
increased because its bundled instructions now ask for an explicit V3 Vault
profile, allow authorized entity reads without a personal anchor, and route
remote ingress and CRUD through verified GitHub MCP capability. Scaffold
profiles move to 2.2.0 for their changed creation contract. A change only to
methodology files referenced by the skill
does not itself change the skill version. Verify the 2.4.0 manifest, package lock,
compatibility tuple and host loading before adopting this candidate in an
explicit experimental channel. Existing client installs remain pinned until
separately updated; this does not migrate a vault or publish a release.

For a V3.0.0 vault declaring `^3.0.0`, follow the
[V3.0.0 to 3.1.0 vault procedure](docs/v3-to-v3.1-vault-upgrade.md). The
compatible minor candidate does not require Record or manifest migration.
Keep historical verification provenance and check each real operation's
host, GitHub, authority and privacy gates separately.
New Vault creation asks for `team`, `personal` or `entity`, with `team`
suggested but never filled from silence. Existing compatible V3 Vaults lacking
`instance.vault_profile` retain their previous governed route and receive a
WARNING; adopting a new profile-dependent policy is a separate, confirmed
metadata change. See [selection and recovery](docs/v3-vault-profile-selection.md).

## Bounded V2 reads from the current client

Updating the client skill/plugin does not update a vault. A verified V2.0.0,
V2.1.0, V2.1.1 or V2.2.0 source may be read through the separate
[legacy read contract](docs/legacy-read-support.md) after its adapter,
GitHub MCP, repository permission and privacy gates pass. This is operation
support, not general V2/V3 compatibility: a V2 vault remains
`migration_required` for V3 operation and V3 writes. Emit the version WARNING
and preserve the old vault unchanged. Other V2 source revisions require
their own proof and fixtures before support is claimed.

Choose installation/update per Claude, Copilot/VS Code or Codex/ChatGPT using
the [host procedure](docs/host-installation.md). Verify the effective package
and runtime in a new session; host loading is not established by local files
alone. A vault upgrade is a distinct, per-instance action.

## V3.1.0 release target

This MINOR update preserves the V3.0.0 Record data contract. A personal anchor
and registered-repository list are optional; operators may identify a target
directly and verify its current manifest and access. `personal` and `team`
profiles grant scoped methodological eligibility to propose Create, Update and
Archive, while execution still needs GitHub write, the matching MCP operation
and canonical CRUD. `entity` writes require a current, scoped representative
grant; technical GitHub write alone does not qualify. The human creator of a
new vault is representative only for that vault. Existing vaults remain
readable and keep their prior versioned authorization and CRUD path until an
operator chooses governed adoption. Adoption is needed to declare a profile or
add representative grants; it is not required to preserve prior valid writes.
See
[Decision 0121](decisions/0121-v3-remote-ingress-and-profile-write-eligibility.md).


## V3.1 executable distribution and experimental channel

Use [runtime installation](docs/v3-runtime-usage.md) and the
[channel contract](docs/v3-distribution-and-channels.md). Stable requires the
verified immutable published release. Explicit experimental use pins a source
commit/optional RC tag and hashes; it emits WARNING and allows valid canonical
engine operations without a GitHub Release or future stable publication.
No Record-schema migration is required from compatible V3.0.x; V2 adoption
retains its separate governed migration. Preserve previous installs and user
state. Do not activate globally or change an instance without authorization.


## V3.0.1 package correction — explicit adoption required

The package target is methodology 3.0.1 / skill 2.0.1 / vault ^3.0.0. V3.0.0
was published; this patch corrects stale release-state and installation
markers without changing the V3.0.0 contract or the vault compatibility range.
Verify the v3.0.1 GitHub Release reports `immutable: true`, its tag resolves
to the release target, and all package hashes match before installation or
activation.
V2 instances do not become compatible by changing a range. Keep the
appropriate immutable V2 package for legacy operation until governed migration
passes. Use per-vault inventory, complete review, accepted Collections and
exact mappings, privacy/source/context gates, canonical CRUD conversion and
fresh reload. Preserve original prose, Unicode/newlines, all legacy fields,
attachments, relations, provenance and unknown source state. Recovery requires
the exact immutable ticket and human acceptance; no direct edits or Git reset.
The scaffold creates proposal/operational structure, never a Record directly.
See [release scope](docs/v3-release-preparation.md) and
[execution procedure](docs/v3-migration-execution.md). The historical candidate
sections below retain their original boundary; this section defines the
corrected package target and does not certify host runtime or full migration.


**Cumulative and idempotent** checklist: what an instance should have, today, to be conformant with the current version of the methodology — no matter which old version it started from. Unlike `CHANGELOG.md` (chronological history of what changed) and `MIGRATIONS.md` (only MAJOR change steps, which break compatibility), this document is the practical "what to do now" list, always relative to the present. See `decisions/0024-upgrade-md-cumulative-checklist.md`.

## How to use

1. Open `AGENTS.md` (or `CLAUDE.md`, if the instance hasn't migrated yet) and check the declared version.
2. Go through the list below, item by item. Each one states whether it's **Mandatory** (invariant or safety — rare), **Recommended** (functional, but nothing breaks without it), or **Informative** (reading, no action on the repository).
3. Repeat for each repository you operate — upgrading is always per instance, never "global" (even if you have several repositories, each one advances whenever it makes sense for it).

This document is updated with every methodology release (mandatory step of the release routine, `decisions/0014` + `decisions/0024`) — always cumulative, never rewritten from scratch.

## Checklist

### Canonical file and skill

- [ ] **[Recommended, since the compatibility contract]** Before a durable operation, evaluate the tuple of client-side skill, methodology, and vault manifest through `COMPATIBILITY.yaml` when available. Continue only for `compatible` or `compatible_with_upgrade`; follow this guide or `MIGRATIONS.md` when the result is blocked. Existing vaults do not need a new field solely because this contract was introduced.

- [ ] **[Recommended, since SPEC section 11]** `AGENTS.md` is the instance's canonical instruction file — not `CLAUDE.md`. If your instance still only uses `CLAUDE.md`, create `AGENTS.md` with the complete content (invariants, scope, local extensions) and leave `CLAUDE.md` as a thin, few-line pointer. See `decisions/0015-agents-md-canonical-instruction-file.md`.
- [ ] **[Recommended, since v2.1.0]** `hipocampo.yaml` declares `instance.policy_profile` (`personal` or `corporate`) — the sole criterion the structural audit uses to select the sensitive-data policy. A legacy `AGENTS.md` “Instance type” declaration remains readable until this manifest field is added; never keep both as active sources of truth.
- [ ] **[Mandatory, since v2.0.0]** This repository **does not have** its own `skill/` folder. The skill always runs client-side, per person/AI environment — never per repository (see `decisions/0025-skill-is-client-side-never-per-repository.md`). If your instance still carries a `skill/` folder (inherited from the old "Use this template"), delete it — it never had a functional effect, and keeping it suggests a wrong mental model ("each repo has its own skill").
- [ ] **[Recommended, since v2.1.0]** The installed skill is version 1.2.0 or newer; its package is checked against the published release, tag-resolved commit and package lock, and it keeps only `anchor_repository` in host-local state. It does not maintain a repository router or identity table.
- [ ] **[Recommended, since v2.1.0]** The personal anchor's manifest registers each externally invited repository as an address in `discovery.registered_repositories`, only after the operator confirms the target manifest and scope.
- [ ] **[Recommended, if applicable — SPEC section 12]** If you operate more than one git account resolving to the same human author, that relationship is recorded in the personal instance's `AGENTS.md`/`profile.md`, never in a local skill router.
- [ ] **[Recommended, since v2.1.0]** This repository has a `hipocampo.yaml` manifest at its root with `instance.entity`, `instance.role`, `instance.policy_profile`, `instance.curation_level`, and scaffold provenance. If it predates v2.1.0, `instance.tier` remains valid until you explicitly replace it with `curation_level`.
- [ ] **[Mandatory, since v2.0.0, breaking]** If your instance's `hipocampo.yaml` still declares `instance.domain` (the pre-v2.0 field), it no longer satisfies the current schema — migrate to `instance.entity`/`instance.role`/`instance.scope_description`. See `MIGRATIONS.md`, "Entity model replaces `domain`", and `decisions/0041-entity-model-and-vault-vocabulary.md`.
- [ ] **[Recommended, since v2.0.0]** This repository's `hipocampo.yaml` declares `instance.language` — the BCP-47 tag for the language this vault's content is actually written in. This is independent of `hipocampo`'s own language (English, `decisions/0034-repository-and-vault-language-policy.md`) — most real vaults are not English. If your instance's `hipocampo.yaml` predates this field, add it now with the vault's real content language, not the scaffold's `"en"` default.
- [ ] **[Recommended, since v2.1.0]** After `instance.policy_profile` is present, remove the duplicate “Instance type” declaration from `AGENTS.md` in the same confirmed update. Do not remove it first from a v2 manifest that has no policy profile.
- [ ] **[Informative]** The skill now publishes a machine manifest (`skill/manifest.yaml`, inside `hipocampo`) — version, compatibility, and update channel queryable by tooling. No practical effect on an existing content instance; it's only about the skill itself.

### Licensing

- [ ] **[Mandatory]** The repository's `LICENSE` is not the Apache-2.0 inherited from the template — it's the `LICENSE-pessoal` or `LICENSE-corporativo` from `scaffold/license-templates/` (the old `hipocampo-toolkit/license-templates/` was consolidated and archived, `decisions/0032`). Common bug in older instances — see `docs/FAQ-AND-COMMON-ERRORS.md`.
- [ ] **[Mandatory, security correction since v2.1.1]** The content `LICENSE` is strictly private and proprietary for its declared owner. `visibility: public` and legacy `LicenseRef-*-Public` identify only the least-restricted handling class among already authorized users; they never authorize external publication, copying, redistribution, sublicensing, or a public repository. Update this root artifact without using the methodology update as a reason to inspect or rewrite every historical document.

### Maintenance rituals

- [ ] **[Recommended, since SPEC section 5-B / v2.0.0]** Frontmatter audit (daily, deterministic) running before the REM ritual of the same cycle — cadence declared in `AGENTS.md`, "Maintenance rituals" section. See `decisions/0017-deterministic-frontmatter-audit-ritual.md`.
- [ ] **[Recommended, since SPEC section 5-A]** REM ritual (daily, two functions: consolidating `inbox/` + updating old memories) — same section of `AGENTS.md`. See `decisions/0008-rem-ritual-and-memory-layers.md` and `decisions/0016-short-term-memory-sanitization.md`.
- [ ] **[Recommended, since v2.1.0]** Structural audit (weekly: atomicity, placement, privacy/security/provenance, and repository-level controlled vocabulary) — same section of `AGENTS.md`. See `decisions/0019-weekly-structural-audit.md`.

### Privacy

- [ ] **[Recommended, progressive since v2.1.0]** Apply the current privacy rules to every new document immediately and to existing documents when they are read, updated, or processed by REM. Do not launch a repository-wide inspection merely because the methodology was updated. A finding is reported first; any remediation remains explicitly confirmed. In particular, never retain credentials or non-public financial values, and retain a public financial value only with its public URL and date citation.
- [ ] **[Informative]** There's a formal, narrow exception to the "a document is never physically deleted" invariant, for the legal obligation to erase personal data (LGPD Art. 16 / GDPR Art. 17) — always a human decision, never the agent's. See `decisions/0010-legal-deletion-exception.md`. No action needed unless the case actually occurs.

## Recommended reading, no action needed on the repository

`BEST-PRACTICES.md`, `docs/AI-MODELS.md`, `docs/PERFORMANCE-AND-GRAPH.md`, `docs/MULTI-TOOL-USAGE.md`, `docs/FAQ-AND-COMMON-ERRORS.md`, `DISCLAIMER.md` — context and best practices that don't structurally change anything in an existing instance.

## Backward-incompatible changes (MAJOR)

**v2.0.0** — one breaking schema change: `hipocampo.yaml`'s `instance.domain` → `instance.entity`/`instance.role`/`instance.scope_description` (`decisions/0041`). This is what makes v2.0.0 a MAJOR release under `decisions/0023-operational-criterion-for-semver-scope.md`'s test — every other change-set accepted in this cycle is `minor` (see each `changes/*/impact.yaml`). See `MIGRATIONS.md`, "1.x → 2.0", for the migration steps.
