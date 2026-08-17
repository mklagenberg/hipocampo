# Specification-driven change management

Hipocampo treats a structural change to the repository as a change to a system of contracts, not just a collection of files. `SPEC.md` is the authoritative normative specification; `decisions/`, `CHANGELOG.md`, `UPGRADE.md`, `MIGRATIONS.md`, `moda.yaml`/`conformance/moda.yaml`, and the personal copy of the skill are synchronized projections of that contract. Mechanism adopted following the [MODA](https://github.com/mklagenberg/moda) model (their `docs/change-management.md`) — see `decisions/0031-change-set-mechanism.md` for the full rationale behind the adoption.

## Change classes

| Class | Meaning | Requires a Change Set? |
|---|---|---|
| `editorial` | Wording, formatting, or a link, with no semantic, operational, structural, security, or compatibility effect | Optional, unless it changes a protected contract surface |
| `operational` | Changes execution guidance, a routine, packaging, or the skill, without changing a normative obligation | Required |
| `normative` | Adds, removes, or changes an obligation, public contract, compatibility boundary, or meaning of conformance | Required |

The names of the three classes stay in English, even with the rest of the repository in Portuguese — `editorial` in Portuguese carries a connotation of opinion/judgment that the original term doesn't have (here it means wording/formatting); keeping the technical term avoids that noise (this will be revisited when the repository's Phase E translation happens).

An apparently editorial change is operational or normative when it changes how a human or agent acts, how an instance validates something, or what an instance needs to implement to remain conformant.

## Hipocampo Change Set

A change that requires a Change Set lives at `changes/<change-id>/` and contains:

- `proposal.md` — problem, current contract, proposed contract, discarded alternatives, risks, acceptance criteria, compatibility/migration, recovery;
- `impact.yaml` — machine-readable classification, SemVer impact, triggers, affected surfaces, validation.

The proposal captures the reasoning behind *this specific* change. A durable structural choice is also recorded in `decisions/` — a Change Set doesn't replace a Decision Record; they answer different questions (the same scope distinction already in use between a Decision Record and `type: decision`, `SPEC.md` section 7, just applied here between Change Set and Decision Record). Accepted Change Sets remain as traceability evidence — never edited after acceptance, only superseded.

## Impact status

Every surface declared in `impact.yaml` is classified as:

- `updated` — one or more declared paths changed;
- `reviewed` — reviewed and intentionally left unchanged, with rationale;
- `not-applicable` — out of scope for the change, with rationale.

The declaration isn't proof by itself — human review assesses whether the rationale is credible. No deterministic validation compares this against the actual diff yet (see the section below).

## Change flow

1. Classify the change before implementing it.
2. Create a Change Set for an operational or normative change.
3. Declare the intended contract and acceptance criteria in `proposal.md`.
4. Declare triggers, SemVer impact, affected surfaces, and expected validation in `impact.yaml`.
5. Change the authoritative source first: `SPEC.md` for a normative rule, or the operational artifact that owns the behavior for an operational change.
6. Synchronize the affected projections without copying normative prose into each file.
7. Run the declared validation: `scripts/validate_hipocampo.py` for the repository's own structural integrity (automatic in CI on the PR), plus human review for everything the script doesn't cover (see "Deterministic and human checking" below).
8. Review the diff, any unresolved gaps, migration/recovery needs, and MODA conformance impact.
9. Merge only after explicit human review (Mau).
10. Cut a tag only through the release routine (`SPEC.md`, section 9).

## Triggers

Adapted to Hipocampo's actual vocabulary — not a literal translation of MODA's table, because some of their concepts (`package_contract`, for example) have no equivalent in this repository today.

| Trigger | Minimum surfaces to review |
|---|---|
| `regra_normativa` — a rule change in `SPEC.md` | `SPEC.md`, `decisions/`, `CHANGELOG.md`, `UPGRADE.md`/`MIGRATIONS.md` depending on SemVer scope (`decisions/0023`) |
| `schema_frontmatter` — a new/changed field in the schema (section 2) | `SPEC.md` section 2, `UPGRADE.md`, examples cited in `GETTING-STARTED.md`/`BEST-PRACTICES.md` |
| `mecanismo_cross_repositorio` — Promote/Depromote/Redbutton/Registry (sections 6/13) | `SPEC.md` sections 6/13, `decisions/`, `CHANGELOG.md` |
| `politica_dados_sensiveis` — section 2-A | `SPEC.md` section 2-A, `decisions/`, `BEST-PRACTICES.md` |
| `release` — version cut | `CHANGELOG.md`, `UPGRADE.md`, `MIGRATIONS.md` (if MAJOR), `moda.yaml` (declared version), `conformance/moda.yaml` |

`reviewed` and `not-applicable` are only valid with concrete rationale. A structural choice also requires a Decision Record.

## Deterministic and human checking

Structural integrity of the methodology repository itself — Decision Record template compliance, internal link resolution, README/CHANGELOG version consistency — is now checked deterministically by `scripts/validate_hipocampo.py`, run in CI on every pull request against `main` (`.github/workflows/validate.yml`, `decisions/0036-deterministic-validation-of-repository-structure.md`), closing the corresponding `major` finding from the 2026-08-17 MODA audit. That check does not reach a Change Set's *semantic* completeness, though — the following remain human review:

- whether the declared classification and SemVer impact are true;
- whether a rule change has been fully projected into the operational guidance (personal skill, instance `AGENTS.md`, etc.);
- whether the `reviewed`/`not-applicable` rationales are credible;
- whether migration and release risks are acceptable.

## Completion rule

A change is incomplete when its implementation looks ready but the declared contract surfaces, evidence, or migration obligation are inconsistent with each other. There's no automated check yet that proves this on its own — human review remains responsible for semantic completeness.
