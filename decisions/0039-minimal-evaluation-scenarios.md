# 0039 — Minimal representative evaluation scenarios

**Status:** Accepted

## Context

Major finding 7 from the 2026-08-17 MODA self-audit: the "quality and evaluation" dimension (MODA SPEC, 4.10) was entirely unaddressed — "no representative test scenario, baseline, or acceptance threshold formalized" (`conformance/moda.yaml`, control `quality_and_evaluation`). The audit's own action plan already names one ready-made candidate: the `@personal-handle` handle misused in `org-acme/acme-latam-observacoes.md`, a `hipocampo-company` document mixing Account and Opinion about a named real person, violating `decisions/0020` — fully described in `decisions/0026-account-vs-opinion-in-corporate-instance.md`. (Entity, colleague, and handle are anonymized placeholders — `decisions/0050-no-nominal-entity-citation-in-methodology-repository.md`.)

This repository never stores real content from any instance (`SPEC.md`, section 1) — an automated harness that executes scenarios against a live vault fixture is not an option without violating that boundary. The project's own scale (one person, no external certification target, `decisions/0037`'s proportionality reasoning) also argues against building a scored acceptance-threshold system that would itself need auditing and upkeep.

## Decision

Add `docs/evaluation-scenarios.md`: a minimal, human-run reference of representative scenarios an operator or auditor can walk through to check whether an agent operating this methodology behaves as `SPEC.md`/`decisions/` prescribe. Not a pass/fail test suite, not wired into CI, no scoring mechanism — a reference document, read and reasoned about by a human (or an agent, self-checking), the same way the Decision Records themselves are read and reasoned about rather than mechanically executed.

Four scenarios, chosen to span both the failure-and-recovery dimension (`decisions/0038`) and the quality-and-evaluation dimension this Decision Record closes, without attempting exhaustive coverage:

1. **A real, already-documented failure case** — the `acme-latam-observacoes.md` handle/labeling violation, testing whether `decisions/0020`'s identity rule and `decisions/0026`'s write gate, if applied today, would have caught it.
2. **A ritual-discipline case** — an expired `ttl` plus a deprecated controlled-vocabulary value, testing whether the frontmatter audit (section 5-B) correctly only reports, and whether an agent correctly resists "helpfully" auto-fixing a flagged value outside the REM ritual's explicit-plan-before-write discipline (invariant 5).
3. **A policy-refusal case** — a request to record a banned data type (a colleague's salary) in a corporate instance, testing section 2-A's ban and section 14's unsafe-request rule (refuse at the point of violation, offer a compliant alternative, not a blanket refusal).
4. **A correct-path, multi-Decision-Record case** — a Promote (personal → corporate, elegant path), testing whether all of `decisions/0011`, `0020`, `0026`, and `0027` are actually applied together, not just individually.

`docs/evaluation-scenarios.md` cross-references `GETTING-STARTED.md`'s "Typical use cases" section (`decisions/0038`'s companion editorial addition) without duplicating it: the use cases show the ordinary path for a newcomer; these scenarios probe judgment specifically at points where it's easy to get wrong.

## Rationale

Built from real, already-documented material — the `acme-latam` case was the audit's own suggested candidate, and the other three scenarios are direct applications of rules already normative in `SPEC.md` — rather than invented from scratch. One real failure case plus three representative correct/edge-path cases is enough to make the two open MODA dimensions checkable in practice without requiring either a new automated harness (which the "never stores real content" boundary rules out anyway) or an exhaustive scenario catalog that would itself become a maintenance burden disproportionate to a one-person-maintained methodology.

## Discarded alternatives

- **An automated test harness executing these scenarios against a live agent.** Rejected — there is no deterministic way to grade a judgment-based response with today's tooling (the same reasoning `decisions/0036` used to scope automation to mechanically-checkable structure only, not semantic correctness); it would also require a live vault fixture, which this repository explicitly never stores (`SPEC.md`, section 1).
- **Folding these scenarios directly into `SPEC.md`.** Rejected — `SPEC.md` is normative; these are illustrative. Same reasoning already used to keep `docs/vocabulary-dictionary.md` outside `SPEC.md` (`decisions/0035`).
- **Exhaustive scenario coverage, one per Decision Record or `SPEC.md` section.** Rejected as disproportionate — "minimal representative" is the audit's own phrasing (Onda 4). Four scenarios, chosen to span both open dimensions rather than to enumerate every rule, is enough to be useful without becoming something that itself needs auditing over time.
