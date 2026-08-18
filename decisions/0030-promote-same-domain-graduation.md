# 0030 — Promote: generalization for graduation within the same domain

**Status:** Accepted

## Context

`decisions/0027` defined Promote as a cross-domain action (personal → corporate) and Depromote as a downgrade within the same ownership domain. `decisions/0029` introduces the `curation_status: staged` field, applicable to `empresa-confidencial` documents that are candidates to eventually become `empresa-público`. Moving a `staged` document from `empresa-confidencial` to `empresa-público` isn't covered by either existing action: it's not Promote (it doesn't cross the personal/corporate boundary) and it's not Depromote (Depromote is specifically defined as a downgrade — the opposite direction from this graduation).

Same pattern already used by `decisions/0028` when broadening the trigger of `decisions/0010`: record the extension as a satellite decision, without editing the original one, preserving traceability of which question each Decision Record answers.

## Decision

The Promote action (`decisions/0027`, `SPEC.md` section 13) now covers two cases:

1. **Cross-domain** (already existing, unchanged): personal → corporate, with the two paths (elegant and literal) already defined.
2. **Graduation within the same domain** (new): an `empresa-confidencial` document with `curation_status: staged` being promoted to `empresa-público`.

Case 2 always uses Promote's **elegant path** — it creates a new document at the destination, following the discipline of `decisions/0011`, with bidirectional `related` and a `revision_note` documenting the graduation. The literal path never applies to this case: since origin and destination are in the same ownership domain (`empresa`) the whole time, there's no new ownership transfer at stake (`decisions/0007` doesn't change), so the literal path's mandatory warning about irreversibility and ownership transfer would be false — its content simply doesn't apply here.

The originating document is neither deleted nor has its `status` changed — the agent updates `curation_status` to `permanent` (ending the candidacy) or keeps `staged` with `related` pointing to the new public document, at the discretion of whoever confirms the action at the moment of promotion.

**Precondition:** only a document with `curation_status: staged` is eligible for this variant. A `permanent` document (or one with the field unfilled, which uses the same default) needs explicit `curation_status` reclassification first — a human decision separate from the decision to promote, to prevent a promotion from silently "resolving" a confidentiality classification that no one purposefully reviewed.

## Rationale

Reusing Promote instead of creating a fourth action avoids duplicating a mechanism that already exists and already works (the elegant path). The only real variable between the two Promote cases is whether ownership changes — and that is already exactly what determines, within the action itself, whether the literal path is available (only in the cross-domain case) or not (never in the intra-domain case). Adding a new action just to name this distinction would create conceptual surface without behavioral gain.

## Discarded alternatives

- **A new fourth action ("Publish"/"Graduate").** Discarded — it would duplicate the mechanism of Promote's elegant path with no real behavioral difference, only a naming one; it increases the surface anyone operating Hipocampo needs to remember, unnecessarily.
- **Treat it as an inverted Depromote.** Discarded — Depromote is specifically defined as a downgrade (`decisions/0027`); inverting its behavior to also cover upgrades would confuse the action's name with what it actually does.
- **Allow the literal path also in the intra-domain case.** Discarded — the literal path exists specifically to warn about ownership transfer (`decisions/0007`); since ownership doesn't change within the same domain, presenting that warning would be false and would confuse whoever is confirming the action.
