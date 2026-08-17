# Hipocampo — Changelog

Version history of the methodology itself. Follows [SemVer](https://semver.org/lang/pt-BR/) — see SPEC.md, section 9.

## [Unreleased]

Work accumulated on `main`, not yet tagged/released — see `decisions/0021-release-cadence-policy.md`. Becomes a real versioned section once the release is cut.

### Added
- **`scripts/validate_hipocampo.py`** (new, Fase G) — dependency-free deterministic validation of the methodology repository's own structure: Decision Record template compliance (canonical DRs vs. bilingual redirect stubs), internal markdown link resolution (file existence + GitHub-slug heading-anchor matching), README/CHANGELOG version consistency, and a non-blocking coverage report cross-referencing every `SPEC.md` section 2 schema field against canonical Decision Records. Closes MODA self-audit major finding 4. See `decisions/0036-deterministic-validation-of-repository-structure.md`.
- **`.github/workflows/validate.yml`** (new) — runs `scripts/validate_hipocampo.py` on every PR against `main` and on push to `main`.
- **`RELEASE-CHECKLIST.md`** (new, Fase G) — minimal release-gate checklist expanding `decisions/0014`/`0021`/`0023` into a single concrete run-through (scope classification, validation gate, dated CHANGELOG, version consistency, migration check, `UPGRADE.md` review, skill/scaffold self-sync, Change Sets accounted for, tag+Release together, merge-landed-on-main confirmation). Closes MODA self-audit minor finding 2. See `decisions/0037-minimal-release-gate-checklist.md`.
- **`decisions/0036-deterministic-validation-of-repository-structure.md`**, **`decisions/0037-minimal-release-gate-checklist.md`** (new) — the two Decision Records above.
- **`changes/0036-0037-deterministic-validation-and-release-gate/`** (new) — combined Change Set for both.
- `SPEC.md`, section 9: now points to `RELEASE-CHECKLIST.md` and `scripts/validate_hipocampo.py`; "`hipocampo-toolkit` synchronization" corrected to "skill/scaffold synchronization", reflecting the consolidation from `decisions/0032`.
- `docs/change-management.md`: "Deterministic and human checking" section updated — structural integrity is now deterministic/CI-checked; Change Set semantic completeness remains human review, unchanged.
- `AGENTS.md` (root): the stale "no deterministic validation exists" working rule corrected to point to the new script; new change-protocol item pointing to `RELEASE-CHECKLIST.md`.
- `moda.yaml`: new `structural_validation`/`release_checklist` documentation entries and a new `structural-validation` component.
- `conformance/moda.yaml`: `repository_contract` control evidence/notes updated to reflect the new script, CI workflow, and checklist — status stays `partial` by design (no branch-protection rule declared, MODA's full release-gate model deliberately not adopted).
- Fixed `decisions/0034-repository-and-vault-language-policy.md` and `decisions/0035-controlled-vocabulary-dictionary.md`: both were missing the leading `NNNN — ` number in their title line, a template defect surfaced by testing `scripts/validate_hipocampo.py` against the real repository.
- **English translation** (Fase E, PR #27) — the entire `hipocampo` repository (`SPEC.md`, all Decision Records, `docs/`, `changes/`, `skill/` including `references/`, `scaffold/` including `skeleton/`) translated from Brazilian Portuguese to English. Every renamed file leaves a bilingual redirect stub at its old path — never deleted, per the "a document is never physically deleted" invariant (`SPEC.md`, section 8). Scope: only this repository — vaults and personal skill copies remain in their own language. See `decisions/0034-repository-and-vault-language-policy.md`.
- **`decisions/0034-repository-and-vault-language-policy.md`** (new) — codifies two things: `hipocampo` (this repository) is maintained in English going forward, not just for the one-time Fase E translation; and every vault's `hipocampo.yaml` now declares its own content language via a new `instance.language` field (BCP-47 tag), independent of `hipocampo`'s own language, defaulting to `"en"` (the scaffold's default) for a newly instantiated vault.
- **`changes/0034-repository-and-vault-language-policy/`** (new) — Change Set for the above.
- **`decisions/0035-controlled-vocabulary-dictionary.md`** (new) — makes English the canonical vocabulary for every remaining controlled-vocabulary field (`source`, `domain`, exposure `tier`, curation-level `tier`, `AGENTS.md`'s "Instance type") — the deviation flagged in PR #27 for not translating these. Every deprecated pt-BR value remains permanently valid via a new de:para reference, `docs/vocabulary-dictionary.md`; migration of existing documents/instances is opportunistic, driven by the same maintenance rituals that already handle `ttl` expiry — never bulk, never silent.
- **`docs/vocabulary-dictionary.md`** (new) — the de:para table plus usage instructions for the above; also names, without resolving, two pre-existing inconsistencies found while building it: `tier` names two different concepts (exposure tier vs. curation-level tier) across `decisions/0029` and `decisions/0033`; and `domain`/`AGENTS.md`'s "Instance type" remain two separate, unharmonized vocabularies (already known per `decisions/0033`).
- **`changes/0035-controlled-vocabulary-dictionary/`** (new) — Change Set for the above.
- `SPEC.md`: sections 2, 2-B, 2-C, 5-A, 5-B, 5-C, 11, 13 updated for the new canonical vocabulary and the ritual-driven normalization mechanism.
- `skill/references/routines.md`: frontmatter audit and REM ritual descriptions gain deprecated-vocabulary detection/normalization; structural audit gains a fourth function for repository-level fields (`AGENTS.md`, `hipocampo.yaml`) not covered by the per-document frontmatter audit.
- `skill/references/instantiation.md`: domain/tier/Instance type values updated to canonical English; flags the pre-existing `tier` concept mismatch between this file and the scaffold profile's actual enum.
- `scaffold/profiles/pessoal.yaml`, `scaffold/profiles/empresa.yaml`: `tier` enum `conteudo`/`vault` → `content`/`vault`; `domain` fixed values → `personal`/`company`.
- `scaffold/skeleton/hipocampo.yaml`, `scaffold/skeleton/AGENTS.md`: fill-in placeholders updated to canonical English values; vocabulary-note comments rewritten to reference `decisions/0035`.
- `scaffold/skeleton/hipocampo.yaml`: new `instance.language` field, pre-filled `"en"`.
- `scaffold/profiles/pessoal.yaml`, `scaffold/profiles/empresa.yaml`: new optional `language` input, default `"en"`.
- `skill/references/instantiation.md`: the instantiation procedure now confirms the vault's content language with the operator instead of silently assuming the default.
- **`scaffold/`** (new) — vault instantiation mechanism consolidated from the former `hipocampo-toolkit` repository, as a declarative scaffold per MODA (`docs/composition-scaffolding-and-distribution.md`): two profiles per domain (`scaffold/profiles/pessoal.yaml`, `scaffold/profiles/empresa.yaml`, with `tier` as input), `scaffold/skeleton/` with the source content for each output, `scaffold/license-templates/` migrated without changes to legal content. See `decisions/0032-toolkit-consolidation-into-scaffolding.md`.
- **`skill/`** (migrated into `hipocampo`) — the methodology's operational skill, previously hosted only in `hipocampo-toolkit`, now lives in `hipocampo/skill/` (`SKILL.md` + `references/crud-frontmatter.md`, `invariants.md`, `personalization.md`, `routines.md`, and the new `references/instantiation.md`). The `skill/` folder is no longer copied into new content repositories — it never had a functional effect there (`decisions/0025`).
- **`skill/manifest.yaml`** (new) — machine manifest for the skill, following the MODA `skill-manifest.yaml` pattern, honestly adapted: no independently packaged/distributed version yet (only the personal client-side copy, `decisions/0025`).
- **`skill/references/instantiation.md`** (new) — complete procedure for agent-driven instantiation of a new vault: profile selection, input collection, presenting the plan before writing (invariant 5), output generation, conflict behavior.
- **`hipocampo.yaml`** (new format, per vault) — machine-readable manifest that every vault generated by the scaffold now carries at the root: provenance (profile, source commit, engine version), `instance.domain`/`instance.tier`, `state`. See `decisions/0033-hipocampo-yaml-per-vault-manifest.md`. The vocabulary divergence between `instance.domain` (`pessoal`/`empresa`) and the "Instance type" field in `AGENTS.md` (`pessoal`/`corporativa`) is recorded as a known pending item, not harmonized in this phase.
- **`changes/0032-0033-scaffolding-and-vault-manifest/`** (new) — prospective Change Set covering `decisions/0032` and `decisions/0033`, the first exercise of the mechanism (`decisions/0031`) outside backfill mode.
- `moda.yaml`: the `personal-skill` component moves from `independent` lifecycle (hosted in `hipocampo-toolkit`) to `embedded`; new `vault-scaffold` and `vault-manifest` components; new local `skill` and `scaffold` packages in `packages`. `artifact.language` corrected from `"pt-BR"` to `"en"`, reflecting Fase E; stale Portuguese `SPEC.md#...` anchor fragments — left over from before the section headers themselves were translated — corrected across `moda.yaml` and `conformance/moda.yaml`; `conformance/moda.yaml`'s `distribution_of_agency` evidence path corrected from the old `skill/references/instanciacao.md` to `skill/references/instantiation.md`.
- `conformance/moda.yaml`: the `packaging_and_synchronization` control is reassessed in light of `skill/manifest.yaml` and the per-vault `hipocampo.yaml` (still `partial` — no existing real vault has been retroactively updated yet); the `specification_driven_change_control` control gains a second piece of evidence (prospective Change Set, not just backfill); the `distribution_of_agency`, `contracts`, and `repository_contract` controls gain new evidence regarding the scaffold.
- `README.md`, `GETTING-STARTED.md` (sections 1 and 2), `UPGRADE.md`: all references to `hipocampo-toolkit` updated to point to the consolidated `scaffold/`; `GETTING-STARTED.md` section 2 rewritten from scratch for the agent-driven model (no "Use this template" button); `UPGRADE.md` gains new checklist items (`hipocampo.yaml`, `skill/manifest.yaml`, `domain`/"Instance type" vocabulary divergence).
- **`docs/change-management.md`** (new) — Change Set mechanism adopted from MODA and adapted to Hipocampo's vocabulary: `editorial`/`operational`/`normative` classes, `changes/<change-id>/` structure (`proposal.md` + `impact.yaml`), its own trigger table. Becomes mandatory for `operational`/`normative` changes from now on. See `decisions/0031-change-set-mechanism.md`.
- **`changes/0026-0028-fact-account-opinion-memory-taxonomy-and-cross-repo-lifecycle/`** (new) — retroactive (backfill) Change Set for PR #22, first validation exercise for the template.
- **`moda.yaml`** (new, root) — formal declaration of retrospective conformance with [MODA](https://github.com/mklagenberg/moda): `relationship: audited_against`, `adoption_mode: retrospective`, `claim_stage: mapped`, `conformance_result: partial`. First artifact of the methodology's alignment with MODA toward v2.0.0.
- **`conformance/moda.yaml`** (new) — control-by-control mapping against MODA's design dimensions (MODA SPEC, section 4) and the repository contract (section 5), reflecting the findings of the 2026-08-17 audit.
- **`audits/moda/2026-08-17-v1.0.0-self-audit.md`** (new) — MODA conformance audit frozen as immutable evidence.
- **`AGENTS.md`** (new, root) — agent entry point for contributing to the methodology itself, distinct from the `AGENTS.md` that each content instance uses for itself (SPEC.md, section 11). Closes audit major finding 2.
- **`ROADMAP.md`** (new, root) — outcome-based direction, without duplicating the backlog (`decisions/`) or the changelog. Closes audit major finding 3.
- `README.md`: MODA disclosure (section 5.1 of the MODA SPEC) — artifact profile, compatibility, adoption relationship, links to the manifest/conformance profile/audit.
- SPEC.md, section 2-C (new): **repository type taxonomy** — two orthogonal axes, domain of ownership (`pessoal`/`empresa`, already in use via `decisions/0002`) and exposure tier (`confidencial`/`público`), mapping without a new repository onto the four real content repositories. New frontmatter field `curation_status` (section 2), relevant only in `empresa-confidencial` repositories — `staged` (candidate for future promotion) or `permanent` (default). See `decisions/0029-repository-type-taxonomy.md`.
- SPEC.md, section 13 (Promote): generalized to also cover graduation within the same ownership domain (an `empresa-confidencial` document with `curation_status: staged` being promoted to `empresa-público`), always via the elegant path — the literal path remains exclusive to the cross-domain case, because only there is there real transfer of ownership at stake. See `decisions/0030-promote-same-domain-graduation.md`.
- SPEC.md, section 2: `contributors` field (added to the schema's central listing — already existed via `decisions/0006`, but never appeared in the main listing) and `contains_subjective_content` (new, relevant only when `owner` is filled in). Four-type information taxonomy — **Fact**, **Account**, **Opinion**, **Memory** — used as an inline label in mixed documents; `contains_subjective_content` covers only Opinion/Memory, the two categories with personal-liability risk. Inline `@handle` only when there is more than one contributor. New Opinion/Memory content is written to a corporate instance only with the user's explicit confirmation — without that, it goes to the personal instance. Also applies to the REM ritual's consolidation function (section 5-A) and to the Promote action (section 13). See `decisions/0026-account-vs-opinion-in-corporate-instance.md`.
- SPEC.md, section 13 (new): **Promote, Depromote, Redbutton** — cross-repository lifecycle actions. Promote (personal → corporate) with two paths (elegant derivation via `decisions/0011`, or literal transfer with explicit ownership warning per `decisions/0007`); Depromote (downgrade within the same ownership domain); Redbutton (remediation of a 2-A policy violation). `superseded_by` (section 2/6) now accepts cross-repository `$alias:` syntax. See `decisions/0027-promote-depromote-redbutton.md`.
- SPEC.md, section 8: the trigger for the exception to invariant 3 (`decisions/0010`) is broadened to also cover a 2-A policy violation identified by structural audit or by the operator, without requiring a formal request from the data subject. See `decisions/0028-broadened-trigger-2a-remediation.md`.
- SPEC.md, section 5-B: **frontmatter audit** — deterministic ritual (script, not AI judgment), recommended daily cadence, runs before the REM, produces `meta/fila-de-manutencao.md`. See `decisions/0017-deterministic-frontmatter-audit-ritual.md`.
- SPEC.md, section 5-C: **weekly structural audit** — atomicity, placement, and sensitive-data leak checking against the per-instance-type policy (first enforcement mechanism for DR0009). See `decisions/0019-weekly-structural-audit.md`.
- SPEC.md, section 11: **AGENTS.md as the canonical instruction file**, `CLAUDE.md` becomes a thin pointer. `AGENTS.md` also now declares the **instance type** (`corporativa`/`pessoal`), the criterion for which variant of the sensitive-data policy (section 2-A) applies to the repository — never again inferred by the agent. See `decisions/0015-agents-md-canonical-instruction-file.md` and `decisions/0022-instance-type-declared-in-agents-md.md`.
- SPEC.md, section 12: **multi-account author identity** — registry of git accounts equivalent to the same `author`, and an invitation-direction rule (personal invites professional into the personal second brain, never the reverse). See `decisions/0020-multi-account-author-identity.md`.
- SPEC.md, section 9: **operational criterion for SemVer scope** — concrete test to classify MAJOR/MINOR/PATCH ("does it break, or just lag behind?"), instead of loose judgment. See `decisions/0023-operational-criterion-for-semver-scope.md`.
- **`UPGRADE.md`** (new) — cumulative, idempotent instance-update checklist: what an instance should have, today, to be conformant with the current version, no matter which old version it started from. Different from `MIGRATIONS.md` (MAJOR jumps only). Exercised against a hypothetical case (instance stuck at v1.3.0) and validated against Mau's 4 real content repositories. See `decisions/0024-upgrade-md-cumulative-checklist.md`.
- **`decisions/0025-skill-is-client-side-never-per-repository.md`** — the skill always runs in the AI environment of whoever is operating it, per person, never per repository. The `skill/` folder that every content repository inherited from "Use this template" never had a functional effect (no agent automatically activates a skill from a file in a repository) — it stops being part of an instance's expected scope. Raised by Mau by directly questioning the architecture.
- `decisions/0016-short-term-memory-sanitization.md` — refines the memory-layers model (DR0008): short term is a sanitization stage (atomicity, placement), not just raw capture; each repository has its own `inbox/`.
- `decisions/0018-frontmatter-validation-at-read-time.md` — extends the CRUD/READ mechanics (DR0012): every read validates frontmatter against the norm, flags an expired `ttl`, and suggests revalidation via research when applicable.
- `decisions/0021-release-cadence-policy.md` — accumulate work before cutting a release, hotfix/PATCH for genuine urgency.
- `decisions/0022-instance-type-declared-in-agents-md.md` — closes an asymmetry in the structural audit (DR0019): the sensitive-data-leak function was anchored only in the generic policy (section 2-A), without saying where the instance type that the policy references is declared. It is now explicitly in `AGENTS.md`, the same artifact that already anchored the placement function.
- `decisions/0023-operational-criterion-for-semver-scope.md` — see above.
- `decisions/0024-upgrade-md-cumulative-checklist.md` — see above.
- `decisions/0026-account-vs-opinion-in-corporate-instance.md` — see above.
- `decisions/0027-promote-depromote-redbutton.md` — see above.
- `decisions/0028-broadened-trigger-2a-remediation.md` — see above.
- `decisions/0029-repository-type-taxonomy.md` — see above.
- `decisions/0030-promote-same-domain-graduation.md` — see above.
- `decisions/0031-change-set-mechanism.md` — see above.
- `decisions/0032-toolkit-consolidation-into-scaffolding.md` — see above.
- `decisions/0033-hipocampo-yaml-per-vault-manifest.md` — see above.

### Changed
- SPEC.md, section 5-A: the REM ritual gains a second function ("update old memories", processing the frontmatter audit queue) and a recommended daily cadence.
- SPEC.md, section 2-B: READ now includes real-time frontmatter validation, not just frontmatter-first reading.
- SPEC.md, section 2-A: new closing sentence pointing to the "instance type" field in `AGENTS.md` as the criterion for which variant of the policy applies (DR0022).
- SPEC.md, section 5-C: function 3 (sensitive-data leak) rewritten to cite the same "instance type" field in `AGENTS.md`, following the same pattern already used by function 2 (placement).
- SPEC.md, section 9: rewritten — operational scope criterion (DR0023), the rule that tag + Release are always published together (closes the real asymmetry in v1.3.0, which has a tag without a Release), and the release routine expanded to include updating `UPGRADE.md` (DR0024).
- SPEC.md, section 11: final note pointing to `UPGRADE.md` as the complete checklist for migrating `CLAUDE.md` → `AGENTS.md`.
- `UPGRADE.md`: new mandatory item — content repositories don't have their own `skill/` folder (DR0025); and, in this round, new manifest items for `hipocampo.yaml`, `skill/manifest.yaml`, and vocabulary divergence (DR0033); `hipocampo-toolkit/*` paths corrected to `scaffold/*` (DR0032).
- Fixed the SPEC.md version header, which was stuck at "1.6.0" (out of step with releases v1.7.0-v1.9.0, which didn't change SPEC.md itself) — it now reflects the current version, 1.9.0 + unreleased.
- `README.md`, `GETTING-STARTED.md`: references to `hipocampo-toolkit` (instantiation via "Use this template", generic skill path) rewritten for the agent-driven model based on `scaffold/` (DR0032).

### Removed
- Reference to the `hipocampo-toolkit` repository as a separate GitHub template — consolidated into `hipocampo` (`scaffold/` + `skill/`). The repository itself is archived on GitHub as a manual action (no tool available in this process automates that step), first receiving a redirect notice in its own `README.md`.

## [1.9.0] — 2026-07-29

### Added
- `docs/FAQ-AND-COMMON-ERRORS.md` — instantiation errors actually encountered in practice (skill not installed by the template, incorrectly inherited LICENSE, outdated `CLAUDE.md`, org permission, migration via direct copy) and frequently asked questions (physical deletion, AI-product outage, need for the skill, methodology license vs. content license, detecting a new release, alternative git host, forgotten visibility).

## [1.8.0] — 2026-07-29

### Added
- `docs/FUNDAMENTALS.md` — concrete step-by-step for "Use this template" (where to click, what to fill in), for those who have never used GitHub.
- `docs/MULTI-TOOL-USAGE.md` — common principle for using Hipocampo (GitHub MCP) and tool-specific specifics: Claude (Cowork, Code, API/Desktop), ChatGPT, Gemini, GitHub Copilot, Antigravity.

## [1.7.0] — 2026-07-29

### Added
- `docs/AI-MODELS.md` — reference on what matters (and what doesn't) in an AI model/product to operate Hipocampo well: context window and frontmatter-first, the probabilistic nature of routines, GitHub MCP as the common denominator across tools.
- `docs/PERFORMANCE-AND-GRAPH.md` — how Hipocampo's retrieval/graph model works, and an explicit comparison with Google's OKF (Open Knowledge Format), published in June 2026.

### Changed
- `GETTING-STARTED.md` — new section 0 with a recommended reading order for those learning the methodology for the first time; instantiation step updated with the LICENSE swap (incorrectly inherited as Apache-2.0) and the personalization/installation of the real skill (`hipocampo-toolkit/skill/SKILL.md`); references to the "stub" skill removed.

## [1.6.0] — 2026-07-29

### Added
- Mandatory routine at every methodology release (SPEC.md, section 9): checking whether migration is needed (even if the conclusion is "no action needed") and syncing `hipocampo-toolkit` (CLAUDE.md and other affected files). First retroactive execution this round: `hipocampo-toolkit/CLAUDE.md` corrected from "^1.0.0" (five releases out of date) to "^1.5.0", and LICENSE templates added for the personal/corporate profiles in `hipocampo-toolkit/license-templates/`, fixing the improper inheritance of the methodology's Apache-2.0 license in newly instantiated content repositories. See `decisions/0014-mandatory-release-routine.md`.

## [1.5.0] — 2026-07-29

### Added
- Section 2-B in SPEC.md: CRUD mechanics explicitly named (Create/Read/Update/Delete mapped onto the already-existing lifecycle) and a frontmatter-first reading rule for agents (frontmatter first, full body only when needed — token savings). See `decisions/0012-crud-frontmatter-first-mechanics.md`.
- Section 10 in SPEC.md: migration of pre-existing content never copies a file directly — frontmatter is always rewritten per the current schema, body adjusted per current atomicity/naming/privacy rules. See `decisions/0011-migration-never-direct-copy.md`.
- New principle in DISCLAIMER.md: data from any instance is always human-readable (markdown + git), regardless of whether a specific AI product is up and running. See `decisions/0013-data-always-human-readable.md`.

## [1.4.0] — 2026-07-29

### Added
- `BEST-PRACTICES.md` — guide to best practices for using the methodology, in an accessible tone: day-to-day operation, privacy/compliance posture, and adoption by new teams/companies.
- Formal, narrow exception to Invariant 3 (SPEC.md, section 8): physical deletion of specific personal content is allowed when triggered by a legitimate personal-data erasure request (LGPD Art. 16 / GDPR Art. 17), always with an explicit human decision and replacement by a minimal record of the fact ("tombstone"). See `decisions/0010-legal-deletion-exception.md`.

## [1.3.0] — 2026-07-28

### Added
- Section 2-A in SPEC.md: sensitive-data policy by instance type. A corporate instance never stores contracts/NDAs, performance reviews, health notes, personal data (password, personal address/contact, relative's name), or salary/vendor/project figures — except a business-outcome figure in a `type: case`. Full name, job title, and professional contact are allowed with a year citation. Technical detail of an active vulnerability/exploit is never recorded verbatim, in any instance. See `decisions/0009-privacy-policy-by-instance.md`.

## [1.2.0] — 2026-07-28

### Added
- Section 5-A in SPEC.md: the REM ritual and the four-stage memory model (sensory → attention gate → short term → REM consolidation → long term), an optional capability per instance. Formalizes how a new item (raw capture) enters the system and becomes a consolidated document — complements section 5 (which covers how an already-existing document ages). See `decisions/0008-rem-ritual-and-memory-layers.md`.

## [1.1.0] — 2026-07-27

### Added
- `license` field in frontmatter (SPEC.md, section 2), always mechanically derived from `visibility`, never set by hand — SPDX `LicenseRef-<idstring>` pattern, full legal text in the `LICENSE` file at the root of each content repository. See `decisions/0007-content-repo-licensing.md`.
- Credit mechanism for historical/migrated content without traceable individual authorship: a `CONTRIBUTORS.md` file per instance, with named, dated sections; `author`/`contributors` can reference a section via `@section-name`. Scoped only to migrated content — a new document always uses a real-person author. See `decisions/0006-contribution-credits.md`.

## [1.0.0] — 2026-07-27

Initial public version of the methodology.

### Added
- `SPEC.md` — unified frontmatter schema (`type`, `category`, `temporality`, `ttl`, `context_anchor`, `related`, `visibility`, `author`/`owner`, among others), a Registry mechanism for cross-repository `related`, distinction between Decision Record and `type: decision`, invariants, and the agent's precedence hierarchy.
- `GETTING-STARTED.md` — practical adoption guide.
- `DISCLAIMER.md` — scope, limits, and recommended/not-recommended scenarios.
- `MIGRATIONS.md` — structure ready for future MAJOR jumps.
- `decisions/` — foundational Decision Records (licensing, multi-repository architecture, naming, alias syntax, `category` vs. `type: framework`).
- `docs/FUNDAMENTALS.md` — introduction to git/GitHub for those who have never used it, with a parallel to Obsidian and a privacy checklist.
- `NOTICE` — trademark carve-out for the name "Hipocampo", complementary to the Apache-2.0 LICENSE.
