# Change Set — 0032/0033: consolidated scaffolding and per-vault hipocampo.yaml manifest

## Summary

Consolidates the vault-instantiation mechanism (previously `hipocampo-toolkit`, a separate GitHub repository) inside `hipocampo/scaffold/`, as a MODA-conformant declarative scaffold; introduces the `hipocampo.yaml` manifest, which every generated vault now carries.

## Class

**normative** — introduces a new normative artifact (the `hipocampo.yaml` schema, `decisions/0033`) and a mechanism change that affects how every future vault is created (`decisions/0032`); it is not merely an editorial correction nor an isolated routine operation.

## Semver

**minor** (consistent with the rest of the MODA-conformance work in this phase — the jump to MAJOR/2.0.0 is accumulated at the end of all phases, not decided phase by phase; same logic as `decisions/0031`).

## Triggers fired

| Trigger | Triggered? | Note |
|---|---|---|
| `regra_normativa` | Yes | `decisions/0032` and `decisions/0033` are new norms. |
| `schema_frontmatter` | No | Does not change the document frontmatter schema — it only introduces a repository manifest, outside the scope of frontmatter. |
| `mecanismo_cross_repositorio` | No | `registry.md`/`$alias:` are not affected. |
| `politica_dados_sensiveis` | No | Does not change the sensitive-data policy or its variant by instance type. |
| `release` | Reserved | Evaluated at the v2.0.0 release closing, not in this isolated Change Set. |

## Impact

See `impact.yaml`.

## Status

`implemented` — the changes described here have already been executed in this same PR (Phase D); this is not a future proposal.