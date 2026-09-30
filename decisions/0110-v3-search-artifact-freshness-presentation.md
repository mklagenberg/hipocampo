# 0110 — V3 Search artifact freshness presentation

**Status:** Accepted for the unreleased V3 candidate

**Date:** 2026-09-30

**Parent:** 0109-v3-record-content-independent-of-artifact-accessibility

## Context

Decision `0109` separates persisted Record content from access to its linked
Artifact. The Search result must preserve that access limit, but a user-facing
sentence that only says the Artifact is unavailable does not explain which
version the Record represents or whether later source updates are included.
The candidate also distinguishes an accessibility check from observation of
the content version.

## Decision

For the unreleased V3 candidate:

1. Preserve the partial disposition and the internal
   `artifact_access_unavailable` limit when the linked Artifact cannot be
   accessed, while the Record itself remains readable and passes its own
   disclosure gates.
2. In default user-facing prose, state the observation timestamp of the exact
   Artifact version represented by the Record and say that later updates were
   not verified or reflected in the response. Do not expose the literal
   availability state as the user-facing explanation.
3. Use `observed_at` only when it records successful observation of the
   represented content version. `checked_at` records an accessibility check
   and is not a substitute for a content-read timestamp.
4. If no valid `observed_at` is recorded, state that the observation date is
   unrecorded and later updates were not verified or considered. Never
   fabricate a date or imply currentness.
5. Keep the structured result, audit trail and deterministic evidence
   explicit about the internal Artifact access limit. This decision changes
   default wording, not authorization, disclosure level or source state.

## Rationale

The user needs the freshness boundary to understand what the result includes.
An observation timestamp gives that boundary when evidence exists; the
missing-date fallback preserves uncertainty. Separating `observed_at` from
`checked_at` prevents an access probe from being misrepresented as reading the
source content.

## Discarded alternatives

- **A — report the observed-version date and exclude later updates from the
  response:** chosen. It preserves Record readability and makes the temporal
  boundary actionable without overstating source verification.
- **B — block at `L0` until the Artifact is accessible:** rejected because it
  makes Artifact access a precondition for reading the governed Record,
  contrary to Decision `0109`.
- **C — return prose as fully accepted and only add an availability warning:**
  rejected because it can imply currentness and keeps the user-facing message
  centered on availability rather than what source version was considered.
- **D — hide the Record body at `L1`/`L2` until the Artifact is verified:**
  rejected as a general rule because it conflates source verification with
  Record authorization; requests that specifically depend on currentness or
  Artifact analysis may still be limited separately.

## Constitutional and contract impact

This is compatible with Constitution clauses `2.1`, `2.2`, `2.7`, `2.8`,
`2.9`, and the resolution procedure in section `4`. It preserves the
independent Record and Artifact boundaries in Decision `0109`, the layered
Search presentation in `0108`, and the separation between dimensions and
readable prose in management Decision `DEC-0063`. The CRUD read boundary and
all privacy, authority, state and disclosure gates remain unchanged.

## Boundaries and validation

This Decision applies only to the unreleased V3 candidate. It does not alter
v2.2.0, authenticate a host, access real vaults, fetch or reconstruct an
Artifact, migrate, publish, deploy or activate V3. The sanitized validator
must cover a known observation timestamp and a missing timestamp; user-facing
prose must avoid the raw availability label while the structured result
retains it.

## Approval

Alternative A with the observation-date wording and missing-date fallback was
accepted explicitly by the project operator on 2026-09-30.
