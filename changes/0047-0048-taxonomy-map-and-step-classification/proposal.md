# Change Set — 0047/0048: Taxonomy map and step-classification reference (Lote E1)

## Summary

Adds two new reference documents, each with its own Decision Record:

- **`docs/taxonomy.md`** (`decisions/0047`) — a single index of every controlled field, enum, and named concept the methodology defines, pointing at its authoritative source. Current-state coverage is complete; retroactive version lineage for anything predating `v1.9.0` is explicitly marked `TBD — Lote E2` rather than silently incomplete or guessed at.
- **`docs/step-classification.md`** (`decisions/0048`) — formalizes Hipocampo's own three-value step-behavior scheme (deterministic/discretionary/gated, already named in passing in `SPEC.md` §5-D/§14) and enumerates every currently-named routine, mechanic action, and failure-recovery mode against it.

This is **Lote E, part 1 (E1)** of the v2.0.0 taxonomy revision sequencing — deliberately last, because both documents' value depends on documenting the *result* of Lotes A–D, which just landed. `docs/taxonomy.md` is itself split further: this Change Set delivers structure and current-state coverage; a second Change Set (Lote E2, not part of this one) will do the retroactive backfill across releases `v1.0.0`–`v1.9.0`.

Neither document introduces a new rule, obligation, schema field, or write gate — both consolidate and index what `SPEC.md` and existing Decision Records already establish, closing a "no single place to look" gap rather than changing what's required. `docs/step-classification.md` additionally narrows (but does not close) a specific gap `conformance/moda.yaml`'s `distribution_of_agency` control already names.

## Class

**operational** — changes execution guidance and reference material (where to look for the current state of the taxonomy, and how a given step is classified) without changing a normative obligation. No new invariant, no new schema field, no new cross-repository mechanism, no new sensitive-data rule — none of the `normative`-triggering conditions in `docs/change-management.md`'s table fire. Still `Required` per the class table, since `operational` always requires a Change Set regardless of which specific trigger fires.

## Semver

**minor** — purely additive reference documentation plus two small pointer sentences in `SPEC.md` (§2-C, §5-D) linking to the new documents. No existing instance becomes formally incompatible with no action, and no existing instance needs to do anything differently to stay conformant — per `decisions/0023`'s operational test.

## Triggers fired

| Trigger | Triggered? | Note |
|---|---|---|
| `regra_normativa` | No | No new or changed rule in `SPEC.md` — both edits are pointer sentences to new reference documents, not new obligations. |
| `schema_frontmatter` | No | No frontmatter field added or changed. |
| `mecanismo_cross_repositorio` | No | Sections 6 and 13 unchanged in substance. |
| `politica_dados_sensiveis` | No | Section 2-A unchanged. |
| `release` | Reserved | Evaluated at the v2.0.0 release closing. |

Change Set required by the `operational` class itself (`docs/change-management.md`'s class table), independent of the trigger table above.

## Impact

See `impact.yaml`.

## Known, not addressed here

- **`docs/taxonomy.md`'s retroactive lineage.** Every cell marked `TBD — Lote E2` in the current document is deferred, on purpose, to a second Change Set — not silently incomplete. See `decisions/0047`'s Decision section for the full reasoning.
- **No mapping from Hipocampo's step-classification scheme onto MODA's own five-value agency vocabulary.** `docs/step-classification.md` explicitly declines to attempt this — see `decisions/0048`'s Discarded alternatives.
- **No automated staleness check for either document.** Both are manually maintained; a future mechanic, action, or field needs its own row/entry added explicitly, the same discipline every prior structural addition in this repository already follows (no tooling regenerates either document from `SPEC.md`).
