# 0108 — V3 Search & Progressive Disclosure engine

**Status:** Accepted for the unreleased V3 candidate

## Context

The V3 candidate has contracts for Records, Chunks, provenance, governance,
delivery and operational audit, but it does not yet define the read-side
capability that selects relevant material and controls how much of it may be
shown. Without that boundary, relevance could be mistaken for authority,
recency for truth, or retrieval for permission to disclose.

## Decision

Adopt one logical `Search & Progressive Disclosure` engine with the following
contract:

1. Search is read-only and evaluates relevance, authority, privacy, epistemic
   state, evidence and limits as independent dimensions.
2. Disclosure is explicit and monotonic through five levels: `L0` none,
   `L1` metadata, `L2` Record envelope, `L3` selected Chunk content and `L4`
   expanded authorized content.
3. A higher relevance, more recent source, or richer result never upgrades
   authority, epistemic status, privacy permission or disclosure entitlement.
4. The default presentation is integrated didactic prose. Separate fields or
   a table are produced only when explicitly requested; material limitations
   remain visible in either mode.
5. Deterministic guardrails enforce identity, entity, vault, scope,
   disclosure, provenance, state, privacy, no-mutation, trail and limit
   requirements. Intent, relevance, conflict, applicability, contextual
   authority and abstention remain semantic review concerns.
6. The first implementation gate is local and read-only, using sanitized
   fixtures distinct from all real vault caches. MCP or host integration is a
   later gate.
7. Record mutation remains exclusively under canonical Record CRUD. Search
   may request a governed read or hand off a write-requiring flow, but it never
   writes a Record or bypasses CRUD.

## Rationale

This keeps retrieval useful without making it an authority engine. The
separate disclosure scale makes least privilege observable, while the
independent dimensions preserve uncertainty and provenance. A single logical
boundary avoids a premature physical refactor and keeps the existing CRUD
mutation guarantee intact.

## Discarded alternatives

- A single opaque `confidence` score was rejected because it collapses
  relevance, authority, privacy and epistemic state into an unsafe proxy.
- Automatic expansion to the most detailed result was rejected because
  relevance does not grant disclosure permission.
- Separate physical Search and Disclosure packages were deferred because the
  current evidence supports one logical engine, not a module split.
- Immediate MCP integration was rejected for this gate because host capability,
  authorization and remote-state behavior require a separate proof boundary.

## Boundaries

This decision and Change Set `0108` extend the unreleased V3 candidate only.
They do not change the active v2.2.0 `SPEC.md`, migrate or read any vault
cache, publish a release, configure MCP, or authorize remote writes.

## Acceptance

Accepted by the project operator on 2026-09-14, following management Decisions
`DEC-0061` through `DEC-0066`.
