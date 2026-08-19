# Change Set — 0047, retroactive backfill: taxonomy map lineage (Lote E2)

## Summary

Fills in every `TBD — Lote E2` cell in `docs/taxonomy.md`, the taxonomy map delivered structurally in Lote E1 (`decisions/0047`, Change Set `changes/0047-0048-taxonomy-map-and-step-classification/`). This is the retroactive-lineage half of that DR's own two-lote split, explicitly deferred at the time: walking `CHANGELOG.md` from `[1.0.0]` forward, cross-referencing `decisions/`, and citing which tagged release (`v1.0.0`–`v1.9.0`) or which point in the still-unreleased `[Unreleased]` section introduced or last changed each field, enum, or named concept.

No new Decision Record accompanies this Change Set — `decisions/0047` already made the durable structural choice (the document exists, is split into two lotes, and doesn't follow `decisions/0031`'s single-sample backfill precedent). This Change Set executes exactly what that DR already decided; it makes no new structural choice of its own.

## Class

**operational** — completes reference/index content (where to look, and since when) without changing any normative obligation. No `SPEC.md` edit in this Change Set — Lote E1 already added the two pointer sentences; the lineage backfill lives entirely inside `docs/taxonomy.md`. Still `Required` per `docs/change-management.md`'s class table.

## Semver

**minor** — purely additive, and non-normative: filling in citation columns in a reference document. No existing instance becomes formally incompatible with no action, per `decisions/0023`'s operational test. (Not `patch` — `decisions/0021` reserves `patch`/hotfix for genuine urgency; this is scheduled, planned completion work, not a fix.)

## Triggers fired

| Trigger | Triggered? | Note |
|---|---|---|
| `regra_normativa` | No | No `SPEC.md` edit in this Change Set. |
| `schema_frontmatter` | No | No frontmatter field added or changed. |
| `mecanismo_cross_repositorio` | No | Sections 6 and 13 unchanged in substance. |
| `politica_dados_sensiveis` | No | Section 2-A unchanged. |
| `release` | Reserved | Evaluated at the v2.0.0 release closing. |

Change Set required by the `operational` class itself, independent of the trigger table above.

## Impact

See `impact.yaml`.

## Known, not addressed here

- **Precision limits inherited from the source material.** Two rows (`entity`/`domain`, and `AGENTS.md`'s "Instance type") don't trace to a single exclusively-dedicated Decision Record — `docs/taxonomy.md`'s "Status of this document" section states this explicitly rather than collapsing it into a false-precision single date.
- **No real version number for anything cited as "Unreleased."** The entire back half of the Decision Record range (`decisions/0015`–`0048`) has never shipped in a tagged release. This Change Set does not resolve that — it only makes the citation honest about which bucket ("Unreleased") each item is in, same as Lote E1 already did for the four just-completed lotes.
- **No automated staleness check.** Same limitation already flagged for `docs/taxonomy.md` and `docs/step-classification.md` in Lote E1 — both remain manually maintained.
