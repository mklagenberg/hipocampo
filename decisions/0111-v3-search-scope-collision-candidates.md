# 0111 — V3 Search scope-collision candidates

**Status:** Accepted for the unreleased V3 candidate

**Date:** 2026-09-30

**Parent:** 0108-v3-search-progressive-disclosure

## Context

The Search contract accepts one declared entity and knowledge scope and may
search multiple authorized vaults. The same lexical term can appear in more
than one eligible Record, or in Records outside the request's boundaries. A
matching term alone cannot establish that the Records share governance,
authority, provenance or meaning.

## Decision

For the unreleased V3 candidate:

1. Filter candidates by the requested entity, authorized/requested vault set
   and knowledge scope before relevance ranking. Do not disclose or mention
   candidates outside those boundaries.
2. If multiple authorized vaults within the declared entity and knowledge
   scope return same-term candidates, keep each Record separate with its own
   provenance, authority, privacy, epistemic status and limitations.
3. Do not merge candidates, choose a winner, or infer shared authority from
   lexical overlap, semantic similarity, ranking, recency or common storage.
4. Preserve the semantic collision as `needs_review` where a combined
   interpretation or answer is requested. Reading each eligible Record still
   follows its own authorization, privacy and disclosure gates.

## Rationale

This preserves the ownership boundary and allows multiple perspectives to
coexist without forcing consensus. Scope filtering prevents cross-entity or
out-of-scope disclosure; separate results keep relevant authorized candidates
available for later human interpretation without silently changing their
authority or provenance.

## Discarded alternatives

- **A — exclude out-of-scope candidates and keep eligible multi-vault
  candidates separate:** chosen; it applies the declared request boundary and
  preserves provenance without treating lexical overlap as identity.
- **B — merge matching or semantically similar candidates:** rejected because
  similarity does not establish shared entity, authority, scope or truth.
- **C — return only the highest-ranked or most recent candidate:** rejected
  because ranking and recency do not resolve governance or epistemic conflict.
- **D — block the entire search when eligible vaults return similar terms:**
  rejected as overbroad; bounded separate results can be disclosed safely
  within the declared authorization and scope.

## Constitutional and contract impact

Compatible with Constitution clauses `2.4`, `2.5`, `2.7`, `2.9` and section
`4`; management Decisions `DEC-0061`, `DEC-0063`, `DEC-0065` and `DEC-0066`;
and candidate Decision `0108`. It clarifies filtering and result separation;
it does not grant access, merge Records or change the CRUD write boundary.

## Boundaries and validation

Applies only to the unreleased V3 candidate. The sanitized validator must
confirm that eligible same-term candidates in two authorized vaults remain
separate, while same-term candidates in another entity or knowledge scope are
excluded. It does not prove semantic truth or authorize cross-entity search,
host integration, real-vault access, migration or publication.

## Approval

Alternative A was accepted explicitly by the project operator on 2026-09-30.
