# Change Set — 0034: repository and vault language policy

## Summary

Codifies, as an ongoing rule (not just the one-time Fase E migration), that `hipocampo` is maintained in English going forward; introduces a new `instance.language` field in the per-vault `hipocampo.yaml` manifest so a vault's own content language is declared independently of `hipocampo`'s language, defaulting to `"en"` for a newly scaffolded vault.

## Class

**normative** — introduces a new manifest field (schema change to `hipocampo.yaml`, extending `decisions/0033`) and a binding contribution rule for this repository going forward; not an editorial correction or an isolated routine operation.

## Semver

**minor** (consistent with the rest of the MODA-conformance work in this cycle — accumulated toward v2.0.0 at the end, not decided phase by phase; same logic as `decisions/0031`). Additive: no existing declared vault becomes formally incompatible — none of the 4 real vaults has adopted `hipocampo.yaml` yet (already a pending item since `decisions/0033`), so this only adds one more field to that same pending step.

## Triggers fired

| Trigger | Triggered? | Note |
|---|---|---|
| `regra_normativa` | Yes | `decisions/0034` is a new norm. |
| `schema_frontmatter` | No | Does not change the document frontmatter schema (`SPEC.md` section 2) — only the vault manifest (`hipocampo.yaml`), which is a separate schema. |
| `mecanismo_cross_repositorio` | No | `registry.md`/`$alias:` are not affected. |
| `politica_dados_sensiveis` | No | Does not change the sensitive-data policy or its variant by instance type. |
| `release` | Reserved | Evaluated at the v2.0.0 release closing, not in this isolated Change Set. |

## Impact

See `impact.yaml`.

## Status

`implemented` — the changes described here have already been executed, in the same branch/PR as Fase E (PR #27); this is not a future proposal.
