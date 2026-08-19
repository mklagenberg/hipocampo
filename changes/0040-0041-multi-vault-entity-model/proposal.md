# Change Set — 0040–0041: multi-vault/multi-entity design premises and the entity model

## Summary

Adds `SPEC.md` section 2-D, "Multi-vault and multi-entity design premises" — three explicit premises (multi-vault/multi-entity by design, confidential-first always, the anchor as an existence guarantee rather than a universal funnel) plus their direct consequences (short-term memory per-vault, a fallback-with-tag mechanism for a known-but-unreachable destination, personal-vault bootstrap as a prerequisite) — closing a real design bug (an earlier hub-spoke discovery proposal that assumed reciprocal access no participant is actually guaranteed) found while reviewing the taxonomy for v2.0.0 (`decisions/0040`).

Rewrites `SPEC.md` section 2-C, replacing `domain` (`personal`/`company`, a fixed two-value enum) with **entity** — an extensible identifier for the person, organization, or relationship a vault belongs to — and formalizes that every entity has exactly one mandatory anchor vault plus any number of additional vaults, each self-declaring `entity`/`role`/`scope_description` in its own manifest, with no vault listing its siblings. Redefines "vault" as a generic noun for any knowledge repository (previously implied confidential-only) (`decisions/0041`).

Extends the `hipocampo.yaml` manifest schema (`decisions/0033`) accordingly: `instance.domain` is replaced by `instance.entity`, `instance.role`, and `instance.scope_description`. Updates the scaffold skeleton and both profiles (`scaffold/skeleton/hipocampo.yaml`, `scaffold/profiles/pessoal.yaml`, `scaffold/profiles/empresa.yaml`) to collect and generate the new fields. Recommends `AGENTS.md`'s "Instance type" field for retirement, now that `entity`+`role` derive the same information — a reversal of `decisions/0033`'s original "deliberately not harmonized" position, since the condition that made harmonization out of scope there (a schema not yet expressive enough) no longer holds.

Both Decision Records are combined into one Change Set because they are one cohesive taxonomy revision — `decisions/0041` is a direct application of the premises `decisions/0040` establishes, the same relationship already used to combine `changes/0026-0028-.../` and `changes/0032-0033-.../`.

This is Lote A of the taxonomy revision sequencing established in this cycle — the first and most structural of five lotes toward v2.0.0; every subsequent lote depends on the entity/vault vocabulary landing here first.

## Class

**normative** — replaces a schema field (`instance.domain` → `instance.entity`/`instance.role`/`instance.scope_description`) and adds new design premises with concrete behavioral consequences (the fallback-with-tag mechanism, the personal-bootstrap-first ordering) that govern agent conduct.

## Semver

**major** — an existing instance's `hipocampo.yaml`, if it declares `instance.domain`, no longer satisfies the current schema with no action; per `decisions/0023`'s operational test, this is MAJOR, not MINOR. See `MIGRATIONS.md`, "1.x → 2.0".

## Triggers fired

| Trigger | Triggered? | Note |
|---|---|---|
| `regra_normativa` | Yes | `SPEC.md` sections 2-C (rewritten) and 2-D (new) are normative rules. |
| `schema_frontmatter` | Yes | `hipocampo.yaml`'s `instance` block changes: `domain` removed, `entity`/`role`/`scope_description` added. This is the vault manifest, not document frontmatter proper (`SPEC.md` section 2) — triggered because the schema-field discipline (declare in `SPEC.md`, update `UPGRADE.md`, cite in examples) applies the same way. |
| `mecanismo_cross_repositorio` | No | Sections 6/13 (Registry, Promote/Depromote/Redbutton) are unchanged by this Change Set — the discovery procedure that reads `entity`/`role` at runtime is deferred to a later lote. |
| `politica_dados_sensiveis` | No | Section 2-A is unchanged. |
| `release` | Reserved | Evaluated at the v2.0.0 release closing, not in this isolated Change Set. |

## Impact

See `impact.yaml`.

## Status

`implemented` — the changes described here have already been executed, in the same PR that introduces this Change Set (Lote A).
