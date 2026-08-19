# 0047 — Taxonomy map (`docs/taxonomy.md`), structure first

**Status:** Accepted

## Context

The v2.0.0 taxonomy revision (Lotes A through D, `decisions/0040`–`0046`) changed a substantial part of this methodology's schema and vocabulary — `domain` superseded by `entity`/`role`, a new Dispatcher/Routine/Mechanic/Action taxonomy, vault discovery replacing a hand-filled router, a sixth invariant. Each change is documented where it lives (a `SPEC.md` section, a Decision Record, a `CHANGELOG.md` entry), correctly per this repository's own change-management discipline (`docs/change-management.md`). But no single document answers "what does the taxonomy look like today, as a whole, and how did it get here" — an operator or auditor has to reconstruct that by reading every relevant Decision Record and cross-referencing `CHANGELOG.md` by hand. This is exactly the kind of confusion that motivated the taxonomy revision in the first place, and most of that confusion traces to decisions older than v1.9.0, not only to the four lotes just completed.

`docs/vocabulary-dictionary.md` (`decisions/0035`) already solves an adjacent, narrower problem — pt-BR/English value equivalence for controlled-vocabulary fields — and includes its own "Change history" section. It does not cover non-vocabulary structural concepts (the Dispatcher/Routine/Mechanic/Action taxonomy has no pt-BR/English pair to track, for example), and its lineage tracking is scoped only to the fields it already covers.

## Decision

Create `docs/taxonomy.md`: a single index of every controlled field, enum, and named concept the methodology defines, with a pointer to its authoritative source (`SPEC.md` section and/or Decision Record) and — where already known — the version it was introduced or last changed in.

**Split into two lotes, not delivered at once.** This lote (E1) establishes the document's structure and populates every row's current state completely, plus the version lineage for everything that changed during the v2.0.0 taxonomy revision itself (already known at time of writing — no separate research needed). Everything predating `v1.9.0` is marked `TBD — Lote E2`, explicitly, rather than guessed at or silently left incomplete-looking-complete. Lote E2 does the actual archaeology: walking `CHANGELOG.md` from `[1.0.0]` forward to fill in every `TBD` cell.

**Why this doesn't follow `decisions/0031`'s backfill-in-one-PR precedent.** That precedent (applied to the Change Set mechanism's own backfill, PR #22) limited retroactive work to a single representative sample, because the goal was validating a template — one sample was sufficient evidence the template worked. Here, the document's entire value proposition is completeness: a taxonomy map that only covers "from here forward" resolves half the problem this DR exists to address and leaves the other half — the confusion rooted in pre-v1.9.0 decisions — exactly as unresolved as before. Proportionality still applies, but it points the other way: splitting structure from backfill lets the structure ship now, reviewable and immediately useful for the just-completed Lotes A–D, without blocking on the larger research task or silently shipping a document that looks complete but isn't.

**Distinct from `docs/vocabulary-dictionary.md`.** `docs/taxonomy.md` is broader (every structural concept, not only controlled-vocabulary fields) and orthogonal (a version-introduced/version-changed lineage, not a pt-BR/English pair). Where a field already has a vocabulary-dictionary entry, `docs/taxonomy.md` points at it instead of repeating it.

## Rationale

Sequencing this last, after Lotes A–D, follows the planning discussion's own reasoning: the taxonomy map's value depends on documenting the *result* of the revision, including everything Lotes A–D just changed — building it earlier would mean rewriting it as soon as each lote landed. Splitting structure from backfill follows the same "no silent caps" discipline already used elsewhere in this repository (Fase G's validator coverage report, this session's own Lote-by-lote PR bodies) — an incomplete document is fine as a first step, an incomplete document presented as finished is not.

## Discarded alternatives

- **Deliver the full document, backfill included, in one lote.** Discarded — the backfill is a large, separate research effort (reconstructing lineage across ten prior releases), and bundling it with the structural decision this DR actually makes would either delay the structure indefinitely or produce a rushed, unreliable backfill. Splitting lets each half be reviewed on its own terms.
- **Skip the backfill entirely, ship only current-state.** Discarded — explicitly rejected in the planning discussion: a map that only starts from here forward would resolve only half the confusion this document exists to address, since most of the original confusion traces to decisions older than v1.9.0.
- **Fold this into `docs/vocabulary-dictionary.md` instead of a separate document.** Discarded — that document is deliberately scoped narrowly to pt-BR/English value pairs (see its own "Scope — what this dictionary does *not* cover" section); most of what `docs/taxonomy.md` needs to index (behavioral taxonomy, cross-repository actions) has no such pair and would strain that document's existing scope discipline.
