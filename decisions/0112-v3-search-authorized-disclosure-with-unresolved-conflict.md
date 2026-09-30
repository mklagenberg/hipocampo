# 0112 — V3 Search authorized disclosure with unresolved conflict

**Status:** Accepted for the unreleased V3 candidate

**Date:** 2026-09-30

**Parent:** 0108-v3-search-progressive-disclosure

## Context

`SPD-S-005` asks whether explicitly authorized expansion can disclose content
when source provenance or epistemic status remains in conflict. Authorization
governs the disclosure boundary; it does not establish truth or settle which
source prevails. The runtime's operation status `accepted` could otherwise be
mistaken for acceptance of the retrieved knowledge.

## Decision

For the unreleased V3 candidate, accept alternative A:

1. Permit the explicitly requested disclosure level, including `L4`, only
   when the declared entity, vault, knowledge scope, privacy and canonical
   Record-read gates pass.
2. Preserve each eligible Record, evidence reference, provenance and
   epistemic status separately. Do not merge conflicting Records, select a
   winner or synthesize a settled conclusion.
3. Keep `interpretation_status: needs_review` on a conflicting result and on
   the overall Search response. Default prose must state that the conflict
   remains unresolved and no conclusion was consolidated.
4. Define operation `status: accepted` as successful completion of the
   requested read/disclosure within its gates; it is not epistemic acceptance
   or a truth judgment. When no conflict is declared, use
   `interpretation_status: not_assessed`, not an implicit semantic approval.

Authorization permits disclosure only. It does not raise authority or
epistemic status. Privacy restrictions, out-of-scope filtering, stale-source
limits and failed Record reads continue to govern independently.

## Rationale

Alternative A allows the operator's explicit disclosure choice to take effect
without pretending that access resolves conflicting evidence. Keeping the
operation disposition separate from `interpretation_status` makes the two
claims legible to both runtime consumers and people reading the response.

## Discarded alternatives

- **A — disclose to the explicitly authorized level and preserve the conflict:**
  chosen; it respects the operator's declared disclosure request while
  maintaining provenance and epistemic uncertainty.
- **B — cap at metadata until semantic review:** rejected as unnecessarily
  restrictive where disclosure is authorized and all privacy/scope/read gates
  pass; the contract can expose content without claiming it is settled.
- **C — block at L0 until sources agree:** rejected because disagreement does
  not itself revoke explicit disclosure permission; privacy or authority
  failures still block independently.
- **D — pick a source by recency, relevance or declared authority and
  synthesize:** rejected because those dimensions do not settle an epistemic
  conflict or license erasing provenance.

## Constitutional and contract impact

Compatible with Constitution clauses `2.2`, `2.4`, `2.5`, `2.7`, `2.8`, `2.9`
and section `4`; management Decisions `0062`, `0063` and `0065`; and candidate
Decision `0108`. No constitutional exception is required. The distinction
between operation disposition and interpretation status is explicit; Search
remains read-only and CRUD-only.

## Validation and limits

A sanitized deterministic case discloses two conflicting Records at L4 under
explicit authorization and asserts separate Record/evidence references,
preserved epistemic status, `status: accepted`, `interpretation_status:
needs_review`, and conflict-aware default prose. This does not prove truth,
authority, real-vault behavior, host integration or publication readiness.
Canonical two-pass constitutional revalidation remains required.

## Approval

Alternative A was accepted explicitly by the project operator on 2026-09-30.
