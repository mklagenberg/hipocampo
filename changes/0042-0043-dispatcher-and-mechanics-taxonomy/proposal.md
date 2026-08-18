# Change Set — 0042–0043: Dispatcher and the four-layer taxonomy

## Summary

Adds `SPEC.md` section 5-D, "Dispatcher and the four-layer taxonomy: Routine, Mechanic, Action." Introduces the **Dispatcher** as a top-level scheduling concept, decoupled from REM — REM's own scope is unchanged (Consolidate + Update old memories, section 5-A); frontmatter audit and the weekly structural audit become sibling routines triggered by the Dispatcher rather than implicitly folded into REM's name (`decisions/0042`).

Formalizes a four-layer taxonomy — Dispatcher → Routine → Mechanic → Action — naming categories that already operate normatively without a shared vocabulary: REM/frontmatter audit/weekly structural audit as **routines**; CRUD (already informally called "mechanics" in section 2-B) as the **CRUD mechanic**; Promote/Depromote as the new **publication mechanic**; Redbutton as the new **sequenced-removal mechanic** — corrected from an earlier working name, "sequenced deletion," which would have contradicted invariant 3 (`SPEC.md` section 8, never physically delete). This taxonomy is orthogonal to the existing step-classification scheme (deterministic/discretionary/gated) — it classifies what kind of thing a piece of behavior is, not how it behaves (`decisions/0043`).

No action's actual behavior changes — Promote, Depromote, Redbutton, and CRUD's four operations work exactly as already specified in sections 2-B and 13. This Change Set only adds shared vocabulary above them.

Both Decision Records are combined into one Change Set for the same reason `changes/0026-0028-.../`, `changes/0032-0033-.../`, and `changes/0040-0041-.../` were combined: `decisions/0043`'s taxonomy directly depends on `decisions/0042`'s Dispatcher/routine split.

This is Lote B of the taxonomy revision sequencing established alongside Lote A (`changes/0040-0041-multi-vault-entity-model/`, a separate PR). Built independently from `main`, not stacked on Lote A's branch — neither PR's diff references the other's new vocabulary (`entity`/`role` vs. Dispatcher/Routine/Mechanic/Action are disjoint concepts), so the two can merge in either order.

## Class

**normative** — introduces the Dispatcher concept and a taxonomy that formally categorizes existing normative mechanisms (CRUD, Promote, Depromote, Redbutton), and corrects a naming defect (Redbutton's governing mechanic) that would otherwise have contradicted invariant 3.

## Semver

**minor** — purely additive vocabulary and one new `SPEC.md` section; every existing instance stays valid with no action (REM's behavior, CRUD's behavior, and Promote/Depromote/Redbutton's behavior are all unchanged). Per `decisions/0023`'s operational test, this is MINOR, not MAJOR.

## Triggers fired

| Trigger | Triggered? | Note |
|---|---|---|
| `regra_normativa` | Yes | `SPEC.md` section 5-D is new normative vocabulary; sections 2-B and 13 gain cross-reference sentences. |
| `schema_frontmatter` | No | No frontmatter field added, removed, or changed. |
| `mecanismo_cross_repositorio` | Yes | `SPEC.md` section 13's intro paragraph is edited (naming the mechanics governing Promote/Depromote/Redbutton) — no behavior change, but the trigger's own table names section 13 as a minimum surface to review whenever it's touched. |
| `politica_dados_sensiveis` | No | Section 2-A is unchanged. |
| `release` | Reserved | Evaluated at the v2.0.0 release closing, not in this isolated Change Set. |

## Impact

See `impact.yaml`.

## Status

`implemented` — the changes described here have already been executed, in the same PR that introduces this Change Set (Lote B).
