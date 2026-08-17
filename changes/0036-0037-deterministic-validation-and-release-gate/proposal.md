# Change Set — 0036–0037: deterministic validation and release-gate checklist

## Summary

Adds `scripts/validate_hipocampo.py` (Decision Record template compliance, internal link resolution, README↔CHANGELOG version consistency, and a non-blocking schema-field-to-DR coverage report) plus `.github/workflows/validate.yml` running it in CI on every PR against `main` (`decisions/0036`); adds `RELEASE-CHECKLIST.md`, a minimal checklist expanding `decisions/0014`/`0021`/`0023` into a single concrete run-through executed at release-cut time (`decisions/0037`). Together, closes MODA self-audit major finding 4 and minor finding 2 (`audits/moda/2026-08-17-v1.0.0-self-audit.md`, "Onda 3" and "Onda 6").

## Class

**operational** — both changes add execution guidance/tooling (a validation script, a CI workflow, a release checklist) without changing a normative obligation on any content instance; nothing in `SPEC.md`'s frontmatter schema, invariants, or instance-facing rules changes as a result of this Change Set.

## Semver

**minor** (consistent with the rest of the MODA-conformance work in this cycle, accumulated toward v2.0.0 at release time — same logic as `decisions/0031`/`0034`/`0035`). Additive and internal to the `hipocampo` repository itself: no existing content instance needs to take any action, and nothing about instance conformance changes.

## Triggers fired

| Trigger | Triggered? | Note |
|---|---|---|
| `regra_normativa` | No | Neither change adds/removes/changes an obligation in `SPEC.md`. |
| `schema_frontmatter` | No | Does not touch the document frontmatter schema (`SPEC.md` section 2). |
| `mecanismo_cross_repositorio` | No | `registry.md`/`$alias:`/Promote/Depromote/Redbutton unaffected. |
| `politica_dados_sensiveis` | No | Section 2-A unaffected. |
| `release` | Reserved | Evaluated at the v2.0.0 release closing, not in this isolated Change Set. |

Classified as `operational` per the class table in `docs/change-management.md` ("Changes execution guidance, a routine, packaging, or the skill, without changing a normative obligation") — a Change Set is required for `operational`/`normative` changes regardless of which row of the trigger table fires.

## Impact

See `impact.yaml`.

## Status

`implemented` — the changes described here have already been executed, in the same PR that introduces this Change Set (Fase G).
