# Hipocampo — SPEC

Version: 1.9.0 + unreleased · Follows [SemVer](https://semver.org/lang/pt-BR/)

> **Version note:** the latest formal release (tag + GitHub Release) is **v1.9.0**. This document already includes work accepted and merged into `main` beyond that release (sections 5-B, 5-C, 11, 12, 13, and 14) — see `CHANGELOG.md`, the `[Unreleased]` section, and `decisions/0021-release-cadence-policy.md`. If you're checking compatibility for an existing instance, check it against the latest tag, not against this file on `main`, until the next release is cut.

This document is the normative specification of the Hipocampo methodology: the frontmatter schema, the retrieval rules, and the conventions that any instance (content repository) must follow to be considered compatible with a version of Hipocampo. It is not a usage manual — for that, see [GETTING-STARTED.md](GETTING-STARTED.md). It is not a document of limitations — for that, see [DISCLAIMER.md](DISCLAIMER.md). It is not a best-practices guide — for that, see [BEST-PRACTICES.md](BEST-PRACTICES.md). It is not an upgrade guide for an existing instance — for that, see [UPGRADE.md](UPGRADE.md).

## 1. Scope

Hipocampo is an agentic second brain methodology: git + markdown + AI rituals. This repository (`hipocampo`) and `hipocampo-toolkit` are the only two public repositories of the methodology — they carry the spec and the tooling, never actual content. Every knowledge base that implements Hipocampo lives in private repositories, without exception (see invariants, section 8).

**Repository language:** this repository is maintained in English — `SPEC.md`, `decisions/`, `docs/`, `skill/`, and `scaffold/` are written and contributed to in English (see `decisions/0034-repository-and-vault-language-policy.md`). A vault (a content repository generated from this methodology) is not bound to this: its own working language is declared in its `hipocampo.yaml` manifest (`instance.language`, `decisions/0033`/`0034`), independent of the language this repository is maintained in.

## 2. Frontmatter — unified schema

Every document in a Hipocampo instance is a `.md` file with this YAML frontmatter:

```yaml
---
title: ""
date: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
source: "url | conversation | internal"    # deprecated pt-BR values (conversa, interno) still valid — see docs/vocabulary-dictionary.md
tags: []
type: "note | reference | decision | project | person | case | framework | company"
category: ""                      # optional, only when the area already has a dedicated physical subfolder by topic
temporality: "evergreen | ephemeral | contextual | historical"
ttl: "YYYY-MM-DD"                 # always a concrete date — never the literal "evergreen"
context_anchor: ""                # required only when temporality: contextual
status: "draft | active | stale | archived | superseded"
related: []                       # "path/local.md" or "$alias:path.md"
superseded_by: ""                 # "path/local.md" or "$alias:path.md" — same cross-repo syntax as related (see section 6 and decisions/0027)
revision: 1
revision_note: ""
visibility: "public | internal | confidential | restricted"
author: "Real Name - @github-username"    # always a person, never the AI — or @section-name from CONTRIBUTORS.md, only for historical content (see decisions/0006)
contributors: []                          # people besides the author who contributed content to this specific document; a new document always uses a real person, verified by commit or explicit citation — @section-name only for historical content (see decisions/0006)
owner: ""                                 # company name, only when the document originates in a work context
contains_subjective_content: false        # default false; only relevant when owner is filled in — flags that the body contains opinion and/or the author's/contributor's personal memory, not just fact/account (see decisions/0026)
curation_status: ""                       # optional, only relevant in an empresa-confidencial repository (section 2-C) — "staged" (candidate for future promotion to empresa-público) or "permanent" (confidential by nature, default); see decisions/0029
license: ""                               # always derived from `visibility`, never filled in by hand (see decisions/0007)
---
```

### title, date, updated, source, tags
Standard descriptive usage. `source` distinguishes knowledge that came in through external research (`url`), through dialogue (`conversation`), or produced internally (`internal`). A document written before this field's canonical vocabulary became English may still carry the deprecated pt-BR values (`conversa`, `interno`) — both remain fully valid, recognized as equivalent to the current values; see `docs/vocabulary-dictionary.md`, `decisions/0035-controlled-vocabulary-dictionary.md`.

### status
Document lifecycle: `draft` (not yet consolidated knowledge) → `active` (in use) → `stale` (flagged by the staleness routine, needs review) → `archived` (withdrawn from circulation, but preserved) → `superseded` (replaced by another document, see `superseded_by`). A document is never physically deleted — it only transitions to `archived` or `superseded` (invariant, see section 8).

### revision, revision_note
Every content edit (not trivial wording) increments `revision` and records the reason in `revision_note`. A history of *why* the document changed, not just *when*.

### visibility
Resolves **only** who, already having access to the repository, can use the content without additional restriction: `public` (no restriction, even outside the repo), `internal` (internal use by the organization that owns the repo), `confidential` (use restricted to those who need to know, even within the repo), `restricted` (individualized use, case by case). `visibility` **never decides exposure to the internet** — that is resolved structurally by the rule that no knowledge repository is public (invariant, section 8). A `confidential` label in a repository the whole team accesses does not stop anyone on that team from reading the file — real GitHub permission is repository-level granularity, not file-level granularity within a shared repository. Content that actually needs technical enforcement goes into a separate repository with restricted access permission, not into a `visibility` label inside a more open repository.

### author / owner
`author` is always a person (`Real Name - @github-username`), never the AI — even when an agent writes the text under someone's direction, the author is whoever directed it. Mandatory field on any document, at any `visibility`. An exception scoped only to historical/migrated content, with no individually traceable authorship at the source: `author`/`contributors` may reference a named, dated section of a `CONTRIBUTORS.md` file via `@section-name`, instead of a person — a new document never uses this exception (see `decisions/0006-contribution-credits.md`). Outside that exception, `contributors` (optional) lists people besides the `author` who actually contributed content to a new document, verified by commit or explicit citation — never assumed in bulk from a team's existence (see `decisions/0006`). `owner` is always the name of a company, filled in only when the document originates in a work context — see the full distinction of roles and what each may do with the content in `DISCLAIMER.md` and in the licensing Decision Records under `decisions/`. See also section 12 for the case of a person operating more than one git account.

### contains_subjective_content
Optional field, relevant only when `owner` is filled in (corporate instance). Flags that the document body contains at least one passage of **Opinion** or **Memory** — the two categories, within the information-type taxonomy (`decisions/0026`), that carry risk of personal liability for whoever wrote them. The full taxonomy has four values, used as an inline prefix when a document mixes more than one type: **Fact:** (verified/confirmed), **Account:** (said/observed, not confirmed), **Opinion:** (value judgment), **Memory:** (reconstructive personal recollection — a term chosen so as not to collide with "memory layers," section 5-A, which is about processing stage, not about the reliability of a statement). A document that is entirely of a single type doesn't need to be labeled sentence by sentence — this field alone is enough. The `@handle` only accompanies the inline label when the document has `contributors` filled in — a case where `author` alone isn't enough to know who wrote each passage; a single-author document skips the inline handle, since the frontmatter's `author` already resolves attribution. Before writing new Opinion or Memory content in a corporate instance (`contains_subjective_content` becoming `true`), the agent explicitly asks whether it should stay marked there or go to the responsible author's/contributor's personal instance — without explicit confirmation, it goes to personal, never guessed. See `decisions/0026-account-vs-opinion-in-corporate-instance.md`.

### curation_status
Optional field, relevant only within a repository of the `company-confidential` tier (section 2-C — formerly described as `empresa-confidencial`, see `docs/vocabulary-dictionary.md`). Flags the intended lifecycle of the document within that repository: `staged` marks a candidate for eventual promotion to a `company-public` repository, after leadership curation; `permanent` (default, when the field is left empty) marks content confidential by nature, with no expectation of future publication. It does not replace or overlap with `visibility` — the two fields resolve different questions: `visibility` is about who, already with access to the repository, can use the content without additional restriction; `curation_status` is about whether that specific document is a candidate to change repository someday. See `decisions/0029-repository-type-taxonomy.md`.

### license
Always mechanically derived from `visibility`, never set by hand — this avoids divergence between the confidentiality layer (`visibility`) and the legal layer (`license`). Uses the SPDX pattern `LicenseRef-<idstring>`, with the full legal text in the `LICENSE` file at the repository root, never rewritten per document. See `decisions/0007-content-repo-licensing.md`.

## 2-A. Sensitive-data policy by instance type

A corporate instance (`owner` filled in with an organization's name) never stores, at any `visibility` level — even `restricted`: contract or NDA content; performance evaluation of an identifiable individual; health note about any person (the instance owner or a third party); personal data (password, personal address, personal phone or email, relative's name); salary figures, amounts paid to a vendor, or project/contract value. Single exception for an absolute figure: a business result delivered to a client in a `type: case` (revenue generated, cost avoided) is the very product of the case, not internal financial exposure. Quantified internal learning (e.g., process savings) is recorded as a percentage variation, never an absolute value.

Financial data about a third party that is not a direct vendor/business partner (e.g., market intelligence about a competitor, extracted from a public source) is not covered by this restriction — provided the public source is explicitly cited in the document.

Full name, title, professional email, professional phone, or professional address — of a colleague or a client contact — are permitted in a corporate instance, always accompanied by a year/date citation: the record is a dated snapshot, never a presumed current state.

Any individual's personal matter (health, personal financial situation) never goes into a corporate instance — always into the relevant owner's personal instance, if one exists.

Technical detail of an active vulnerability or exploit (attack payload, query/dork that reveals the compromise, credential, exploitable endpoint) is never recorded verbatim, in any instance, even confidential/restricted — the fact is recorded (the flaw's existence, category, date of the finding) and the response given, never the material that would reproduce or confirm the attack.

When an entire document structurally depends on a banned data type (it can't be fixed by just removing the problematic passage), the agent doesn't decide alone between publishing anyway or discarding it — it flags the violation to the human responsible for the instance and waits for an explicit decision. See `decisions/0009-privacy-policy-by-instance.md`. The weekly structural audit (section 5-C) is the periodic mechanism that checks compliance with this policy, and the Redbutton action (section 13) is the remediation mechanism when a violation is confirmed.

**Which variant of this policy applies to a repository is never inferred by the agent** from the repository's name or the conversation's context — it is read from the "instance type" field (`corporate` or `personal` — deprecated pt-BR values `corporativa`/`pessoal` remain valid and equivalent, see `docs/vocabulary-dictionary.md`), mandatorily declared in the "Repository scope" block of that repository's `AGENTS.md` (section 11). See `decisions/0022-instance-type-declared-in-agents-md.md`.

## 2-B. CRUD mechanics and frontmatter-first reading

The document lifecycle (section 2, `status` field) implements the four operations of a CRUD: **Create** (creation with full frontmatter), **Read** (query by agent or human), **Update** (content edit with `revision` increment), **Delete** (mitigated by invariant 3 — never delete physically, only `archived`/`superseded`, with the narrow exception of `decisions/0010`, with its trigger broadened by `decisions/0028`). See `decisions/0012-crud-frontmatter-first-mechanics.md`. Formally, CRUD is the first **mechanic** named under the Dispatcher/Routine/Mechanic/Action taxonomy (section 5-D) — this section already used the word informally, before that taxonomy existed; nothing about CRUD's behavior changes.

Recommended reading rule for the agent: when operating over multiple documents (search, triage, staleness), always read the **frontmatter first** — YAML, low token cost, sufficient to filter by `type`, `tags`, `status`, `temporality`, `related`, and decide relevance. Only read the **full body** after deciding, from the frontmatter, that that specific document needs a full read. In an instance with many documents, this avoids unnecessary token cost — reading the full body of every candidate just to discard most of them is not the default access pattern.

In addition, every READ operation includes a light validation of the frontmatter against the norm in this section 2 and the staleness check in section 5 — independent of whether the frontmatter audit (section 5-B, batch ritual) has already gone over that specific document. If validation finds a problem, the agent explicitly flags what's wrong and what needs to be done; in the case of an expired `ttl`, it makes clear that the information is outdated and suggests revalidation by research when the document is `source: url`. The same light validation also recognizes a deprecated pt-BR controlled-vocabulary value (`docs/vocabulary-dictionary.md`) and flags it as a normalization candidate, the same way it flags an expired `ttl`. This validation never changes `status` or any field on its own — it only flags. See `decisions/0018-frontmatter-validation-at-read-time.md` and `decisions/0035-controlled-vocabulary-dictionary.md`.

## 2-C. Repository-type taxonomy: entity and vault

Every Hipocampo content repository (a **vault**, section 2-D) belongs to exactly one **entity** — an extensible identifier for the person, organization, or relationship the content belongs to (`personal`, a specific company, a family, or any other grouping an operator introduces), not a fixed two-value enum. `entity` supersedes `domain` (`personal`/`company`, `decisions/0002`/`0029`) — the original two values remain valid entity identifiers, the smallest possible entity set, not deprecated and not required to expand. See `decisions/0041-entity-model-and-vault-vocabulary.md`.

Every entity has exactly one mandatory **anchor** vault (private) and may have any number of **additional** vaults beyond it (public, or private with a narrower declared scope) — this is normal multi-vault operation, not an edge case (section 2-D, premise 3). Each vault self-declares, in its own manifest (`hipocampo.yaml`, `decisions/0033`/`0041`):

| Field | Meaning |
|---|---|
| `instance.entity` | which entity this vault belongs to |
| `instance.role` | `anchor` (the entity's one mandatory private vault) or `additional` |
| `instance.scope_description` | required only when `role: additional` — a short statement of what belongs in this vault |

No vault lists its siblings — which other vaults belong to the same entity is never declared by any one vault about another. "All vaults of entity X" is only ever enumerable from the root manifest of a specific user with access to more than one of them; the procedure an agent uses to discover this at runtime is specified in section 12-A (`decisions/0044-vault-and-entity-discovery.md`). When an additional vault's `scope_description` alone isn't enough to decide between more than one candidate for a specific item, that is not a new mechanism — it is already covered by section 14's "insufficient evidence" behavior: the agent surfaces the ambiguity rather than guessing.

**Exposure tier** (`confidential`/`public`) is unchanged as a concept, but no longer implied by the word "vault" (section 2-D). It is carried by the repository's own name — a `restricted`/`open` suffix convention (e.g. `<entity>-restricted-vault`, `<entity>-open-vault`) — rather than by which member of a pair happens to carry a `-vault` suffix. There is still no third "structuring" tier as a separate repository: confidential knowledge that is a candidate to eventually become public keeps living in the confidential vault, with the lifecycle intent marked in the document's own frontmatter (`curation_status`, section 2), not by an additional physical separation — this reasoning, from `decisions/0029`, is unchanged by the entity model.

The formal declaration of which entity+role a specific vault implements is operationalized by the instance manifest (`hipocampo.yaml`, `decisions/0033`/`0041`). `AGENTS.md`'s "instance type" field (`corporate`/`personal`, section 2-A/11) is recommended for retirement, not yet removed from any real instance — `entity`+`role` now derive the same information the field existed to carry, and keeping it as a manually-filled echo of the manifest would reintroduce the same divergence risk this schema change resolves. See `decisions/0041` for the full rationale and migration status.

**Vocabulary note:** `personal`/`company`/`confidential`/`public` are the current canonical values, per `decisions/0035-controlled-vocabulary-dictionary.md`. The original pt-BR values (`pessoal`, `empresa`, `confidencial`, `público`) remain fully valid wherever they already appear — never treated as an error or an incompatibility — and are recognized as equivalent via `docs/vocabulary-dictionary.md`. New content and new instances use the canonical English values going forward.

**Known, separate inconsistency — not addressed here.** `decisions/0033`'s `hipocampo.yaml` manifest and the scaffold profiles (`scaffold/profiles/pessoal.yaml`/`empresa.yaml`) define `instance.tier` with a *different* pair of values (`content`/`vault`, describing repository curation level) than the `confidential`/`public` exposure tier defined in this section and in `decisions/0029`. This predates the vocabulary dictionary and is not a language issue — both value sets are now in English, but they still describe two different things under the same field name `tier`. Flagged here for a future decision; out of scope for `decisions/0035` and unaffected by the entity model.

**Full taxonomy index.** For a consolidated map of every controlled field and named concept across this schema, the vault manifest, and `AGENTS.md` — current state as of this revision, with retroactive version lineage for anything older than v1.9.0 still pending — see `docs/taxonomy.md` (`decisions/0047-taxonomy-map.md`).

## 2-D. Multi-vault and multi-entity design premises

Three premises the schema and rituals above are designed around, not incidental properties of them — see `decisions/0040-multi-vault-multi-entity-design-premises.md`:

1. **Multi-vault and multi-entity by design.** Hipocampo works with a single vault, but that is a degraded case, not the target. A single-vault instance gives up the per-repository access separation invariant 4 (section 8) provides.
2. **Confidential-first, always.** Information is confidential by default; promotion to a public vault is always a later, explicit step (the Promote action, section 13) — with no exception for content that looks "obviously public." There is never a direct write path to a public vault.
3. **The anchor vault is an existence guarantee, not a universal funnel.** Every entity's anchor guarantees that entity always has at least one private vault. It does not guarantee every user of that entity can reach it — a user without access to a specific entity's anchor still always has *some* private landing place available: at minimum, their own personal entity's anchor.

Two direct consequences of premise 3:

- **Short-term memory is per-vault, not per-entity.** Every vault — anchor or additional — has its own `inbox/` (section 5-A). There is no single, entity-wide capture point.
- **Fallback with tag.** When the correct destination for a captured item is a specific entity's vault the capturing user cannot access, the item lands in that user's own personal vault's `inbox/` instead, tagged as not permanently belonging there. Distinct from section 14's "insufficient evidence" mode — there the destination is unknown; here it is known but unreachable. The tag's exact field format, and who resolves a tagged item later, are open items.

A user's own personal anchor vault is always the first vault instantiated for that user, before any third-party entity — otherwise the fallback mechanism above has nowhere to land for that user. The mechanism that enforces this ordering is specified separately, as its own bootstrap procedure; this section only establishes the premise it depends on.

## 3. `type` — enum and expansion criterion

| Value | Usage |
|---|---|
| `note` | atomic observation that doesn't fit any of the others |
| `reference` | depersonalized, reusable concept (absorbs what would be "generic") |
| `decision` | content/architecture decision for a specific instance — distinct from the methodology's Decision Record, see section 7 |
| `project` | ongoing initiative |
| `person` | named person |
| `company` | named company (client, partner, competitor, the company itself) |
| `case` | delivered client/work case, with a quantified result |
| `framework` | methodology subject to an authorship/ownership regime (see DISCLAIMER.md) |

`context` was evaluated and dropped as a `type` value — too much overlap with `reference`/`company`. When it makes sense, it becomes a tag (`contexto`), not a retrieval classification.

**Expansion rule:** only create a new `type` value when there is a critical mass of documents that don't fit any existing value — the same principle already applied to `category` subfolders (section 4). A small, non-overlapping enum is what sustains the retrieval improvement that motivates having `type` as a structured field.

## 4. `category`

Optional field, free string. Only filled in when a thematic area has already accumulated a critical mass of documents to the point of justifying a dedicated physical subfolder — not mandatory from a topic's very first document.

**`category: frameworks` and `type: framework` coexist and are not redundant.** They are different axes: `category` is about where the document physically lives in the repository (only exists once the area already has critical mass for subfolders); `type: framework` is about the authorship/ownership regime, independent of folder. A document can be `type: framework` without `category: frameworks` — not having reached critical mass for a physical subfolder doesn't change the content's ownership regime. See `decisions/0005-category-vs-type-framework.md`.

## 5. `temporality` and the staleness cycle

Field orthogonal to `type` — controls how the staleness routine (periodic check for outdated knowledge) treats each document.

| Value | Suggested `ttl` | Staleness-routine behavior |
|---|---|---|
| `evergreen` | concrete, long date (+24 months) | Light check — "is it still true?" |
| `ephemeral` | concrete, short date (+30 to 90 days) | Aggressive — expired without renewal enters pre-marked "suggestion: archive/supersede," not just "review" |
| `contextual` | concrete, safety date (+90 to 180 days) | Double check: by the safety `ttl` AND by the status of the document in `context_anchor` — if the anchor changes to `archived`/`superseded`, the contextual document is flagged immediately, regardless of whether the `ttl` has expired yet |
| `historical` | concrete date, practically irrelevant (can be quite far out) | Skipped entirely by the staleness routine — only leaves this state via `superseded_by` |

`ttl` is **always a concrete date**, never the literal `"evergreen"` — that is `temporality`'s exclusive role. A document with `ttl: "evergreen"` as the field's value is a filling error, not a valid convention.

`context_anchor` is required only when `temporality: contextual`. Uses the same syntax as `related` (local `path.md` or cross-repo `$alias:path.md`, see section 6), but is a single value, not a list — it needs to be unambiguous which document governs the expiration.

Precedents: `evergreen`/`ephemeral` follow Andy Matuschak, "Evergreen notes" (evergreen vs. transient). `contextual` follows records-management practice (event-based retention vs. time-based retention). `historical` formalizes the already-used convention of the "(historical)" title suffix.

## 5-A. REM ritual and memory layers

Section 5 formalizes how an *already existing* document ages. This section formalizes how a *new* item — raw capture, not yet curated — enters the system and becomes a consolidated document. An optional capability per instance (see `decisions/0008-rem-ritual-and-memory-layers.md`, refined by `decisions/0016-short-term-memory-sanitization.md`).

Three layers relevant to day-to-day operation:

1. **Sensory memory** — lives outside any Hipocampo repository: the conversation/session itself, loose notes (e.g., Google Keep), an external document (e.g., Google Drive), an attached file. Never versioned in git; high loss by design.
2. **Short-term memory** — already lives inside the repository, in `inbox/`, has already passed the attention gate (e.g., a "check-in"/session dump), but is not yet atomic and not necessarily in the right place. It's a **sanitization** stage, not just a capture buffer — it needs work (splitting by concept, fixing `category`/naming/`visibility`) before becoming long-term memory.
3. **Long-term memory** — atomic document, curated, full frontmatter, correctly positioned. The main body of any Hipocampo repository.

**REM ritual (consolidation):** recommended cadence is daily, running after the same cycle's frontmatter audit (section 5-B). Two functions:

1. **Consolidate** — read `inbox/` (short-term memory, never sensory memory directly), decide for each pending item between becoming a new document, merging with an existing one, or being discarded. This is the first line of protection against misclassified content — deciding at intake whether an item is born personal or corporate (Promote action, section 13, when the natural destination differs from the repository where the item is being consolidated). When the consolidated item's destination is a corporate instance and it contains Opinion or Memory from the author/contributor, this decision includes explicitly asking whether the subjective content stays marked there or goes to the responsible author's/contributor's personal instance — see section 2, field `contains_subjective_content`, and `decisions/0026`.
2. **Update old memories** — read `meta/fila-de-manutencao.md` (produced by the frontmatter audit, section 5-B) and decide the disposition of each flagged item: revalidate (including via external research, when `source: url`), archive, supersede, or fix a field — normalizing a deprecated controlled-vocabulary value to its current form (`docs/vocabulary-dictionary.md`) is one instance of "fix a field," not a separate disposition; same explicit-plan-before-write rule applies.

The full plan (for either of the two functions) is always presented before any execution — the same explicit-request invariant (section 8) applied to this ritual. Maintenance rituals always operate at the scope of one repository at a time — each repository has its own `inbox/` and its own queue.

Additional rules (unchanged since v1.2.0): atomicity (a consolidated document = a single concept; raw material with N ideas becomes N documents); an agent harness's `memory.md` (a small, durable satellite of the agent itself) and a transfer snapshot (immutable export for migration) are neither sensory memory nor subject to the REM ritual — distinct mechanisms, not to be confused; schema evolution is reactive, only growing through critical mass (same principle as section 4).

## 5-B. Frontmatter audit

New ritual, **deterministic** (a script, not an AI agent's judgment) — recommended daily cadence, running before the same cycle's REM consolidation (section 5-A). Scans the frontmatter (never the body — frontmatter-first, section 2-B) of every document in a repository, and produces `meta/fila-de-manutencao.md`, listing: expired `ttl` (by `temporality`, section 5), missing required field (section 2), a deprecated controlled-vocabulary value still in its old pt-BR form (matched mechanically against `docs/vocabulary-dictionary.md` — no judgment involved, a literal lookup), and any other mechanically detectable violation of the frontmatter norm.

The frontmatter audit never decides disposition — it only reports. Disposition decisions always belong to the "update old memories" function of the REM ritual (section 5-A), or to an explicit human request. See `decisions/0017-deterministic-frontmatter-audit-ritual.md`.

## 5-C. Weekly structural audit

New ritual, recommended weekly cadence, with three functions: (1) reviewing the atomicity of already-consolidated documents; (2) reviewing positioning — whether the `category`/folder structure still makes sense, whether a document is outside the scope of the repository it lives in (see section 11, scope declared in `AGENTS.md`); (3) checking for sensitive-data leaks against the policy by instance type (section 2-A) — using as criterion the **instance type** (`corporate`/`personal` — deprecated pt-BR values `corporativa`/`pessoal` remain valid, see `docs/vocabulary-dictionary.md`) declared in the same "Repository scope" block of `AGENTS.md` (section 11), never inferred by the agent (see `decisions/0022-instance-type-declared-in-agents-md.md`). This is the first periodic verification mechanism for that policy, which has existed as a rule since v1.3.0 with no formal check until now. A finding from function 3 can trigger the Redbutton action (section 13, `decisions/0028`).

The structural audit is also the touchpoint for controlled-vocabulary fields that live outside document frontmatter and so are never seen by the frontmatter audit (section 5-B) — `AGENTS.md`'s "Instance type" field and `hipocampo.yaml`'s `instance.domain`/`instance.tier` (section 2-C). Whenever the audit reads either file, it checks their values against `docs/vocabulary-dictionary.md` the same way, and flags a deprecated value as a normalization candidate — never rewritten on its own.

Any finding is always presented to the responsible human before any action — moving, splitting, or removing a document never happens on its own (invariant 5). See `decisions/0019-weekly-structural-audit.md` and `decisions/0035-controlled-vocabulary-dictionary.md`.

## 5-D. Dispatcher and the four-layer taxonomy: Routine, Mechanic, Action

Two related, but separate, changes — both naming what already exists rather than introducing new behavior. See `decisions/0042-dispatcher-decoupled-from-rem.md` and `decisions/0043-dispatcher-routine-mechanic-action-taxonomy.md`.

**Dispatcher.** REM (section 5-A) is, in practice, the only process the recommended daily cadence schedules today — but frontmatter audit (5-B) and the weekly structural audit (5-C) are structural-maintenance rituals, not memory consolidation, and folding them under REM's name would break the precision the rest of this document's vocabulary depends on (REM's biological metaphor, the sensory/short-term/long-term model of section 5-A). The **Dispatcher** is a separate, neutral top-level concept: it triggers each **routine** (REM, frontmatter audit, weekly structural audit) on schedule. REM's own scope is unchanged — Consolidate and Update old memories only (section 5-A) — it does not gain responsibility for triggering the other two rituals; they become sibling routines under the Dispatcher, not children of REM. Execution order among the three routines remains fixed, exactly as already documented (frontmatter audit before REM in the same daily cycle, section 5-A; structural audit on its own weekly cadence, section 5-C). Whether this becomes dynamic — decided by the Dispatcher from per-routine metadata — is an open question, deferred until at least one real instance is actually running these rituals in practice (none are yet — dogfooding pending, see `AGENTS.md`). The format of the process registry the Dispatcher would read to make that decision is a future artifact, not yet designed.

**Four-layer taxonomy.** Orthogonal to the step-classification scheme (deterministic/discretionary/gated — how a step behaves, sections 8/14, formalized and enumerated per-step in `docs/step-classification.md`, `decisions/0048-step-classification-scheme.md`) is a taxonomy of what kind of thing a piece of behavior *is*:

- **Dispatcher** — triggers routines, by schedule (above).
- **Routine** — a scheduled process: REM, frontmatter audit, weekly structural audit. Orchestrates sequences of actions, applying judgment where the routine itself requires it.
- **Mechanic** — the ruleset a family of actions must follow. Not itself an event — the rulebook an action follows when invoked.
- **Action** — the concrete operation, invocable on demand or by a routine as a building block (for example, REM's Consolidate function invokes the CRUD mechanic's Create action when writing a new document, section 5-A).

Four mechanics, named here for the first time — the actions themselves already existed normatively, except Bootstrap, which section 12-B introduces alongside its own naming:

1. **CRUD mechanic** — Create, Read, Update, Delete (section 2-B, `decisions/0012`).
2. **Publication mechanic** — Promote, Depromote (section 13, `decisions/0027`, `decisions/0030`).
3. **Sequenced-removal mechanic** — Redbutton (section 13, `decisions/0027`, `decisions/0028`). Kept separate from the publication mechanic because the trigger profile differs (a deliberate curation decision vs. incident response), and each is expected to grow independent depth over time.
4. **Bootstrap mechanic** — Select, Orient, Instantiate, Interview (section 12-B, `decisions/0045-bootstrap-mechanic-and-profile-md.md`). Event-triggered, not scheduled, like every other mechanic here — it does not join the Dispatcher's routines.

See `decisions/0043-dispatcher-routine-mechanic-action-taxonomy.md` for why "sequenced removal," not "sequenced deletion" — the latter would contradict invariant 3 (section 8), which Redbutton itself respects (tombstone, never a silent physical delete with no trace).

## 6. `related` across repositories — the Registry

A document in any Hipocampo instance can reference another document in the same repository or in a different repository belonging to the same person/organization. The syntax distinguishes the two cases:

- No prefix (`"path/local.md"`) = same repository.
- With `$alias:` prefix (`"$alias:path.md"`) = a different repository, resolved via a `registry.md` file.

`$name`, not `{{name}}` — `{{name}}` risks being interpreted as templating-engine syntax (Jinja/Mustache) if the file ever passes through such a pipeline; `$` has no special meaning in plain YAML. See `decisions/0004-alias-syntax.md`.

`registry.md` lives in the least-restricted repository of each scope (for example, the concepts repository of a personal scope, or the main repository of a corporate scope). Format:

```markdown
| Alias | Current repository | Valid since | Note |
|---|---|---|---|
| $example-alias | owner/current-repo | YYYY-MM-DD | — |
```

**Never edit an existing registry row.** Renaming a repository = add a new row with the new name and date, preserving the old row — the same principle as `superseded_by` (section 2), applied to a repository name instead of a document.

`superseded_by` (section 2) accepts the same cross-repository `$alias:` syntax documented above for `related` — necessary for the Promote (literal path) and Depromote (section 13) actions, which replace a document in one repository with another in a different repository. See `decisions/0027-promote-depromote-redbutton.md`.

A `type: framework` document exempt from company ownership (see DISCLAIMER.md) never migrates between repositories — in that specific sense, `related` for it never needs cross-repo syntax, because it never changes address. The inverse is expected and correct: a document in any content repository can (and should) have a cross-repo `related` pointing **to** one of these exempt frameworks. The exemption prevents copying/duplicating the framework, not referencing it.

## 7. Decision Record vs. `type: decision`

Two mechanisms with different scopes — not to be confused:

- **Decision Record** (`decisions/NNNN-slug.md`) — only exists in the `hipocampo` repository. A decision about the methodology itself: schema, rule, routine. Template: Context (central question) → Decision (choice) → Rationale (why) → Discarded alternatives → Status.
- **`type: decision`** — a regular document, existing in any content repository. A decision about that specific instance's content/architecture (for example, "why this client ended up in this repository and not another").

Each content instance's `CHANGELOG.md` is narrow in scope: it only records that instance's local structural decisions. A change to Hipocampo's own rules/schema becomes a reference line ("updated to Hipocampo vX.Y, see hipocampo's CHANGELOG") instead of being re-explained.

## 8. Extension/customization and agent precedence

**Invariants** — no instance overrides these, under any circumstance:

1. No knowledge repository is public to the internet.
2. `author` is always a person, never the AI (see the scoped exception in section 2 for historical content).
3. A document is never physically deleted — only archived or superseded.
4. Access separation is always per repository, never by a label within a shared repository.
5. The agent never writes without an explicit request from the user.
6. Content declared in the repository always overrides locally-cached or customized skill state.

Invariant 3 has a formal, narrow exception, documented in `decisions/0010-legal-deletion-exception.md`: physical deletion of specific personal content is permitted when triggered by a legitimate request to erase an identifiable data subject's personal data, on a real legal basis (LGPD Art. 16 / GDPR Art. 17). `decisions/0028-broadened-trigger-2a-remediation.md` broadens this trigger to also cover a confirmed violation of the sensitive-data policy (section 2-A) identified by the structural audit (5-C) or by the instance operator, even without a formal request from the data subject — see section 13, Redbutton action. Under either trigger, the legitimacy of the request/finding is always assessed by the human responsible for the instance, never decided by the agent alone, and the removed content is replaced by a minimal record of the fact that occurred (a "tombstone") — never simply deleted without a trace, and never an open door for deletion out of convenience.

Invariant 6 governs a different axis than the agent precedence hierarchy below: skill-versus-repository authority, not conversation-request-versus-instance-extension precedence. It applies generically to any content the repository declares — `AGENTS.md`, the `hipocampo.yaml` manifest (`decisions/0033`/`0041`), `profile.md` (section 12-B, `decisions/0045`), and any future structured repository file — not a closed list naming specific files, so the invariant does not need amending every time the methodology gains a new one. It exists as a safety fallback against a user's local skill copy going stale relative to the repository, or being hand-modified in a way that no longer matches what the repository actually declares. For the invariant to resolve without ambiguity, no two repository-side files may declare the same field — the reason `AGENTS.md`'s "instance type" field is recommended for retirement (section 2-C, `decisions/0041`) rather than kept as a duplicate echo of the manifest, not a stylistic preference. See `decisions/0046-repository-content-overrides-skill-local-state.md`.

**Adjustable per instance** — always documented, never implicit, in an "Local extensions to Hipocampo vX.Y" block in that repository's `AGENTS.md` (see section 11): `category` subfolders, suggested default `ttl` per content type, extra instance-specific rituals (including whether/how the REM ritual from section 5-A is adopted), commit/branch naming.

**Agent precedence hierarchy**, from most specific to most general:

1. Explicit user request in the current conversation — within the limits of the invariants.
2. Extension/override documented locally in the instance.
3. Base rule from this `SPEC.md`.
4. Default convention from `hipocampo-toolkit`, in the absence of everything else.

No layer overrides an invariant. If a request would violate an invariant, the agent follows the invariant and explicitly says so — it never silently complies nor silently refuses.

## 9. Versioning

The methodology itself follows [SemVer](https://semver.org/lang/pt-BR/): MAJOR for a breaking change (requires active migration, see `MIGRATIONS.md`), MINOR for a new capability compatible with what already exists, PATCH for clarification or correction that doesn't change behavior. Each change's scope is classified by a concrete operational test, not loose judgment: it's MAJOR when an existing instance, with no action, would become formally incompatible; MINOR when the instance stays valid with no action, even if it lags behind the new capability; PATCH is clarification/correction with no new capability. See `decisions/0023-operational-criterion-for-semver-scope.md`.

Every released version is marked with a git tag **and** a published GitHub Release, always together, in the same step of the release routine — never one without the other. Each instance declares, in its own `AGENTS.md`/`CLAUDE.md`, the version or compatibility range it implements (example: "Follows Hipocampo ^1.0.0").

Every new version follows a mandatory routine before being considered complete: scope classification (above), tag + Release, `CHANGELOG.md` update, skill/scaffold synchronization (formerly `hipocampo-toolkit` synchronization, before its consolidation into this repository, `decisions/0032`), and an update to **[UPGRADE.md](UPGRADE.md)** — a cumulative, idempotent checklist of what an existing instance needs to have to conform to the current version, different from `MIGRATIONS.md` (which only covers MAJOR jumps). See `decisions/0014-mandatory-release-routine.md` and `decisions/0024-upgrade-md-cumulative-checklist.md`.

Cutting a release (tag + published GitHub Release) doesn't need to happen for every accepted change — work accumulates on `main` until critical mass or a natural pause, see `decisions/0021-release-cadence-policy.md`. An urgent change (a fix, not a new capability) ships as a PATCH, outside the normal accumulation cycle.

Before a release routine is considered complete, **[RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md)** operationalizes the steps above into a single concrete run-through, and **`scripts/validate_hipocampo.py`** (run automatically in CI on every pull request against `main`, `.github/workflows/validate.yml`) deterministically checks the methodology repository's own structural integrity — Decision Record template compliance, internal link resolution, and version consistency between `README.md` and `CHANGELOG.md`. See `decisions/0036-deterministic-validation-of-repository-structure.md` and `decisions/0037-minimal-release-gate-checklist.md`.

## 10. Migrating pre-existing content

Bringing in content from outside Hipocampo (a legacy system, an export from another tool) or from a previous version of the methodology never copies the original file directly into the destination repository. The frontmatter is always rewritten from scratch, per the current schema (section 2); the body is adjusted per the current rules of atomicity, naming, and privacy (section 2-A), documenting in `revision_note` what was preserved verbatim and what was changed, and why. See `decisions/0011-migration-never-direct-copy.md`. The same discipline is reused by the Promote action's elegant path (section 13).

## 11. Instruction file: AGENTS.md and CLAUDE.md

`AGENTS.md` is the canonical operational instruction file for any Hipocampo instance — invariants, local extensions (section 8), frontmatter reference, and the **repository scope**: what should and shouldn't be stored there, and where whatever doesn't belong goes instead, plus the **instance type** (`corporate` or `personal` — deprecated pt-BR values `corporativa`/`pessoal` remain valid, `docs/vocabulary-dictionary.md`, see section 2-A). These items are mandatory, never implicit — same principle as local extensions — and are the source the maintenance rituals (REM, section 5-A; structural audit, section 5-C) consult to decide whether a document belongs in the repository it's in and which variant of the sensitive-data policy applies.

`CLAUDE.md` continues to exist in every instance, but as a thin pointer — a few lines, referring to `AGENTS.md` as the source of truth, without duplicating content. See `decisions/0015-agents-md-canonical-instruction-file.md`.

Instances that already existed before this section (v1.6.0 and earlier, when `CLAUDE.md` was still the canonical file) migrate the next time they're touched — not automatic (same principle as any MINOR change, see DISCLAIMER.md). See `UPGRADE.md` for the full migration checklist.

## 12. Multi-account author identity

When the person behind `author` operates more than one git account (e.g., personal and one tied to an employer) that need to resolve to the same human `author` (invariant 2), that relationship is recorded in the `AGENTS.md` of the least-restricted personal repository — never in the public `hipocampo`/`hipocampo-toolkit`. It is discovered from there at runtime (section 12-A), not tracked in a separate local file — `profile.md` (section 12-B) is the one place a user's own git-handle facts are recorded outside the repositories themselves.

Between a person's personal instance and corporate instance, the access invitation (repository collaborator) always starts from the personal account inviting the professional one into the **personal** second brain — never the reverse. Personal identity is always the anchor of trust; the employing organization never has standing to grant or deny access to someone's personal knowledge. See `decisions/0020-multi-account-author-identity.md`.

## 12-A. Vault and entity discovery

Section 2-C left the runtime procedure for "which vaults belong to entity X" unspecified, pointing here. This section is that procedure. See `decisions/0044-vault-and-entity-discovery.md` for the full rationale, including why an earlier hub-spoke design was rejected.

**Discovery, not storage.** No repository router is stored anywhere, generic or personal. At the start of a session, the agent reads the manifest of the user's own anchor vault, discovers every entity/vault address and identity field that manifest declares, and caches the result in **sensory memory** (section 5-A) — ephemeral, never versioned in git, rediscovered fresh each new session, not re-asked for within the same one.

**No graph between sibling vaults.** Each vault self-declares only its own `entity`/`role`/`scope_description` (section 2-C) — never a pointer to any sibling vault, anchor or additional. "All vaults of entity X" is only ever computed from a specific user's own root manifest, for whichever of that entity's vaults that user happens to have access to — never from a vault enumerating its own siblings.

**Known limitation.** Access granted outside the Bootstrap mechanic (section 12-B) — for example, a direct GitHub collaborator invite — is not auto-discovered; it requires manual registration in that case, the same posture section 14's "insufficient evidence" behavior already takes toward a gap the agent cannot close on its own.

**Consistency checking.** Without sibling pointers, there is no "does every vault point back correctly" check to run. The weekly structural audit (section 5-C) instead confirms that each vault's own self-declaration is still valid and its address still reachable — no new ritual, an extension of the existing one.

**Step classification (sections 8/14).** Reading and caching the root manifest is deterministic-or-discretionary, ungated. Registering a new vault (the Instantiate action, section 12-B) is gated, per invariant 5, like any other durable write.

**What remains local.** One pointer — which repository is the user's own anchor vault — cannot itself come from any manifest, because it is the address of the first manifest to read. This is not a router; it is a single value, not a table. Neither this section nor `decisions/0044` names where that pointer lives — see `decisions/0045-bootstrap-mechanic-and-profile-md.md` (section 12-B), which creates the anchor vault this pointer refers to, without yet resolving the storage question either.

## 12-B. Bootstrap mechanic: instantiation and profile.md

**Classification.** Bootstrap is a **mechanic** (section 5-D), not a routine — event-triggered, not scheduled; it never joins the Dispatcher's process registry. See `decisions/0045-bootstrap-mechanic-and-profile-md.md`.

**Trigger.** "Discovery attempted, nothing found" (section 12-A: the agent tries to read the user's own anchor-vault manifest and finds none) is the recognized condition that launches Bootstrap — a positive signal to act on, not a generic failure state handled by section 14.

**Personal bootstrap is a prerequisite.** Before any third-party entity, a new user's first vault is always their own personal anchor (section 2-D, premise 3) — the fallback-with-tag mechanism has nowhere to land otherwise. Bootstrap enforces this as its first step, even when what actually brought the user in was an invitation to someone else's entity.

**Four actions, in order:**

1. **Select** — which repository, for which entity. Fixed (personal, anchor) for a user's very first vault; the normal profile/entity choice (`skill/references/instantiation.md`) for any later one.
2. **Orient** — a conversational walkthrough of what Hipocampo is and why it needs a repository, including platform-specific installation notes (`docs/getting-started-non-technical.md`) — delivered as conversation, not as a link to go read alone. Conditional: only on a user's first (personal) vault, and only with a signal the user doesn't already know what Hipocampo is.
3. **Instantiate (skeleton)** — the existing scaffolding mechanism (`decisions/0032`, `skill/references/instantiation.md`), creating the repository and its `hipocampo.yaml`. Ordered before Interview — there is nothing to write Interview's answers into until the skeleton exists.
4. **Interview** — collects `profile.md`'s fields (below). Full depth on a user's very first instantiation; a lighter pass afterward, since `profile.md` already answers identity questions from the second vault onward. A separate step from Orient's conversation — "what is a repository" is onboarding content, not a `profile.md` field. Closes the loop with **Instantiate (content)**, filling the skeleton from step 3, through the same explicit-confirmation gate every other durable write already goes through (invariant 5).

**`profile.md`.** A structured, fixed-schema file — closer in kind to `hipocampo.yaml` (`decisions/0033`) than to a `type: person` content document, and outside the frontmatter/staleness/structural-audit cycle that governs ordinary knowledge documents. Lives at the root of the user's personal anchor vault. Fields:

```yaml
name: ""                 # full name
preferred_name: ""       # optional — how the user prefers to be addressed
emails: []
github_handles: []       # resolved per entity via discovery (section 12-A), not a separate routing table
updated: "YYYY-MM-DD"     # date of last confirmed edit
```

A fixed, small schema by design — a new field is added through its own Decision Record, not through ad hoc capture during an Interview. Capture happens conversationally, but the written result always passes through the same explicit-confirmation gate (invariant 5) as any other durable write — conversational discovery is a capture method, not an exemption from confirmation. `profile.md` is not (yet) an output the scaffold's declarative profile system (`scaffold/profiles/`) generates — the Interview action writes it directly.

**Invite template.** `docs/invite-template.md` provides static, public text for bringing someone else into an entity — content whose only role is to trigger this mechanic in whoever receives it; not itself an action or part of the mechanic.

## 13. Cross-repository lifecycle actions: Promote, Depromote, Redbutton

Three actions that move or remove content between repositories of the same person/organization, complementary to the single-repository CRUD (section 2-B). The REM ritual's curation (section 5-A, Consolidate function) and the structural audit (5-C) are the first line of protection against misplaced content — these three actions exist for when that curation fails, or for deliberate reclassification of already-existing content. See `decisions/0027-promote-depromote-redbutton.md` and `decisions/0028-broadened-trigger-2a-remediation.md`. Promote and Depromote are governed by the publication mechanic; Redbutton by the sequenced-removal mechanic — both formally named in section 5-D. The actions and their behavior are unchanged by that naming.

### Promote — personal → corporate, or graduation within the same domain

Two path variants, always presented together before any writing (invariant 5), plus a second application case:

**Elegant path (recommended by default):** creates a new document in the corporate repository, following `decisions/0011`'s discipline — frontmatter rewritten from scratch for the destination's schema/policy, never copied verbatim; body depersonalized as needed; sensitive-data policy compliance check (section 2-A) before writing; `author` corrected to the corporate identity (`decisions/0020`); information-type labels (`decisions/0026`) re-evaluated in the new context. The source personal document **does not change `status`** — it stays active, gaining only a new `related` pointing (`$alias:`) to the corporate document, with `revision_note` recording the date and nature of the derivation. The corporate document points back to the personal one the same way. The two documents evolve independently from then on — this is not the replication vetoed by `decisions/0002`, because there was never an expectation of them staying in sync.

**Literal path (rare):** the personal document is actually transferred — `status: superseded`, `superseded_by: $alias:destination`, `temporality: historical`, content preserved as it was at the moment of promotion. Before any write on this path, the agent explicitly explains to the user: (a) this transfers ownership of the content to the company, per `decisions/0007` — the corporate repository's `LICENSE` declares the company as owner; (b) this is not trivially reversible — full reversal (the document going back to living fully in the personal domain) is not a routine action. Only proceeds with explicit confirmation after this warning.

**Graduation within the same domain (new, `decisions/0030`):** Promote also covers the case where a `company-confidential` document marked `curation_status: staged` (section 2-C) is ready to become `company-public` — same ownership domain the whole time, so it always uses the elegant path (never the literal one, since there's no new ownership transfer at stake, `decisions/0007` doesn't change in this case). The source document is not deleted; `curation_status` either becomes `permanent` (ending its candidacy) or the document ends up with `related` pointing to the new public document, at the discretion of whoever confirms the action. Only a `staged` document is eligible for this variant — a `permanent` document needs an explicit `curation_status` reclassification first, a human decision separate from the promotion itself.

### Depromote — moving down within the same ownership domain

Moves content between repositories of the same owner (e.g., `company-public` → `company-confidential`, or between personal variants), without crossing the personal/corporate boundary — so it doesn't carry the ownership question of the literal Promote, and doesn't need the equivalent explicit warning. Mechanics: `status: superseded` at the source, `superseded_by: $alias:destination`. A literal reversal of Promote (corporate → personal, crossing the ownership boundary back) is out of scope for this action — it is not automated; it's a case-by-case decision by the responsible human, outside Hipocampo's normal flow, in the same spirit as `DISCLAIMER.md` ("does not replace legal compliance").

### Redbutton — remediation of a sensitive-data policy violation

Extension of `decisions/0010`'s trigger (see `decisions/0028`): physical deletion of the specific content, replaced by a tombstone, triggered not only by a data subject's request, but also when the structural audit (5-C) or the instance operator identifies content that violates the sensitive-data policy (section 2-A), even without a formal request. Same mechanism as `decisions/0010`: the decision is always explicitly human, never automatic; the tombstone documents the fact without repeating the data; it cleans the repository's current state, not the git history (which requires a manual, rare rewrite for that, decided case by case). Reserved for a real policy violation or legal risk — not the mechanism for removing a misplaced opinion or memory with no legal risk (that's a regular Update, no tombstone, see `decisions/0026`).

## 14. Behavior under failure and recovery

The sections above prescribe correct-path behavior — what an agent does when everything needed is available and consistent. This section prescribes the complementary case: what a conformant agent does when it isn't. None of these six situations is exotic; each has already happened in real use of this methodology, or is a predictable consequence of running an agent against fallible tools, incomplete input, and a human who might ask for the wrong thing. The common thread across all six: an agent operating Hipocampo never silently guesses, never silently refuses, and never treats "I don't know how to proceed" as a reason to proceed anyway. It says what's wrong, in plain terms, and hands the decision to the human when the decision is genuinely the human's to make — the same posture invariant 5 (section 8) already requires for writing, generalized here to judgment under uncertainty.

**Insufficient evidence.** When an agent is asked to state something as fact (a Fact-type entry per `decisions/0026`'s taxonomy, a `source: url` claim, a frontmatter value inferred rather than declared) and the available material doesn't actually support the claim at the confidence the request implies, the agent says so explicitly instead of filling the gap with a plausible-sounding answer. It states what it does know, what it doesn't, and — when the missing evidence is checkable — proposes how to check it (a search, a read of a specific file, a question back to the human) rather than either inventing the answer or refusing the whole task. This mirrors the existing rule in section 2-B for an expired `ttl` (flag, don't silently trust); it extends the same posture to any claim, not only staleness.

**Frontmatter↔body contradiction.** When a document's frontmatter and its body content disagree (e.g., `status: archived` but the body reads as current guidance; `visibility: public` on a body that plainly contains restricted material; a `related` link to a document whose content no longer matches the relationship it implies) — encountered incidentally during a read, not only during the frontmatter audit's scan (section 5-B, which only ever reads frontmatter and so cannot detect this class of defect by itself) — the agent flags the contradiction and does not act on either side of it as authoritative until a human resolves which one is correct. It never silently prefers the frontmatter over the body or vice versa, and it never edits either side to make them agree without an explicit instruction to do so.

**Unavailable tool.** When a tool the current task depends on is unavailable (the GitHub MCP integration is down or rate-limited, a write permission is missing — the `.github/workflows/` scope restriction encountered during Fase G, `decisions/0036`, is a real, already-documented instance of this) the agent does not retry indefinitely, does not silently drop the affected part of the task while reporting the rest as complete, and does not fall back to an unrequested alternative mechanism (e.g., writing outside version control, or through a different account) without flagging that it's a fallback. It names exactly what couldn't be done and why, completes whatever part of the task doesn't depend on the unavailable tool, and states the remaining step as a pending action — for the human to complete manually or to unblock (e.g., granting a missing permission) — never presented as done when it isn't.

**Interruption mid-ritual.** The REM ritual and the frontmatter/structural audits (sections 5-A, 5-B, 5-C) are explicitly scoped to run to completion within one repository per pass; none of them defines a checkpoint/resume mechanism. If a ritual is interrupted partway (the session ends, the human stops responding, a tool failure per above), the agent does not assume partial writes already made are safe to leave half-applied as if they were the finished ritual — on resuming, it re-derives the ritual's current state from the repository itself (what `meta/fila-de-manutencao.md` already reflects, what frontmatter/`related` already changed) rather than from memory of the interrupted conversation, and explicitly tells the human the ritual was left incomplete and from where it's resuming, before continuing. Invariant 5 (explicit request before writing, section 8) applies again at resumption — resuming is not assumed to still carry the same standing permission if enough time or context has passed that the human may no longer expect it.

**Unsafe request.** A request that would violate an invariant (section 8), or the sensitive-data policy for the instance's declared type (section 2-A), is refused at the specific point of violation — not by refusing the entire surrounding task. The agent states which invariant or policy clause is at stake and, where a compliant alternative exists (e.g., recording a fact without the banned verbatim detail, per section 2-A's exploit-detail rule), offers it instead of a bare refusal. This is the same behavior section 8 already prescribes for an invariant conflict ("the agent follows the invariant and explicitly says so — it never silently complies nor silently refuses"); this entry makes explicit that the same rule governs safety-relevant requests generally, not only the five enumerated invariants.

**Incompatible migration.** When an instance's declared version/compatibility range (`AGENTS.md`, section 11) is behind a MAJOR change documented in `MIGRATIONS.md`, and a requested action depends on behavior only the newer version defines, the agent does not silently operate as if the migration had already happened, and does not silently apply the migration on the instance's behalf. It names the version gap, points at the relevant `MIGRATIONS.md` entry, and confirms with the human whether to proceed with the pre-migration behavior, pause the requested action until the migration is applied, or apply the migration now as an explicit, separate, confirmed step — never folded silently into an unrelated request.

See `decisions/0038-failure-and-recovery-behavior.md`. Minimal representative scenarios exercising both this section and ordinary correct-path behavior are collected in `docs/evaluation-scenarios.md` (`decisions/0039-minimal-evaluation-scenarios.md`).

## Version history

See [CHANGELOG.md](CHANGELOG.md).
