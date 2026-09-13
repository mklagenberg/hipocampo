# 0071 — V3 record state and separated maintenance queues

**Status:** Accepted for the unreleased V3 contract

## Context

The V3 planning decisions separate epistemic nature, processing state,
maturity, authorization, and staleness. They also require three queues and a
READ operation that does not write directly. The current v2.1.1 specification
does not define the exact fields or queue envelope needed to implement those
rules.

## Decision

The unreleased V3 contract uses the following independent dimensions on a
Record or Chunk:

- `processing_state`: `new`, `in_review`, `consolidated`, `discarded`, or
  `superseded`;
- `maturity`: `new`, `provisional`, or `curated`;
- `staleness`: `current`, `stale`, `revalidation_required`, or
  `historical_exempt`;
- `epistemic.base`: `Fact`, `Account`, `Opinion`, or `Memory`;
- `epistemic.qualifiers`: zero or more of `Inference`, `Hypothesis`, or
  `Recommendation`;
- `provisional_type`: one of the approved provisional types, or an unknown
  identifier preserved as unknown/provisional.

Maintenance is split into `meta/fila-frontmatter.yaml`,
`meta/fila-staleness.yaml`, and `meta/fila-semantica.yaml`. Each finding stores
an identifier, target reference, rule revision, detection time, minimal
description, and lifecycle status. It never stores raw source content,
secrets, or sensitive values by default.

READ remains non-writing. A finding is persisted only through CREATE or UPDATE.
The frontmatter normalizer may apply an explicitly supported, deterministic,
idempotent vocabulary correction. It must not consume the staleness or
semantic queue. Staleness calculation may update the staleness state, but
disposition remains a REM or human decision. Semantic findings always remain
reviewed work.

## Consequences

V3 consumers cannot infer factual authority from `new`, `provisional`,
`in_review`, stale, or unknown material. Current answers may rely on curated,
authorized, non-stale material and must preserve its epistemic label and
provenance. Discussion answers may mention other material only with explicit
status and limits.

V2 documents remain readable without immediate migration. Missing V3 metadata
is treated as legacy/unmapped by a V3 consumer; no silent field conversion is
performed.

## Rationale

Keeping the dimensions independent prevents a document's processing stage or
freshness from being mistaken for truth. Separate queues let deterministic
mechanics correct only what they can prove while handing semantic judgment
back to REM or the responsible human. The compatibility fallback preserves
older instances without hiding that they have not yet been mapped to V3.

## Discarded alternatives

- one combined status field — rejected because it conflates independent axes;
- one maintenance queue — rejected because it mixes deterministic fixes with
  staleness and semantic judgment;
- direct writes from READ — rejected because observation is not authorization
  to mutate a vault;
- automatic semantic normalization — rejected because semantic adequacy and
  promotion require review.
