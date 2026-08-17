# Instructions for agents

Hipocampo is a public methodology repository. This file is the canonical agent entry point for whoever contributes **to the methodology itself** — distinct from the `AGENTS.md` that each content instance (vault) uses for itself, and that Hipocampo specifies for others (`SPEC.md`, section 11). If you got here trying to operate a vault (store knowledge, run a ritual), the right file is that content repository's `AGENTS.md`, not this one.

## Start with the map

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

Before changing the methodology's structure, read `moda.yaml`, `conformance/moda.yaml`, and the latest audit in `audits/moda/`. Do not claim conformance without evidence produced against the declared MODA version — today the declared relationship is `audited_against` (retrospective, `claim_stage: mapped`, `conformance_result: partial`), not `conforms_to`. Do not migrate structure silently.
<!-- moda:disclosure:end -->

## Working rules

- Preserve the distinction between methodology, framework, method, process, procedure, workflow, standard, prompt, skill, toolkit, and implementation (MODA SPEC, section 3) — `SPEC.md` itself already uses these distinctions consistently, even without MODA's explicit RFC 2119 keywords.
- Treat the repository as a system of record. Do not treat an unrecorded conversation as the sole source of durable intent — a structural decision always becomes a Decision Record.
- Point to evidence; do not copy normative rules into a conformance mapping or audit report.
- Prefer deterministic validation when it exists — today none exists for the methodology repository itself (`major` finding from the 2026-08-17 audit, `audits/moda/`); until this is resolved (see `ROADMAP.md`), every structural change depends on explicit human review.
- Require human direction for unresolved intent, risk acceptance, destructive action, external side effect, security boundary, and incompatible migration — same principle as invariant 5 of `SPEC.md` (section 8), applied here to the methodology itself, not only to the instances it specifies.
- Never report a source, test, link, or audit as checked when it wasn't actually checked.

## Change protocol

- Classify the work as editorial, operational, or normative before implementing (MODA vocabulary). The formal Change Set mechanism (`changes/<id>/proposal.md` + `impact.yaml`) has existed since Phase C (`docs/change-management.md`, `decisions/0031-change-set-mechanism.md`) and is **mandatory** for `operational`/`normative` change from that point on: a new Change Set in `changes/<id>/`, accompanying the Decision Record (when it involves a structural choice) and the corresponding sections of `SPEC.md`/`CHANGELOG.md`, all updated in the same PR. `editorial` change doesn't require a Change Set.
- Change the normative specification (`SPEC.md`) first when the obligation changes.
- Use a short-lived branch and PR for normal change; keep `main` as the only permanent integration branch.
- Update `CHANGELOG.md` for a notable behavior or contract change.
- Record a durable structural choice in `decisions/`.
- Update `ROADMAP.md` when direction changes; never use it as a task backlog or changelog.
- Update `UPGRADE.md` for adoption action required by a backward-compatible release.
- Update `MIGRATIONS.md` for an incompatible change.
- When operating only via MCP, without the ability to create a tag/release, give the human the exact tag, target branch, commit, title, description derived from the changelog, and release classification for creation after approval — never claim the tag or release exists. See `SPEC.md`, section 9, and `decisions/0014-mandatory-release-routine.md`.

## Versioning

Hipocampo follows [SemVer](https://semver.org/lang/pt-BR/) — full operational criterion in `SPEC.md`, section 9, and `decisions/0023-operational-criterion-for-semver-scope.md`.

## Conclusion

A change is only complete when:

- the intent and scope are explicit;
- the relevant Decision Record (when applicable), the Change Set (when `operational`/`normative`), and the corresponding sections of `SPEC.md`/`CHANGELOG.md` are synchronized in the same PR;
- no known critical finding is left hidden;
- affected documentation and generated disclosures are synchronized;
- no MODA conformance claim goes beyond what the evidence in `conformance/moda.yaml` supports.