# Vocabulary dictionary — deprecated pt-BR values ↔ current English values

**Contract revision:** `1.0` — compatibility decision states added by Change Set `0058`.

Canonical de:para reference for every controlled-vocabulary field this methodology defines, since `decisions/0035-controlled-vocabulary-dictionary.md` made English the canonical vocabulary. **A deprecated value in the "pt-BR" column is never an error, never a schema violation, and never breaks compatibility with any instance.** It is fully equivalent to its English counterpart, permanently — there is no removal deadline. This document also registers controlled operational terms that have no pt-BR alias pair, so new terms remain discoverable and governed in one place.

## How to use this dictionary

1. **Reading a document or a repository-level file** (`AGENTS.md`, `hipocampo.yaml`): treat a value in the "Deprecated (pt-BR)" column exactly the same as its "Canonical (en)" counterpart. Never flag it as a schema violation, never refuse to process a document because of it, never assume the instance is "behind" in any way that matters functionally.
2. **Writing new content, or scaffolding a new instance**: always use the "Canonical (en)" value. This applies even inside an instance whose *other*, pre-existing values are still pt-BR — a new document in an otherwise-pt-BR vault still gets `source: conversation`, not `source: conversa`. This does not imply migrating anything else in that instance.
3. **Migrating an existing deprecated value**: never rewritten silently, per invariant 5 (`SPEC.md`, section 8 — the agent never writes without an explicit request). The mechanism is ritual-driven, not immediate or forced:
   - For a **document frontmatter field** (currently: `source`): the read-time validation (`SPEC.md` section 2-B) and the daily frontmatter audit (`SPEC.md` section 5-B) both flag a deprecated value the same way they flag an expired `ttl`. The REM ritual's "update old memories" function (`SPEC.md` section 5-A) is where a human actually confirms the fix, presented like any other field fix — never auto-applied, never batched without review.
   - For a **repository-level field** (`hipocampo.yaml`'s `instance.policy_profile`, `instance.curation_level`, or a legacy field): these aren't document frontmatter, so the frontmatter audit never sees them. The weekly structural audit (`SPEC.md` section 5-C, function 4) is the touchpoint.
   - In both cases, a normalization is a small, low-risk edit — but it's still presented as a plan and confirmed before writing, same as any other change under invariant 5. It is fine for an instance to never confirm it; the deprecated value keeps working indefinitely.
4. **Scope — what this dictionary does *not* cover.** `category` (`SPEC.md`, section 4) is a free string, not a controlled enum — whatever value an instance already uses, in whatever language, is correct as-is; this dictionary makes no claim about it and there is nothing to normalize. Likewise, filenames that are literal tokens referenced programmatically by the scaffold engine (`scaffold/profiles/pessoal.yaml`, `scaffold/profiles/empresa.yaml`, `scaffold/license-templates/LICENSE-pessoal.md`, `scaffold/license-templates/LICENSE-corporativo.md`) were deliberately not renamed (PR #27) and are out of scope here too — only the *content* of those files is covered.

## Dictionary

| Field | Where it appears | Deprecated (pt-BR) | Canonical (en) | Governing decision(s) |
|---|---|---|---|---|
| `source` | document frontmatter (`SPEC.md`, section 2) | `conversa` | `conversation` | `decisions/0035` |
| `source` | document frontmatter | `interno` | `internal` | `decisions/0035` |
| `domain` (superseded, `decisions/0041` — kept for an instance that hasn't migrated to `entity`/`role`) | `hipocampo.yaml`, `instance.domain` / `scaffold.profile`'s meaning (`SPEC.md`, section 2-C) | `pessoal` | `personal` | `decisions/0029`, `0035`, `0041` |
| `domain` (superseded, see above) | `hipocampo.yaml` | `empresa` | `company` | `decisions/0029`, `0035`, `0041` |
| exposure `tier` | `SPEC.md` section 2-C / `decisions/0029` concept (confidential vs. public access) | `confidencial` | `confidential` | `decisions/0029`, `0035` |
| exposure `tier` | same | `público` | `public` | `decisions/0029`, `0035` |
| `instance.curation_level` | `hipocampo.yaml` / scaffold profile input | `conteudo` | `content` | `decisions/0033`, `0035`, `0052` |
| `instance.policy_profile` | `hipocampo.yaml` | `corporativa` | `corporate` | `decisions/0022`, `0035`, `0052` |
| `instance.policy_profile` | `hipocampo.yaml` | `pessoal` | `personal` | `decisions/0022`, `0035`, `0052` |

**Legacy compound repository descriptors** (used in prose, never a manifest field) were built from `domain`+exposure `tier`: `empresa-confidencial` → `company-confidential`; `empresa-público` → `company-public`; `pessoal-confidencial` → `personal-confidential`; `pessoal-público` → `personal-public`.

**Current operational descriptors** are prose labels assembled from the manifest rather than a controlled field: `personal-open-vault` = personal entity/policy, `role: additional`, `curation_level: content`; `personal-restricted-vault` = personal entity/policy, `role: anchor`, `curation_level: vault`; `company-open-vault` = corporate policy, `role: anchor`, `curation_level: content`; `company-restricted-vault` = corporate policy, `role: additional`, `curation_level: vault`. The real `instance.entity` remains extensible and authoritative (for example, it is not replaced by the generic word `company`). `open` and `restricted` describe relative access posture only: every such vault remains private and proprietary, and neither descriptor grants legal permission beyond its root `LICENSE`.

## Compatibility aliases

## Unreleased V3 candidate terms

These terms are candidate V3 governance concepts, not changes to the active
v2.1.1 frontmatter contract:

| Term | Meaning | Governing decision |
|---|---|---|
| `entity` profile | Broad entity-scoped vault policy | `decisions/0074` |
| `team` profile | Collaborative single-entity vault policy | `decisions/0074` |
| `personal` profile | User-private vault policy | `decisions/0074` |
| `Owner` | Boundary and policy accountability role | `decisions/0074` |
| `Authority` | Current-knowledge authority for an entity and scope | `decisions/0074` |
| `Curator` | Processing and reconciliation role | `decisions/0074` |
| `User` | Authorized consumer or operator | `decisions/0074` |
| `Source` | Provenance origin; not a governance role | `decisions/0074` |

### Unreleased V3 conversational aliases

The candidate alias map and ambiguity rules are maintained in
[`docs/v3-vocabulary-and-aliases.md`](v3-vocabulary-and-aliases.md), with
fixtures in [`docs/v3-vocabulary-fixtures.yaml`](v3-vocabulary-fixtures.yaml).
These aliases resolve conversational wording to the canonical V3 vocabulary;
they do not add new persisted types to the active v2.1.1 contract.

The V3 `Source` concept is broader than the v2 frontmatter `source` field. The
frontmatter field remains governed by `SPEC.md`; the V3 concept identifies the
origin of a Record or Chunk and may carry a stable non-secret reference.

- `instance.tier: conteudo | content | vault` is a legacy curation-level field accepted only for manifests created before v2.1.0. New manifests use `instance.curation_level`.
- An `AGENTS.md` “Instance type” declaration is a legacy fallback only when `instance.policy_profile` is absent. Once the manifest field is added, remove the duplicate declaration in the same confirmed update.

## Compatibility decision states

These controlled operational values are defined in `COMPATIBILITY.yaml`, not in
document frontmatter. They are not language aliases and must not be confused
with epistemic types or with the `status` field:

| Term | Meaning | Permitted action |
|---|---|---|
| `compatible` | Required declarations, integrity and ranges align. | Allow, subject to other gates. |
| `compatible_with_upgrade` | The tuple is operable and a non-blocking upgrade is recommended. | Allow with notice. |
| `migration_required` | A known incompatible methodology transition exists. | Block until migration is confirmed. |
| `unsupported_or_unknown` | A declaration is missing, malformed, unsupported or unestablished. | Block until reviewed. |
| `access_unavailable` | A required source cannot be read. | Block until access is restored. |

The values are introduced by Change Set `0058-compatibility-contract`. Their
precedence and complete contract remain in `COMPATIBILITY.yaml`; this table is
the vocabulary registry, not a second rule source.

Nominal-citation review is an opt-in check over explicitly supplied new or
changed files. `scripts/validate_nominal_citations.py` uses placeholders and
the project operator handle only; it does not retain a third-party name list
and does not rewrite or audit the legacy corpus.

## Change history

## Term governance

Before a contribution introduces a canonical term, alias, enum value, schema field, or named operating concept, it searches this dictionary and `docs/taxonomy.md`. An accepted term is registered in both surfaces when applicable, with its owning SPEC section or Decision Record; a Change Set records the terminology review even when the result is not applicable. Free prose and existing user-authored `category` values remain outside this controlled vocabulary.

- `decisions/0035-controlled-vocabulary-dictionary.md` (this file's origin) — initial dictionary, covering `source`, `domain`, both historical `tier` concepts, and `AGENTS.md`'s `Instance type`.
- `decisions/0052-consistency-contracts-anchor-registration-and-codex-distribution.md` — resolves the field-name collision with `instance.curation_level` and moves the policy selector to `instance.policy_profile`.
- `decisions/0041-entity-model-and-vault-vocabulary.md` — `instance.domain` (`hipocampo.yaml`) superseded by `instance.entity`/`instance.role`/`instance.scope_description`; "vault" redefined as a generic noun for any knowledge repository (previously implied confidential-only, via the `-vault` suffix asymmetry); `AGENTS.md`'s "Instance type" field recommended for retirement rather than treated as a permanent, unharmonized second vocabulary.
- `decisions/0054-private-proprietary-content-license-boundary.md` — `open`/`public` vocabulary is constrained to private-context handling and relative posture; it never confers an open license or publication permission.
