# 0036 — Deterministic validation of the methodology repository's own structure

**Status:** Accepted

## Context

Major finding 4 from the 2026-08-17 MODA audit (`audits/moda/2026-08-17-v1.0.0-self-audit.md`): Hipocampo has no deterministic/CI validation of its own structural integrity (schema, links, Decision Record template, version↔changelog consistency). `SPEC.md` section 5-B already specifies a deterministic frontmatter audit, but that ritual is scoped to **content instances** validating their own documents — the methodology repository itself has never applied the same discipline to its own files. `decisions/0031` (Change Set mechanism) already anticipated this gap explicitly: `docs/change-management.md`'s "Deterministic and human checking" section states that, until resolved, every Change Set check is human.

## Decision

Adopt `scripts/validate_hipocampo.py` — a dependency-free Python script — implementing four checks:

1. **Decision Record template compliance.** Every file in `decisions/` is either a canonical DR (`# NNNN — Title` matching the filename's number, a non-empty `**Status:**` line, and `## Context`/`## Decision`/`## Rationale`/`## Discarded alternatives` headings in that order) or a valid bilingual redirect stub (the `> **Movido / Moved:**` blockquote pointing at a target file that actually exists in `decisions/`).
2. **Internal link resolution.** Every markdown link in every `.md` file in the repository resolves: a relative path must point at a file that exists, and a `#anchor` fragment must match a real heading in the target, computed with GitHub's own heading-slug algorithm.
3. **Version consistency.** `README.md`'s `Current version: **X.Y.Z**` must match `CHANGELOG.md`'s latest `## [X.Y.Z]` released-version heading (`[Unreleased]` is skipped).
4. **Schema-field coverage report.** Every top-level field declared in `SPEC.md` section 2's frontmatter schema is checked for at least one mention across canonical Decision Records — reported as information, never as a failure.

Only checks 1–3 fail the build; check 4 is informational. A field can be fully and correctly specified in `SPEC.md` prose without a dedicated Decision Record citing it by name — `type` (section 3) is a real example found while designing this check — so treating check 4 as a hard gate would fail real, structurally sound content and teach maintainers to ignore the tool's output.

Wired into CI via `.github/workflows/validate.yml`, running on every pull request against `main` and on every push to `main`.

## Rationale

This closes major finding 4 with the minimum viable version the audit actually named — nothing broader. It is deliberately scoped to the repository's own literal structure (files present, links resolve, numbers agree, template shape matches) — not to whether a Change Set's declared impact matches its real diff (still human review, see `docs/change-management.md`), and not to the methodology's effectiveness as a knowledge system (MODA dimension 4.10, quality and evaluation — a different, still-open gap, see `ROADMAP.md`). A dependency-free script needs no install step in CI and no dependency-version maintenance, proportional to a task that only needs to read markdown files and apply two small deterministic operations (a heading-slug function, a small state machine over headings and blockquotes) — nothing here justifies pulling in a general markdown-processing library.

## Discarded alternatives

- **A general-purpose markdown-linting tool** (e.g., markdownlint, remark-lint). Discarded — these check generic markdown style, not this repository's own Decision Record template or the version↔changelog contract; all four checks here would still need to be hand-written on top of whichever tool was chosen, so adopting one only for the wrapping doesn't earn its dependency cost.
- **Hard-failing the schema-field-to-DR-association check.** Discarded — see Rationale: it would immediately fail on real, correct content (`type` has no direct DR citation today despite being fully specified), which is worse than not checking it at all.
- **Cross-checking a Change Set's `impact.yaml` claims against the actual PR diff, in this same script.** Discarded for now — out of the audit's named Onda 3 scope, and a materially harder problem (requires git-diff awareness, not just static file content). Left as a known, explicitly named open gap (`conformance/moda.yaml`, control `specification_driven_change_control`), not silently dropped.
