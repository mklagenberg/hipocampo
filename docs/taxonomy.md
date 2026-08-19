# Taxonomy map

A single index of every controlled field, enum, and named concept this methodology defines — what it is, where it's authoritatively defined, and (where already known) when it was introduced or last changed. This document doesn't re-argue any rationale — every row points at the `SPEC.md` section and/or Decision Record that actually carries it. See `decisions/0047-taxonomy-map.md` for why this document exists and why this first version stops short of full retroactive coverage.

**Distinct from `docs/vocabulary-dictionary.md`.** That document is narrowly scoped to pt-BR ↔ English value equivalence for controlled-vocabulary fields (`decisions/0035`) — it never goes out of scope. This document is broader and orthogonal: it indexes every structural concept the methodology defines, controlled-vocabulary or not (a behavioral taxonomy like Dispatcher/Routine/Mechanic/Action has no pt-BR/English pair to track, but still belongs here), together with a version lineage vocabulary alone doesn't carry. Where a field also has a pt-BR/English pair, this document points at the dictionary instead of repeating it.

## Status of this document

**Current-state coverage: complete for this revision.** Every row below reflects the schema and concepts as they stand after Lote D of the v2.0.0 taxonomy revision (`decisions/0040` through `0046`).

**Retroactive lineage: partial by design, not oversight.** The "Introduced" and "Last changed" columns are filled in for everything that changed during the v2.0.0 taxonomy revision itself (Lotes A–D, `decisions/0040`–`0046`), because that lineage was already known at the moment of writing this document — no separate research needed. Everything that predates v1.9.0 is marked `TBD — Lote E2`, explicitly, rather than left blank or guessed at. Walking `CHANGELOG.md` from `v1.0.0` forward to reconstruct that older lineage is real, separate work — this repository's own `decisions/0031` precedent limited a Change Set backfill to a single representative PR by proportionality, but that precedent doesn't transfer here: there, the backfill only had to validate a template, one sample was enough; here, the document's entire value proposition is completeness, since the confusion motivating this taxonomy revision came mostly from decisions older than v1.9.0. A map that only covers "from here forward" would resolve half the problem and leave the other half exactly as confusing as it is today. See `decisions/0047` and the planning note in section 12 of the taxonomy revision's own sequencing for why this split into two lotes rather than one.

## 1. Document frontmatter fields (`SPEC.md`, section 2)

| Field | Enum / type | Introduced | Last changed | Source |
|---|---|---|---|---|
| `title` | free string | TBD — Lote E2 | — | `SPEC.md` §2 |
| `date` | date | TBD — Lote E2 | — | `SPEC.md` §2 |
| `updated` | date | TBD — Lote E2 | — | `SPEC.md` §2 |
| `source` | `url \| conversation \| internal` (deprecated pt-BR: `conversa`, `interno` — see `docs/vocabulary-dictionary.md`) | TBD — Lote E2 | v(Fase E) English canonicalization | `SPEC.md` §2, `decisions/0035` |
| `tags` | free list | TBD — Lote E2 | — | `SPEC.md` §2 |
| `type` | `note \| reference \| decision \| project \| person \| case \| framework \| company` | TBD — Lote E2 | — | `SPEC.md` §3 |
| `category` | optional free string | TBD — Lote E2 | — | `SPEC.md` §4 |
| `temporality` | `evergreen \| ephemeral \| contextual \| historical` | TBD — Lote E2 | — | `SPEC.md` §5 |
| `ttl` | concrete date, never the literal `"evergreen"` | TBD — Lote E2 | — | `SPEC.md` §5 |
| `context_anchor` | required only when `temporality: contextual` | TBD — Lote E2 | — | `SPEC.md` §5 |
| `status` | `draft \| active \| stale \| archived \| superseded` | TBD — Lote E2 | — | `SPEC.md` §2 |
| `related` | list, local or `$alias:` cross-repo | TBD — Lote E2 | — | `SPEC.md` §2, §6 |
| `superseded_by` | same syntax as `related` | TBD — Lote E2 | — | `SPEC.md` §2, §6 |
| `revision` / `revision_note` | integer / free string | TBD — Lote E2 | — | `SPEC.md` §2 |
| `visibility` | `public \| internal \| confidential \| restricted` | TBD — Lote E2 | — | `SPEC.md` §2 |
| `author` | `Real Name - @github-username`, or `@section-name` (historical only) | TBD — Lote E2 | — | `SPEC.md` §2, `decisions/0006` |
| `contributors` | list, same identity rules as `author` | TBD — Lote E2 | — | `SPEC.md` §2, `decisions/0006` |
| `owner` | company name, only for a work-context document | TBD — Lote E2 | — | `SPEC.md` §2 |
| `contains_subjective_content` | boolean, relevant only when `owner` is filled in | TBD — Lote E2 | — | `SPEC.md` §2, `decisions/0026` |
| `curation_status` | `staged \| permanent`, relevant only in `company-confidential` | TBD — Lote E2 | — | `SPEC.md` §2, §2-C, `decisions/0029` |
| `license` | `LicenseRef-<idstring>`, always derived from `visibility` | TBD — Lote E2 | — | `SPEC.md` §2, `decisions/0007` |

## 2. Repository/vault-level taxonomy (`SPEC.md`, section 2-C/2-D)

| Concept | Values | Introduced | Last changed | Source |
|---|---|---|---|---|
| `entity` | extensible identifier, supersedes `domain` | TBD — Lote E2 (`domain`) | Lote A, v2.0.0-unreleased — `domain` superseded by `entity` | `SPEC.md` §2-C, `decisions/0041` |
| `role` | `anchor \| additional` | Lote A, v2.0.0-unreleased | — | `SPEC.md` §2-C, `decisions/0041` |
| `scope_description` | required only when `role: additional` | Lote A, v2.0.0-unreleased | — | `SPEC.md` §2-C, `decisions/0041` |
| Exposure tier | `confidential \| public`, carried by repository naming convention | TBD — Lote E2 | Lote A: no longer implied by the `-vault` suffix | `SPEC.md` §2-C/§2-D, `decisions/0029`, `0041` |
| `instance.language` | BCP-47 tag, default `"en"` | TBD — Lote E2 | — | `decisions/0033`, `0034` |
| `instance.tier` (curation-level — **a different concept from exposure tier above, known unresolved name collision**) | `content \| vault` | TBD — Lote E2 | — | `decisions/0033`, `SPEC.md` §2-C "Known, separate inconsistency" |
| `AGENTS.md` "Instance type" (recommended for retirement) | `corporate \| personal` | TBD — Lote E2 | Lote A: recommended for retirement in favor of `entity`+`role` | `SPEC.md` §2-A, §11, `decisions/0022`, `0041` |
| Multi-vault/multi-entity design premises | 3 premises (multi-vault by design; confidential-first; anchor as existence guarantee) | Lote A, v2.0.0-unreleased | — | `SPEC.md` §2-D, `decisions/0040` |

## 3. Identity artifacts

| Concept | Fields | Introduced | Source |
|---|---|---|---|
| `profile.md` | `name`, `preferred_name`, `emails`, `github_handles`, `updated` | Lote C, v2.0.0-unreleased | `SPEC.md` §12-B, `decisions/0045` |
| Multi-account author identity | recorded in `AGENTS.md` of the least-restricted personal repository | TBD — Lote E2 | `SPEC.md` §12, `decisions/0020` |

## 4. Behavioral taxonomy (`SPEC.md`, section 5-D)

| Concept | Members | Introduced | Source |
|---|---|---|---|
| Dispatcher | schedules routines | Lote B, v2.0.0-unreleased | `SPEC.md` §5-D, `decisions/0042` |
| Routine | REM (§5-A), frontmatter audit (§5-B), weekly structural audit (§5-C) | Lote B, v2.0.0-unreleased (naming); routines themselves predate it | `SPEC.md` §5-D, `decisions/0043` |
| Mechanic — CRUD | Create, Read, Update, Delete | TBD — Lote E2 (mechanic itself predates the naming, formally named in Lote B) | `SPEC.md` §2-B, §5-D, `decisions/0012`, `0043` |
| Mechanic — Publication | Promote, Depromote | TBD — Lote E2 (predates naming); formally named Lote B | `SPEC.md` §13, §5-D, `decisions/0027`, `0043` |
| Mechanic — Sequenced-removal | Redbutton | TBD — Lote E2 (predates naming); formally named Lote B | `SPEC.md` §13, §5-D, `decisions/0027`, `0028`, `0043` |
| Mechanic — Bootstrap | Select, Orient, Instantiate, Interview | Lote C, v2.0.0-unreleased | `SPEC.md` §5-D, §12-B, `decisions/0045` |
| Vault and entity discovery | manifest read + sensory-memory cache, no stored router | Lote C, v2.0.0-unreleased | `SPEC.md` §12-A, `decisions/0044` |

## 5. Cross-repository lifecycle actions (`SPEC.md`, section 13)

| Action | Variants | Introduced | Source |
|---|---|---|---|
| Promote | elegant path, literal path, graduation within the same domain | TBD — Lote E2 (graduation variant: `decisions/0030`) | `SPEC.md` §13, `decisions/0027`, `0030` |
| Depromote | — | TBD — Lote E2 | `SPEC.md` §13, `decisions/0027` |
| Redbutton | — | TBD — Lote E2 (trigger broadened by `decisions/0028`) | `SPEC.md` §13, `decisions/0027`, `0028` |

## 6. Information-type taxonomy (`decisions/0026`)

Fact, Account, Opinion, Memory — see `SPEC.md` section 2, field `contains_subjective_content`. Not duplicated here; this row exists so the index is complete. Introduced: TBD — Lote E2.

## 7. Controlled vocabulary (pt-BR ↔ English)

Not duplicated here — see `docs/vocabulary-dictionary.md`, which already carries its own version lineage in its "Change history" section for every deprecated/canonical pair it covers.

## 8. Step-behavior taxonomy

Not duplicated here — see `docs/step-classification.md` (deterministic / discretionary / gated), introduced in the same lote as this document.

## Known cross-references and name collisions (collected here, not duplicated)

- `instance.tier` (curation-level) and the exposure tier of section 2-C name two different concepts under the same word `tier` — flagged in `SPEC.md` §2-C, unresolved.
- `AGENTS.md`'s "Instance type" and `hipocampo.yaml`'s `instance.entity`/`instance.role` currently both exist, with the former recommended for retirement — flagged in `SPEC.md` §2-C and §8 (Invariant 6's no-duplicate-field condition), unresolved until real instances migrate.

## Retroactive backfill — what Lote E2 will do

For every `TBD — Lote E2` cell above: walk `CHANGELOG.md` from `[1.0.0]` forward, identify the version each field/value/concept was introduced or last materially changed, and cite the governing Decision Record for that change. Scope is exactly the cells marked `TBD` above — not a rewrite of this document's structure, which this lote (E1) already establishes.
