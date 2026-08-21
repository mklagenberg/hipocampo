# Change Set — 0054: Clarify third-party anonymization scope

## Summary

Corrects `decisions/0050` so its standing anonymization rule consistently governs real, identifiable third parties. The previous wording prohibited every named individual while the Decision Record itself uses necessary provenance references to the repository's own operator. The corrected wording preserves the unconditional protection for third parties and permits only the repository operator's necessary provenance references, never third-party disclosure.

## Class

**operational** — repairs an internal methodology policy's scope without changing any content-instance contract, schema, or required behavior outside this repository.

## SemVer

**patch** — corrective repository guidance; no existing instance needs migration or action.

## Triggers fired

| Trigger | Triggered? | Note |
|---|---|---|
| `regra_normativa` | No | `SPEC.md` is unchanged; this corrects an internal Decision Record's scope. |
| `schema_frontmatter` | No | No schema field changes. |
| `mecanismo_cross_repositorio` | No | No discovery or cross-repository mechanism changes. |
| `politica_dados_sensiveis` | No (adjacent) | The correction concerns identifiable citations in the methodology repository, not a content instance's sensitive-data policy. |
| `release` | No | No release cut occurs in this Change Set. |

## Risks

The exception must remain narrow: it permits only provenance references to the repository's own operator and never restores a third-party entity, person, or personal handle.

## Acceptance criteria

- `decisions/0050` explicitly restricts the anonymization rule to real, identifiable third parties.
- The decision preserves the unconditional rule for third-party citations and states the narrow provenance boundary.
- Repository and Change Set validators pass with zero errors.

## Compatibility / migration

None — no content instance action is required.

## Recovery

If a later clarification shows this scope is still ambiguous, supersede this Change Set with a new scoped correction; do not weaken the third-party protection by silent interpretation.

## Status

`implemented`.
