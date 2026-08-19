# Change Set — 0050: CI enforcement of repository structure, skill-doc consistency, and Change Set validation

## Summary

Adds `.github/workflows/validate.yml`, running three checks on every PR against `main` and on push to `main`: `scripts/validate_hipocampo.py` (existed since `decisions/0036`, but not actually wired into CI until now — a gap this Change Set closes); the new `scripts/validate_skill_docs.py` (checks `skill/**.md`'s `example/*.md` output-path literals against `scaffold/profiles/*.yaml`'s declared outputs, and flags any use of the superseded `domain:` field under `skill/`, `decisions/0041`); and the new `scripts/validate_change.py` (structural schema validation of every `changes/*/impact.yaml`, plus PR-mode diff-coverage checking that a protected path changed in a PR is named by an `updated` `impact[]` entry in a Change Set touched by the same diff). Also corrects `conformance/moda.yaml` and `docs/change-management.md`, both of which cited this CI workflow as existing evidence before it existed in this repository — found during a v2.0.0 personal-skill revalidation exercise, not by this Change Set's own tooling (which didn't exist yet to catch it).

## Class

**operational** — adds execution guidance/tooling (two new validation scripts, a CI workflow, a documentation correction) without changing any normative obligation on a content instance; nothing in `SPEC.md`'s frontmatter schema, invariants, or instance-facing rules changes as a result.

## Semver

**minor** — additive and internal to the `hipocampo` repository's own tooling; no existing content instance needs to take any action.

## Triggers fired

| Trigger | Triggered? | Note |
|---|---|---|
| `regra_normativa` | No | No `SPEC.md` obligation added, removed, or changed. |
| `schema_frontmatter` | No | Doesn't touch document frontmatter (`SPEC.md` section 2). |
| `mecanismo_cross_repositorio` | No | `registry.md`/`$alias:`/Promote/Depromote/Redbutton unaffected. |
| `politica_dados_sensiveis` | No | Section 2-A unaffected. |
| `release` | No | Not a release cut. |

Classified `operational` per `docs/change-management.md`'s class table — a Change Set is required regardless of which trigger row fires.

## Discarded alternatives

- **Enforcing `scripts/validate_change.py`'s full schema on every pre-existing `changes/*/impact.yaml`**, including ones that predate the schema converging on its current `change_set`/`impact`/`validation` shape (`decisions/0031` describes iterative adoption, not one atomic cutover — this was confirmed empirically: `changes/0026-0028-.../impact.yaml` uses an entirely different `{change, git, triggers, affected, validation}` shape, and `changes/0032-0033-.../impact.yaml`, `changes/0034-.../impact.yaml`, `changes/0035-.../impact.yaml` are each missing or violating parts of the current schema — see the CI run this Change Set fixes). Discarded: it would either fail CI permanently on already-accepted, historical Change Sets, or require editing them after acceptance — both violate `docs/change-management.md`'s explicit rule that "Accepted Change Sets remain as traceability evidence — never edited after acceptance, only superseded." Chose instead to grandfather the specific pre-existing directories (including the two pt-BR/EN redirect stubs) out of strict schema enforcement; full validation applies only to Change Sets created after this one.
- **Adding `scripts/` and `.github/` to `PROTECTED_PREFIXES`**, so this Change Set's own tooling files would themselves require diff-coverage. Discarded for this Change Set: `scripts/` and `.github/` are execution mechanics, not the contract surfaces (`SPEC.md`, `decisions/`, `skill/`, `scaffold/`, `docs/`, `moda.yaml`, the `CHANGELOG.md` family) the diff-coverage check exists to protect; broadening scope is a separate decision, not bundled here.

## Risks

- The diff-coverage check's path-token matching is heuristic (regex-based), not semantic — already documented in `scripts/validate_change.py`'s own docstring and in `docs/change-management.md`'s "Impact status" section.
- Grandfathering historical Change Sets means CI cannot catch a genuine schema violation if one of those specific files is edited again in a future PR — judged an acceptable, narrow gap given the alternative (rewriting accepted history).

## Acceptance criteria

- `python3 scripts/validate_change.py --root .` passes with 0 errors against the actual repository state (all existing Change Sets, grandfathered or not).
- `python3 scripts/validate_change.py --root . --base <pre-PR-#43 main> --head <PR #43 head>` passes with 0 errors — i.e. this Change Set itself covers every protected path (`conformance/moda.yaml`, `docs/change-management.md`) touched by PR #43's diff.
- CI (`.github/workflows/validate.yml`) runs and passes on PR #43.

## Compatibility / migration

None — internal repository tooling only, no content-instance-facing change.

## Recovery

If the grandfather list or diff-coverage heuristic proves too strict or too loose in practice, `scripts/validate_change.py` is edited in a follow-up Change Set; this one is marked `superseded`, never edited in place, per the same rule it documents.

## Impact

See `impact.yaml`.

## Status

`implemented` — already executed, in the same PR (#43) that introduces this Change Set.
