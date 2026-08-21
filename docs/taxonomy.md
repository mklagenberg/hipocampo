# Taxonomy map

A single index of every controlled field, enum, and named concept this methodology defines — what it is, where it's authoritatively defined, and when it was introduced or last changed. This document doesn't re-argue any rationale — every row points at the `SPEC.md` section and/or Decision Record that actually carries it. See `decisions/0047-taxonomy-map.md` for why this document exists and why it originally shipped in two lotes.

**Distinct from `docs/vocabulary-dictionary.md`.** That document is narrowly scoped to pt-BR ↔ English value equivalence for controlled-vocabulary fields (`decisions/0035`) — it never goes out of scope. This document is broader and orthogonal: it indexes every structural concept the methodology defines, controlled-vocabulary or not (a behavioral taxonomy like Dispatcher/Routine/Mechanic/Action has no pt-BR/English pair to track, but still belongs here), together with a version lineage vocabulary alone doesn't carry. Where a field also has a pt-BR/English pair, this document points at the dictionary instead of repeating it.

## Status of this document

**Coverage: complete, current state and lineage.** Lote E1 (`decisions/0047`) established this document's structure and populated current-state coverage completely, plus the lineage for everything that changed during the v2.0.0 taxonomy revision itself (Lotes A–D, `decisions/0040`–`0046`), already known at the time. Every cell that predated `v1.9.0` was left `TBD — Lote E2`, explicitly, rather than guessed at.

**Lote E2 (this revision) fills every remaining `TBD` cell**, by walking `CHANGELOG.md` from `[1.0.0]` forward and cross-referencing the `decisions/` directory listing. Two things worth stating plainly about how that walk was done, per this repository's own "no silent caps" discipline:

- **A field's real version is the tagged release it shipped in — `v1.0.0` through `v1.9.0` — cited by the Decision Record (if any) that introduced or changed it.** At the time Lote E2 did this backfill, everything added to `SPEC.md` after the `v1.9.0` tag (2026-07-29) was still cited in this document as **"Unreleased"**, since it hadn't shipped in a tagged release yet — that covered almost the entire second half of the Decision Record range (`decisions/0015` through `decisions/0049`): `AGENTS.md` as canonical instruction file, the frontmatter and structural audit rituals, multi-account identity, the SemVer operational criterion, `UPGRADE.md`, the skill's client-side-only status, Promote/Depromote/Redbutton, the repository type taxonomy, the Change Set mechanism itself, the scaffold/manifest consolidation, the English translation and vocabulary dictionary, the deterministic validator, failure/recovery behavior, evaluation scenarios, and the entire v2.0.0 taxonomy revision (Lotes A–F). **That bucket resolved to a single real version, `v2.0.0`, when the tag was cut** — every table cell below that once read "Unreleased" now reads `v2.0.0` uniformly; the "Lote" labels already in this document (and the `decisions/0040`+ numbering) remain the only reliable ordering signal *within* that version, since `v2.0.0` accumulated over several PRs rather than shipping as one atomic change.
- **Not every field traces to a single, exclusively-dedicated Decision Record.** A few rows below cite a DR that established the *concept* (e.g. "instance type" as a distinction between repositories) separately from a later DR that made it an explicit, declared field (e.g. requiring it to live in `AGENTS.md`). Where that split exists, both are cited, with a short note on which is which — collapsing them into one date would overclaim precision the source material doesn't have. Likewise, `domain` (superseded by `entity` in Lote A) is attributed to `decisions/0002`, which establishes the multi-repository architecture underlying the personal/corporate split but does not itself name a `domain` frontmatter field — the field's exact origin as a schema entry is the `v1.0.0` base schema ("`type`, `category`, `temporality`, `ttl`, `context_anchor`, `related`, `visibility`, `author`/`owner`, among others"); `decisions/0002` is cited because it's the DR that actually explains *why* that split exists, per this document's own precedent for the analogous `AGENTS.md` "Instance type" row.
- **Decisions `0001`–`0005`** (Apache-2.0 licensing, this multi-repository architecture, the "Hipocampo" naming, `$alias:` syntax, `category` vs. `type: framework`) are cited only in aggregate, matching how `CHANGELOG.md`'s own `[1.0.0]` entry cites them — as "foundational Decision Records," not attributed individually to specific schema fields. This document doesn't split that aggregate further; doing so would require re-deriving attributions `CHANGELOG.md` itself never made.

## 1. Document frontmatter fields (`SPEC.md`, section 2)

| Field | Enum / type | Introduced | Last changed | Source |
|---|---|---|---|---|
| `title` | free string | v1.0.0 | — | `SPEC.md` §2 |
| `date` | date | v1.0.0 | — | `SPEC.md` §2 |
| `updated` | date | v1.0.0 | — | `SPEC.md` §2 |
| `source` | `url \| conversation \| internal` (deprecated pt-BR: `conversa`, `interno` — see `docs/vocabulary-dictionary.md`) | v1.0.0 | v2.0.0 — Fase E, English canonicalization | `SPEC.md` §2, `decisions/0035` |
| `tags` | free list | v1.0.0 | — | `SPEC.md` §2 |
| `type` | `note \| reference \| decision \| project \| person \| case \| framework \| company` | v1.0.0 | — | `SPEC.md` §3 |
| `category` | optional free string | v1.0.0 | — | `SPEC.md` §4 |
| `temporality` | `evergreen \| ephemeral \| contextual \| historical` | v1.0.0 | — | `SPEC.md` §5 |
| `ttl` | concrete date, never the literal `"evergreen"` | v1.0.0 | — | `SPEC.md` §5 |
| `context_anchor` | required only when `temporality: contextual` | v1.0.0 | — | `SPEC.md` §5 |
| `status` | `draft \| active \| stale \| archived \| superseded` | v1.0.0 | — | `SPEC.md` §2 |
| `related` | list, local or `$alias:` cross-repo | v1.0.0 | — | `SPEC.md` §2, §6 |
| `superseded_by` | same syntax as `related` | v1.0.0 | v2.0.0 — gained cross-repository `$alias:` syntax | `SPEC.md` §2, §6, `decisions/0027` |
| `revision` / `revision_note` | integer / free string | v1.0.0 | — | `SPEC.md` §2 |
| `visibility` | `public \| internal \| confidential \| restricted` | v1.0.0 | — | `SPEC.md` §2 |
| `author` | `Real Name - @github-username`, or `@section-name` (historical only) | v1.0.0 | v1.1.0 — `@section-name` historical-reference syntax added | `SPEC.md` §2, `decisions/0006` |
| `contributors` | list, same identity rules as `author` | v1.1.0 (credit mechanism, `CONTRIBUTORS.md`) | v2.0.0 — added to the schema's central field listing; already in use, just never listed there | `SPEC.md` §2, `decisions/0006`, `decisions/0026` |
| `owner` | company name, only for a work-context document | v1.0.0 | — | `SPEC.md` §2 |
| `contains_subjective_content` | boolean, relevant only when `owner` is filled in | v2.0.0 | — | `SPEC.md` §2, `decisions/0026` |
| `curation_status` | `staged \| permanent`, relevant only in a restricted corporate vault | v2.0.0 | v2.1.1 — promotion target clarified as broader-access private, never public | `SPEC.md` §2, §2-C, `decisions/0029`, `0054` |
| `license` | `LicenseRef-<idstring>`, always derived from `visibility`; never an open license | v1.1.0 | v2.1.1 — private/proprietary boundary clarified | `SPEC.md` §2, `decisions/0007`, `0054` |

## 2. Repository/vault-level taxonomy (`SPEC.md`, section 2-C/2-D)

| Concept | Values | Introduced | Last changed | Source |
|---|---|---|---|---|
| `entity` | extensible identifier, supersedes `domain` | v1.0.0 (`domain`, base schema; `decisions/0002` explains the underlying architecture without naming the field) | Lote A, v2.0.0 — `domain` superseded by `entity` | `SPEC.md` §2-C, `decisions/0002`, `0041` |
| `role` | `anchor \| additional` | Lote A, v2.0.0 | — | `SPEC.md` §2-C, `decisions/0041` |
| `scope_description` | required only when `role: additional` | Lote A, v2.0.0 | — | `SPEC.md` §2-C, `decisions/0041` |
| Visibility handling classification | `public \| internal \| confidential \| restricted`; never legal permission | v1.0.0 | v2.1.1 — `public` constrained to the authorized private context | `SPEC.md` §2, §2-C/§2-D, `decisions/0007`, `0054` |
| `instance.language` | BCP-47 tag, default `"en"` | v2.0.0 — Fase E | — | `decisions/0033`, `0034` |
| `instance.curation_level` | `content \| vault`, distinct from exposure tier | v2.1.0 | — | `SPEC.md` §2-C, `decisions/0052` |
| `instance.policy_profile` | `corporate \| personal`, sole sensitive-data-policy selector | v2.1.0 | — | `SPEC.md` §2-A, §11, `decisions/0052` |
| Operational vault descriptor | `personal-open-vault`, `personal-restricted-vault`, `company-open-vault`, `company-restricted-vault`; prose only, derived from manifest fields | v2.1.1 | — | `docs/vocabulary-dictionary.md`, `SPEC.md` §2-C, `decisions/0054` |
| Multi-vault/multi-entity design premises | 3 premises (multi-vault by design; confidential-first; anchor as existence guarantee) | Lote A, v2.0.0 | — | `SPEC.md` §2-D, `decisions/0040` |

## 3. Identity artifacts

| Concept | Fields | Introduced | Source |
|---|---|---|---|
| `profile.md` | `name`, `preferred_name`, `emails`, `github_handles`, `updated` | Lote C, v2.0.0 | `SPEC.md` §12-B, `decisions/0045` |
| Multi-account author identity | recorded in `AGENTS.md` of the least-restricted personal repository | v2.0.0 | `SPEC.md` §12, `decisions/0020` |

## 4. Behavioral taxonomy (`SPEC.md`, section 5-D)

| Concept | Members | Introduced | Source |
|---|---|---|---|
| Dispatcher | schedules routines | Lote B, v2.0.0 | `SPEC.md` §5-D, `decisions/0042` |
| Routine | REM (§5-A): v1.2.0. Frontmatter audit (§5-B): v2.0.0. Weekly structural audit (§5-C): v2.0.0. Collectively named "Routine": Lote B | `SPEC.md` §5-D, `decisions/0008`, `0017`, `0019`, `0043` |
| Mechanic — CRUD | Create, Read, Update, Delete | Named "CRUD": v1.5.0. Recategorized as a Mechanic: Lote B | `SPEC.md` §2-B, §5-D, `decisions/0012`, `0043` |
| Mechanic — Publication | Promote, Depromote | v2.0.0. Recategorized as a Mechanic: Lote B | `SPEC.md` §13, §5-D, `decisions/0027`, `0043` |
| Mechanic — Sequenced-removal | Redbutton | v2.0.0; trigger broadened, also v2.0.0. Recategorized as a Mechanic: Lote B | `SPEC.md` §13, §5-D, `decisions/0027`, `0028`, `0043` |
| Mechanic — Bootstrap | Select, Orient, Instantiate, Interview | Lote C, v2.0.0 | `SPEC.md` §5-D, §12-B, `decisions/0045` |
| Vault and entity discovery | manifest read + sensory-memory cache, no stored router | Lote C, v2.0.0 | `SPEC.md` §12-A, `decisions/0044` |

## 5. Cross-repository lifecycle actions (`SPEC.md`, section 13)

| Action | Variants | Introduced | Source |
|---|---|---|---|
| Promote | elegant path, literal path, graduation within the same domain | v2.0.0 (base action); graduation variant: v2.0.0 | `SPEC.md` §13, `decisions/0027`, `0030` |
| Depromote | — | v2.0.0 | `SPEC.md` §13, `decisions/0027` |
| Redbutton | — | v2.0.0; trigger broadened by a later, also-v2.0.0 DR | `SPEC.md` §13, `decisions/0027`, `0028` |

## 6. Information-type taxonomy (`decisions/0026`)

Fact, Account, Opinion, Memory — see `SPEC.md` section 2, field `contains_subjective_content`. Not duplicated here; this row exists so the index is complete. Introduced: v2.0.0.

## 7. Controlled vocabulary (pt-BR ↔ English)

Not duplicated here — see `docs/vocabulary-dictionary.md`, which already carries its own version lineage in its "Change history" section for every deprecated/canonical pair it covers.

## 8. Step-behavior taxonomy

Not duplicated here — see `docs/step-classification.md` (deterministic / discretionary / gated), introduced in the same lote as this document.

## Known cross-references and name collisions (collected here, not duplicated)

- Legacy `instance.tier` and `AGENTS.md` “Instance type” remain readable only as compatibility aliases; new manifests use `instance.curation_level` and `instance.policy_profile` (`decisions/0052`).
- New named methodology concepts are admitted only after the term-governance check in `docs/vocabulary-dictionary.md`; the taxonomy records the concept and its authoritative source, while the dictionary records controlled values and aliases.

## Retroactive backfill — what Lote E2 did

Every cell marked `TBD — Lote E2` in the Lote E1 revision of this document is now filled in, per the method described in "Status of this document" above: walking `CHANGELOG.md` from `[1.0.0]` forward, cross-referencing the `decisions/` directory listing, and spot-reading a handful of Decision Records directly (`decisions/0002`, `0029`, `0033`) where `CHANGELOG.md`'s own bullet text left the attribution ambiguous, rather than trusting every citation at face value. No cell was left as `TBD` a second time; where the underlying source material itself doesn't support single-date precision (the `entity`/`domain` row, the `AGENTS.md` "Instance type" row), that imprecision is stated explicitly rather than resolved by guessing.
