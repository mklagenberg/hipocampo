# Change Set 0079 — V3 multivault resolution

## Problem

Multiple vaults and entities require typed relationships and partial
resolution. Accessibility cannot become authority, and an unavailable source
must not be disclosed or silently revoked.

## Proposed contract

Add bounded multivault resolution for typed relations, hereditary succession,
cycles, collisions, conflicts and partial frontiers. Preserve entity, vault,
Source and Chunk context; keep semantic conciliation and human governance
outside deterministic graph traversal.

## Risks and compatibility

The candidate remains local and in-memory. No access is inherited, no remote
authorization is inferred, and no source is exposed merely because a graph
contains a relationship.

## Acceptance criteria

- typed relations and scope are preserved;
- cycles and collisions are deterministic diagnostics;
- inaccessible sources produce partial coverage without disclosure;
- entity-specific perspectives remain separate;
- composed personal, company and client fixtures pass.

