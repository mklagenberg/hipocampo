# Change Set — 0035: controlled-vocabulary dictionary

## Summary

Makes English the canonical vocabulary for every controlled-vocabulary field in `hipocampo` (`source`, `domain`, exposure `tier`, curation-level `tier`, `AGENTS.md`'s "Instance type"), while keeping every existing pt-BR value permanently valid via a new de:para reference, `docs/vocabulary-dictionary.md`. Extends the maintenance rituals (frontmatter audit, REM, structural audit) so a deprecated value is flagged and migrated opportunistically, the same way an expired `ttl` already is — never in bulk, never silently.

## Class

**normative** — changes the canonical values of several schema-level controlled-vocabulary fields and adds a new ritual behavior (deprecated-value detection and disposition) to sections 2-B, 5-A, 5-B, 5-C of `SPEC.md`. Not an editorial correction or an isolated routine operation.

## Semver

**minor** — additive and backward-compatible by explicit design: no existing instance's frontmatter, `AGENTS.md`, or `hipocampo.yaml` becomes invalid or requires any action. An instance that never touches these fields again stays fully conformant indefinitely with its current pt-BR values. Consistent with the rest of this release cycle's MODA-conformance work, accumulated toward v2.0.0.

## Triggers fired

| Trigger | Triggered? | Note |
|---|---|---|
| `regra_normativa` | Yes | `decisions/0035` is a new norm; changes canonical schema values. |
| `schema_frontmatter` | Yes | `source`'s enum values change (document frontmatter, `SPEC.md` section 2). |
| `mecanismo_cross_repositorio` | No | `registry.md`/`$alias:` are not affected. |
| `politica_dados_sensiveis` | No | Does not change the sensitive-data policy itself, only the vocabulary of the field that selects which variant applies. |
| `release` | Reserved | Evaluated at the v2.0.0 release closing, not in this isolated Change Set. |

## Impact

See `impact.yaml`.

## Status

`implemented` — the changes described here have already been executed, in a branch stacked on PR #27's `moda/fase-e-traducao-ingles`; this is not a future proposal.
