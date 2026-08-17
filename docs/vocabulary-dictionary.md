# Vocabulary dictionary — deprecated pt-BR values ↔ current English values

Canonical de:para reference for every controlled-vocabulary field this methodology defines, since `decisions/0035-controlled-vocabulary-dictionary.md` made English the canonical vocabulary. **A deprecated value in the "pt-BR" column is never an error, never a schema violation, and never breaks compatibility with any instance.** It is fully equivalent to its English counterpart, permanently — there is no removal deadline.

## How to use this dictionary

1. **Reading a document or a repository-level file** (`AGENTS.md`, `hipocampo.yaml`): treat a value in the "Deprecated (pt-BR)" column exactly the same as its "Canonical (en)" counterpart. Never flag it as a schema violation, never refuse to process a document because of it, never assume the instance is "behind" in any way that matters functionally.
2. **Writing new content, or scaffolding a new instance**: always use the "Canonical (en)" value. This applies even inside an instance whose *other*, pre-existing values are still pt-BR — a new document in an otherwise-pt-BR vault still gets `source: conversation`, not `source: conversa`. This does not imply migrating anything else in that instance.
3. **Migrating an existing deprecated value**: never rewritten silently, per invariant 5 (`SPEC.md`, section 8 — the agent never writes without an explicit request). The mechanism is ritual-driven, not immediate or forced:
   - For a **document frontmatter field** (currently: `source`): the read-time validation (`SPEC.md` section 2-B) and the daily frontmatter audit (`SPEC.md` section 5-B) both flag a deprecated value the same way they flag an expired `ttl`. The REM ritual's "update old memories" function (`SPEC.md` section 5-A) is where a human actually confirms the fix, presented like any other field fix — never auto-applied, never batched without review.
   - For a **repository-level field** (currently: `AGENTS.md`'s "Instance type"; `hipocampo.yaml`'s `instance.domain`/`instance.tier`): these aren't document frontmatter, so the frontmatter audit never sees them. The weekly structural audit (`SPEC.md` section 5-C, function 4) is the touchpoint — whenever it reads either file for its other checks, it also checks the value against this dictionary, and flags a deprecated value as a normalization candidate the same way it flags any other finding.
   - In both cases, a normalization is a small, low-risk edit — but it's still presented as a plan and confirmed before writing, same as any other change under invariant 5. It is fine for an instance to never confirm it; the deprecated value keeps working indefinitely.
4. **Scope — what this dictionary does *not* cover.** `category` (`SPEC.md`, section 4) is a free string, not a controlled enum — whatever value an instance already uses, in whatever language, is correct as-is; this dictionary makes no claim about it and there is nothing to normalize. Likewise, filenames that are literal tokens referenced programmatically by the scaffold engine (`scaffold/profiles/pessoal.yaml`, `scaffold/profiles/empresa.yaml`, `scaffold/license-templates/LICENSE-pessoal.md`, `scaffold/license-templates/LICENSE-corporativo.md`) were deliberately not renamed (PR #27) and are out of scope here too — only the *content* of those files is covered.

## Dictionary

| Field | Where it appears | Deprecated (pt-BR) | Canonical (en) | Governing decision(s) |
|---|---|---|---|---|
| `source` | document frontmatter (`SPEC.md`, section 2) | `conversa` | `conversation` | `decisions/0035` |
| `source` | document frontmatter | `interno` | `internal` | `decisions/0035` |
| `domain` | `hipocampo.yaml`, `instance.domain` / `scaffold.profile`'s meaning (`SPEC.md`, section 2-C) | `pessoal` | `personal` | `decisions/0029`, `0035` |
| `domain` | `hipocampo.yaml` | `empresa` | `company` | `decisions/0029`, `0035` |
| exposure `tier` | `SPEC.md` section 2-C / `decisions/0029` concept (confidential vs. public access) | `confidencial` | `confidential` | `decisions/0029`, `0035` |
| exposure `tier` | same | `público` | `public` | `decisions/0029`, `0035` |
| curation-level `tier` | `hipocampo.yaml`, `instance.tier` / scaffold profile `tier` input (`decisions/0033`) — **a different concept from exposure `tier` above; see the note below** | `conteudo` | `content` | `decisions/0033`, `0035` |
| `Instance type` | `AGENTS.md`, "Repository scope" block (`decisions/0022`) | `corporativa` | `corporate` | `decisions/0022`, `0035` |
| `Instance type` | `AGENTS.md` | `pessoal` | `personal` | `decisions/0022`, `0035` |

**Compound repository-descriptor labels** (used in prose, not a single field's literal value — built by combining `domain`+exposure `tier`): `empresa-confidencial` → `company-confidential`; `empresa-público` → `company-public`; `pessoal-confidencial` → `personal-confidential`; `pessoal-público` → `personal-public`.

## Known, unresolved inconsistencies (not fixed by this dictionary)

- **Two different things are both called `tier`.** `SPEC.md` section 2-C and `decisions/0029` define an *exposure* tier (`confidential`/`public` — who can read it). `decisions/0033` and the scaffold profiles (`scaffold/profiles/pessoal.yaml`/`empresa.yaml`) define a *curation-level* tier (`content`/`vault` — how the repository's LICENSE and visibility range are structured) under the same field name, `instance.tier` in `hipocampo.yaml`. Both value sets are translated to English by `decisions/0035`, but which concept `tier` actually names is not resolved here — flagged for a future decision.
- **`domain` and `AGENTS.md`'s "Instance type" are two vocabularies for a related-but-distinct concept**, deliberately not harmonized (`decisions/0033`). Both are now independently in English, but still two separate fields an operator fills in separately.

## Change history

- `decisions/0035-controlled-vocabulary-dictionary.md` (this file's origin) — initial dictionary, covering `source`, `domain`, both `tier` concepts, and `AGENTS.md`'s `Instance type`.
