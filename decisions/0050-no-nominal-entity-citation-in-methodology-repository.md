# 0050 — No nominal entity citation in the methodology repository

**Status:** Accepted

## Context

Several files in this repository — worked examples, a real-case evaluation scenario, Decision Record context sections, a frozen audit, and one artifact-path entry in an accepted Change Set — cited the real name of Mau's employer, a real colleague's first name, and Mau's real personal GitHub handle, to make the Fact/Account/Opinion/Memory taxonomy (`decisions/0026`) and the evaluation scenarios (`decisions/0039`) concrete and evidence-based. Found and flagged by Mau directly (2026-08-19): `docs/evaluation-scenarios.md`'s Scenario 1, `decisions/0026`'s Context and Discarded alternatives sections, `decisions/0039`'s Context/Decision/Rationale, `decisions/0024`'s Context, `skill/references/instantiation.md`'s worked example, the frozen `audits/moda/2026-08-17-v1.0.0-self-audit.md`, and one artifact-path entry in the accepted Change Set `changes/0038-0039-failure-recovery-and-evaluation-scenarios/impact.yaml`.

This repository is the methodology itself — public, meant to be read by anyone adopting Hipocampo, structurally distinct from a content instance (`SPEC.md`, section 1: this repository never stores real content from any instance). That boundary was already correct for *content* (notes, vault data); it did not yet cover *citations of real entities used as pedagogical examples inside the methodology's own reference material* — a narrower but real gap this decision closes.

## Decision

No file in the `hipocampo` methodology repository may name a real, identifiable entity — a company, business unit, or named individual — nor a real, identifiable personal account handle, in any context: worked example, evaluation scenario, Decision Record rationale, audit finding, or Change Set note. This applies unconditionally, with no risk-based exception — a single company name in one worked example is not judged "low-risk enough" to keep.

Where a real case is genuinely more evidentially valuable than a constructed one (an evaluation scenario built from an actual documented failure, for instance), the case is kept, but every identifying token is replaced with a clearly-marked, generic or fictional placeholder — a bracketed role (`[Colleague]`), a fictional company name (`Acme` — already an established convention elsewhere in this repository's own examples, e.g. `skill/references/routines.md`'s `case-acme.md`), a generic handle label (`@personal-handle`) — chosen so the substitution reads unambiguously as a redaction, never as a coincidental resemblance to a different real entity.

This is a standing, forward-looking rule, not a one-time cleanup: any future contribution to this repository — a new Decision Record, evaluation scenario, worked example, or audit — is written with this constraint from the start, the same way `SPEC.md` section 1's real-content boundary already is.

## Rationale

The real-content boundary (`SPEC.md`, section 1) already established that this repository's job is to hold the *rule*, never the *content* an instance manages. A real company name, a real colleague's name, or a real personal handle cited inside an example is a narrow but genuine instance of the same category error: real content, standing inside the methodology's own text, in a repository more widely readable than any single instance — public, cited in onboarding material, potentially read by people with no relationship to that entity or colleague. Anonymizing preserves every example's pedagogical and evidentiary value intact — the taxonomy gap `decisions/0026` closes, and the failure mode `docs/evaluation-scenarios.md`'s Scenario 1 tests, are both fully preserved under a fictional company and a bracketed colleague placeholder — while removing the one part of each example that was never necessary for that value: the specific real-world identity.

## Discarded alternatives

- **Case-by-case risk judgment (keep low-visibility citations, redact only the clearly sensitive ones).** Rejected per Mau's explicit instruction: unconditional, not risk-scored.
- **Delete the real-case examples entirely instead of anonymizing them.** Rejected: their value comes from being drawn from an actual documented situation, not invented from scratch (`decisions/0039`'s own rationale for why a real case was chosen); anonymizing keeps that grounding while removing the identifying content.
- **Leave frozen evidence (`audits/moda/2026-08-17-v1.0.0-self-audit.md`) and the accepted Change Set (`changes/0038-0039-.../impact.yaml`) untouched, citing `docs/change-management.md`'s "never edited after acceptance" rule as an absolute bar.** Rejected: the no-nominal-entity-citation rule is unconditional per Mau's instruction and takes precedence over that narrower rule when the two conflict. Instead, both are corrected with the narrowest possible in-place token substitution, each accompanied by a visible, dated note documenting exactly what changed and why, citing this Decision Record and `changes/0051`. This preserves the traceability the immutability rule exists to protect, without leaving real entity data sitting in a public repository indefinitely.

## Status

Accepted.
