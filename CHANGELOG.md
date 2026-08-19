# Hipocampo — Changelog

Version history of the methodology itself. Follows [SemVer](https://semver.org/lang/pt-BR/) — see SPEC.md, section 9.

## [Unreleased]

### Added
- **CI enforcement of repository structure, skill-doc consistency, and Change Set validation** (`changes/0050-ci-and-change-set-validation`) — `.github/workflows/validate.yml` (new) runs `scripts/validate_hipocampo.py`, the new `scripts/validate_skill_docs.py`, and the new `scripts/validate_change.py` on every PR against `main` and on push to `main`. `scripts/validate_skill_docs.py` checks `skill/**.md`'s `example/*.md` output-path literals against `scaffold/profiles/*.yaml`'s declared outputs, and flags any leftover use of the superseded `domain:` field under `skill/` (`decisions/0041`). `scripts/validate_change.py` validates every `changes/*/impact.yaml`'s own schema and, in PR mode, checks that a protected path changed in the diff is covered by an `updated` `impact[]` entry in a Change Set touched by the same diff — closing the gap `docs/change-management.md` previously described as "no deterministic validation compares this against the actual diff yet." `requirements-dev.txt` (new) pins PyYAML for the one script that needs it.

### Fixed
- **`conformance/moda.yaml` and `docs/change-management.md` corrected** — both previously cited `.github/workflows/validate.yml` as existing evidence before the workflow file actually existed in this repository. Found during a v2.0.0 personal-skill revalidation exercise. `repository_contract` and `specification_driven_change_control` now list the real scripts and workflow as evidence, with the diff-coverage check's heuristic (not semantic) nature made explicit; status stays `partial`.
- **`skill/SKILL.md` and `skill/references/instantiation.md`** — two doc-only bugs found during the same revalidation exercise: `skill/SKILL.md` pointed at a nonexistent `example/example-note.md` instead of `example/exemplo-nota.md` (the path `scaffold/profiles/*.yaml` actually declares); `skill/references/instantiation.md`'s worked example used the superseded `domain:`/`tier:` vocabulary instead of `entity:`/`role:`/`tier:` (`decisions/0041`). Editorial per `docs/change-management.md`'s class table — no Change Set required.

## [2.0.0] — 2026-08-19
