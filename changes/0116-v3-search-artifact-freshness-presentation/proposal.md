# Change Set 0116 — V3 Search Artifact freshness presentation

## Intent

Implement Decision `0110`: when a readable Record refers to an inaccessible
Artifact, keep the result partial and present the observed-version date and
the boundary on later updates instead of the literal Artifact availability
state.

## Scope

Clarify `observed_at` versus `checked_at`, render a freshness note in default
Search prose, preserve the internal Artifact access limit, and validate both
dated and undated sanitized cases. No source is fetched or reconstructed.

## Authority and compatibility

This Change Set implements Decision `0110` under Constitution clauses `2.1`,
`2.2`, `2.7`, `2.8`, `2.9`, and section `4`. It refines candidate Decision
`0109` only at the presentation boundary; it does not amend released v2.2.0.
It is normative for the unreleased V3 candidate, with SemVer `none` pending
release classification.

## Acceptance criteria

- an inaccessible Artifact does not block readable Record prose that passes
  all Record privacy, authorization, state and disclosure gates;
- default prose with `observed_at` reports that date and states later updates
  were not verified or reflected, without saying the Artifact is unavailable;
- when `observed_at` is missing, prose explicitly says the observation date
  is unrecorded and does not fabricate a timestamp;
- `checked_at` is never interpreted as the content-read timestamp;
- the structured result retains `artifact_access_unavailable` and the result
  remains `partial`;
- a separate unavailable-Record case continues to block at `L0`;
- sanitized validators and the integrated engine suite pass, with no real
  vault or Artifact access.

## Recovery

Reverting this Change Set restores the prior candidate presentation. It does
not change Decision `0109`, the released v2.2.0 contract, any vault or source
Artifact.
