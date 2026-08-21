# Instructions for agents

Hipocampo is a public methodology repository. This file is the canonical agent entry point for whoever contributes **to the methodology itself** — distinct from the `AGENTS.md` that each content instance (vault) uses for itself, and that Hipocampo specifies for others (`SPEC.md`, section 11). If you got here trying to operate a vault (store knowledge, run a ritual), the right file is that content repository's `AGENTS.md`, not this one.

## Start with the map

## Route by user intent

Classify the request before loading documents. Read only the listed path, then expand only when the request requires it:

| User intent | Required route | Write boundary |
|---|---|---|
| Already operates Hipocampo | Target vault's `AGENTS.md` and `hipocampo.yaml`; relevant SPEC rule | Never infer a target vault or write permission. |
| New to Hipocampo | `README.md`, `GETTING-STARTED.md`, `DISCLAIMER.md`, and `docs/FUNDAMENTALS.md` | Orientation only until the user explicitly asks to instantiate. |
| Wants to know or install the methodology | `README.md`, `GETTING-STARTED.md`, `skill/SKILL.md`, and the relevant host adapter | Installation is client-side and always confirmed. |
| Wants to update the skill | `skill/manifest.yaml`, `skill/package-lock.yaml`, host adapter, `UPGRADE.md` | Compare version and package hash; notify and wait for confirmation. |
| Wants to update vaults | Each target vault's `AGENTS.md`/manifest, `UPGRADE.md`, `MIGRATIONS.md`, `CHANGELOG.md` | No repository-wide sweep; remediate progressively through CRUD or REM. |
| Wants focused methodology context | `README.md`, then only the relevant SPEC section and Decision Records | Read-only unless a separate change is requested. |
| Wants the complete methodology | `README.md`, `DISCLAIMER.md`, full `SPEC.md`, taxonomy, vocabulary, CHANGELOG, UPGRADE, conformance, and latest audit | State reading scope and limits. |

Load only the context needed for the current task:

1. Read `README.md` for the repository's identity and navigation.
2. Read `SPEC.md` for the complete normative specification.
3. Read `moda.yaml` for machine-readable identity and MODA conformance state.
4. Read the relevant Decision Record in `decisions/` before changing any existing rule.
5. Read `ROADMAP.md` when the change affects direction or introduces a new capability.
6. Read `CHANGELOG.md` and `UPGRADE.md` before changing already-released behavior.
7. Read `conformance/moda.yaml` and the latest audit in `audits/moda/` before changing structure that affects MODA conformance.

Don't turn this file into an encyclopedia. Detailed knowledge lives in the linked documents.

## MODA Disclosure

<!-- moda:disclosure:start -->
This repository is being structured and evaluated with [MODA](https://github.com/mklagenberg/moda) — an open framework for organizing, designing, auditing, packaging, and evolving agentic methodologies.

Before changing the methodology's structure, read `moda.yaml`, `conformance/moda.yaml`, and the latest audit in `audits/moda/`. Do not claim conformance beyond the evidence produced against the declared MODA version — today the declared relationship is `conforms_to` (retrospective, `claim_stage: mapped`, `conformance_result: partial`), not full conformance. Do not migrate structure silently.
<!-- moda:disclosure:end -->

## Working rules

- Write all content contributed to this repository (`SPEC.md`, `decisions/`, `docs/`, `skill/`, `scaffold/`) in English — see `decisions/0034-repository-and-vault-language-policy.md`. This does not apply to a vault (a content repository generated from this methodology): a vault's own working language is declared in that vault's `hipocampo.yaml`, independent of this repository's language.
- Preserve the distinction between methodology, framework, method, process, procedure, workflow, standard, prompt, skill, toolkit, and implementation (MODA SPEC, section 3) — `SPEC.md` itself already uses these distinctions consistently, even without MODA's explicit RFC 2119 keywords.
- Treat the repository as a system of record. Do not treat an unrecorded conversation as the sole source of durable intent — a structural decision always becomes a Decision Record.
- Point to evidence; do not copy normative rules into a conformance mapping or audit report.
- Prefer deterministic validation when it exists — for this repository's own structural integrity (Decision Record template, internal links, README/CHANGELOG version consistency), run `python3 scripts/validate_hipocampo.py --root .` (also enforced in CI on every PR, `.github/workflows/validate.yml`, `decisions/0036-deterministic-validation-of-repository-structure.md`). This does not cover everything: whether a Change Set's declared impact matches its actual diff, and the methodology's own quality/evaluation dimension, remain human review — see `docs/change-management.md` and `ROADMAP.md`.
- Require human direction for unresolved intent, risk acceptance, destructive action, external side effect, security boundary, and incompatible migration — same principle as invariant 5 of `SPEC.md` (section 8), applied here to the methodology itself, not only to the instances it specifies.
- Never report a source, test, link, or audit as checked when it wasn't actually checked.

## Change protocol

- Classify the work as editorial, operational, or normative before implementing (MODA vocabulary). The formal Change Set mechanism (`changes/<id>/proposal.md` + `impact.yaml`) has existed since Phase C (`docs/change-management.md`, `decisions/0031-change-set-mechanism.md`) and is **mandatory** for `operational`/`normative` change from that point on: a new Change Set in `changes/<id>/`, accompanying the Decision Record (when it involves a structural choice) and the corresponding sections of `SPEC.md`/`CHANGELOG.md`, all updated in the same PR. `editorial` change doesn't require a Change Set.
- Change the normative specification (`SPEC.md`) first when the obligation changes.
- Use a short-lived branch and PR for normal change; keep `main` as the only permanent integration branch.
- Update `CHANGELOG.md` for a notable behavior or contract change.
- Record a durable structural choice in `decisions/`.
- Before accepting a new named term or controlled value, update the taxonomy and vocabulary surfaces in the same Change Set, or record why neither applies.
- Update `ROADMAP.md` when direction changes; never use it as a task backlog or changelog.
- Update `UPGRADE.md` for adoption action required by a backward-compatible release.
- Update `MIGRATIONS.md` for an incompatible change.
- When operating only via MCP, without the ability to create a tag/release, give the human the exact tag, target branch, commit, title, description derived from the changelog, and release classification for creation after approval — never claim the tag or release exists. See `SPEC.md`, section 9, and `decisions/0014-mandatory-release-routine.md`.
- Before considering a release routine complete, go through `RELEASE-CHECKLIST.md` — it operationalizes `decisions/0014`/`0021`/`0023` into a single concrete run-through (`decisions/0037-minimal-release-gate-checklist.md`).

## Versioning

Hipocampo follows [SemVer](https://semver.org/lang/pt-BR/) — full operational criterion in `SPEC.md`, section 9, and `decisions/0023-operational-criterion-for-semver-scope.md`.

## Conclusion

A change is only complete when:

- the intent and scope are explicit;
- the relevant Decision Record (when applicable), the Change Set (when `operational`/`normative`), and the corresponding sections of `SPEC.md`/`CHANGELOG.md` are synchronized in the same PR;
- no known critical finding is left hidden;
- affected documentation and generated disclosures are synchronized;
- no MODA conformance claim goes beyond what the evidence in `conformance/moda.yaml` supports.
