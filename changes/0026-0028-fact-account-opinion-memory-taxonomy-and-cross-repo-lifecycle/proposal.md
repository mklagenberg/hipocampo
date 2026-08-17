# Fact/Account/Opinion/Memory taxonomy + cross-repository lifecycle (Promote/Depromote/Redbutton)

**Note:** Retroactive (backfill) Change Set, created after implementation and merge (PR #22, 2026-08-17) — the first exercise of the Change Set mechanism adopted in `decisions/0031`. The actual work was already reviewed and merged before this document existed; it reconstructs the proposal and impact to validate the template, not to reopen the decision.

## Problem

Hipocampo had no formal vocabulary to distinguish verified information from personal opinion/memory within a corporate-instance document — a risk of undue personal liability without clear signaling. There was also no formal mechanism to move or remove content between repositories of the same person/organization (personal↔corporate reclassification, confidentiality-level correction, policy-violation remediation) — only single-repository CRUD (section 2-B).

## Current contract

`SPEC.md` section 2 did not distinguish information type within a document's body. Section 8 covered only single-repository CRUD; there was no formal action to move content between repositories of the same owner, nor to physically delete content that violated the sensitive-data policy (section 2-A) outside the narrow trigger of a formal legal request (`decisions/0010`).

## Proposed contract

- Four-type information taxonomy (**Fact**, **Account**, **Opinion**, **Memory**) + `contains_subjective_content` field, with an explicit confirmation gate before writing new Opinion/Memory content in a corporate instance (`decisions/0026`).
- Three cross-repository lifecycle actions — Promote (personal → corporate, two paths), Depromote (intra-domain downgrade), Redbutton (policy-violation remediation) — complementary to the existing CRUD (`decisions/0027`).
- Physical-deletion trigger (`decisions/0010`) broadened to also cover confirmed sensitive-data-policy violations identified by structural audit or by the operator, not only formal legal requests (`decisions/0028`).

## Alternatives

- **Treat Opinion/Memory as Fact without distinction.** Discarded — loses the personal-liability-risk signal that motivated the change.
- **Resolve cross-repo reclassification with ad-hoc manual editing, without a named action.** Discarded — without consistent `related`/`superseded_by`, it breaks traceability and the "document never physically deleted" discipline (invariant 3).
- **Deletion trigger restricted only to a formal legal request.** Discarded — left policy violations found by audit without formal remediation, even without a request from the data subject.

## Risks

- Confusion between `contains_subjective_content` and `visibility`: mitigated by explicit text in `SPEC.md` section 2 distinguishing the two fields.
- Misuse of Redbutton to remove merely inconvenient, non-violating content: mitigated by an always-explicit human decision and a narrow scope (reserved for actual policy violation or legal risk).

## Acceptance criteria

- [x] `SPEC.md` section 2 documents the four-type taxonomy and `contains_subjective_content`.
- [x] `SPEC.md` section 13 documents Promote/Depromote/Redbutton.
- [x] `SPEC.md` section 8 documents the broadened physical-deletion trigger.
- [x] `CHANGELOG.md` records the three changes under `[Unreleased]`.
- [x] `decisions/0026`, `0027`, `0028` merged.

## Compatibility and migration

Additive — no existing instance becomes formally incompatible without these actions (test from `decisions/0023`). MINOR scope in isolation; it enters the batch of accumulated changes toward v2.0.0 by accumulation decision (`decisions/0021`), not because it forces MAJOR on its own.

## Recovery

Reverting the three decision commits + the corresponding `SPEC.md`/`CHANGELOG.md` sections would be the rollback path, if needed — no migrated adopter depends on this yet (recent, unreleased work).