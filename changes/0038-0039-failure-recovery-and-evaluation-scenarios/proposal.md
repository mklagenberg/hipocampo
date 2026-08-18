# Change Set — 0038–0039: failure/recovery behavior and minimal evaluation scenarios

## Summary

Adds `SPEC.md` section 14, defining required agent behavior under six failure modes (insufficient evidence, frontmatter↔body contradiction, unavailable tool, interruption mid-ritual, unsafe request, incompatible migration) — closes MODA self-audit major finding 6 (`decisions/0038`). Adds `docs/evaluation-scenarios.md`, four minimal representative scenarios (one real documented failure, three edge/correct-path cases) an operator or auditor can walk through — closes MODA self-audit major finding 7 (`decisions/0039`). Both close Onda 4 of the audit's own action plan (`audits/moda/2026-08-17-v1.0.0-self-audit.md`), combined into one Change Set for the same reason `changes/0032-0033-.../` and `changes/0036-0037-.../` were combined: tightly coupled work closing one audit wave.

Also adds `GETTING-STARTED.md` section 7, "Typical use cases" (three narrative walk-throughs of ordinary, correct-path use) — editorial, developed alongside the two normative changes above as the companion "what going right looks like" to `docs/evaluation-scenarios.md`'s "what going wrong looks like," but not itself a new obligation.

Also fixes six pre-existing Decision Records (`decisions/0026`–`0031`) whose `**Status:**` line read `Proposed` despite being fully merged, referenced normatively throughout `SPEC.md`, and treated as accepted everywhere else in the repository — a leftover from before they were merged, never updated. Found while reviewing the mechanism (`decisions/0031`, the Change Set mechanism itself) this Change Set uses. Corrected to `Accepted`, the value every other Decision Record in the repository uses. Same category of finding-fixed-transparently as the `decisions/0034`/`0035` title-template defect from Fase G (`changes/0036-0037-.../`) — not swept under the rug.

## Class

**normative** — `SPEC.md` section 14 adds real obligations on agent behavior (what an agent does/doesn't do under each failure mode); a Decision Record's `Status` field is metadata about the repository's own decision record, not content instances, but a Change Set is required once any part of the combined change is normative.

## Semver

**minor** — new guidance and a new reference document, both additive; no existing content instance becomes incompatible, and nothing about instance-side conformance is required to change as a result. Consistent with the rest of the MODA-conformance work accumulated toward v2.0.0 this cycle.

## Triggers fired

| Trigger | Triggered? | Note |
|---|---|---|
| `regra_normativa` | Yes | `SPEC.md` section 14 is a new normative rule governing agent behavior under failure. |
| `schema_frontmatter` | No | No frontmatter field added, removed, or changed. |
| `mecanismo_cross_repositorio` | No | Scenario 4 (`docs/evaluation-scenarios.md`) illustrates Promote; it does not change sections 6/13. |
| `politica_dados_sensiveis` | No | Scenario 3 illustrates section 2-A; it does not change the policy itself. |
| `release` | Reserved | Evaluated at the v2.0.0 release closing, not in this isolated Change Set. |

## Impact

See `impact.yaml`.

## Status

`implemented` — the changes described here have already been executed, in the same PR that introduces this Change Set (Fase H).
