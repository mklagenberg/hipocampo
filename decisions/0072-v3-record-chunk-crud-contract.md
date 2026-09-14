# 0072 — V3 Record–Chunk CRUD and package integrity contract

**Status:** Accepted for the unreleased V3 contract

## Context

The V3 model distinguishes a governed Record from contextual Chunks, logical
Collections, separate Artifacts, and transport Packages. CRUD must preserve
those distinctions while preventing orphaned Chunks, weaker visibility in a
child object, stale material presented as current, or partial selections that
lose their parent context.

## Decision

Record is the persistence and governance unit. A Record has a stable
`record_id`, an explicit active Collection membership, a physical path that is
not its identity, and a versioned governed envelope. A Chunk is addressed by
`record_id + chunk_id`, is not an autonomous CRUD unit, and inherits Record
restrictions unless an explicit, non-weakening exception is represented.

Create and Update validate the complete Record envelope. Update preserves
`record_id`, increments the Record version for governed changes, and does not
pretend that a Chunk edit is an independent document version. Read of a Chunk
returns its parent identity and required context. A physical move preserves
Record identity, Collections, and the root Collection index.

Every Record has at least one active Collection. The root index catalogs
Collections; directories organize files; tags remain transverse discovery
attributes. None of these replaces Record identity or type.

Packages may select Records or Chunks. A partial Chunk Package carries the
parent Record identity, selection marker, context, provenance, effective
visibility, staleness, and integrity metadata. Sending is blocked when the
destination cannot handle the effective restriction or when staleness has not
been resolved for a current-use operation. Artifacts remain separate; changing
an Artifact version never silently updates its Record.

## Consequences

The CRUD boundary can be tested without treating every physical file or search
fragment as an independent object. Privacy and staleness are checked before
relevance or transport. Split, merge, promotion, migration, and semantic
disposition remain explicit operations rather than side effects of Create,
Read, Update, or Package selection.

## Rationale

The contract follows the monotonic restrictions and context-preservation
decisions already accepted for the V3 model. It makes the smallest unit that
can be governed a Record while still allowing retrieval and transport at Chunk
granularity. A fail-closed Package boundary prevents partial context from
becoming an apparently complete answer.

## Discarded alternatives

- treating Chunks as independent documents — rejected because it creates
  duplicate identity, version, and privacy state;
- deriving Collection membership from directories — rejected because physical
  organization changes over time;
- allowing a child object to weaken the Record restriction — rejected by
  monotonic privacy and staleness precedence;
- silently refreshing a Record when an Artifact changes — rejected because a
  reference or hash identifies a version, not an authorization to rewrite
  knowledge.
