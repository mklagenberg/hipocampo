# Change Set 0104 — V3 logical engine organization

## Intent

Organize V3 capabilities as logical engines with explicit ownership, use cases,
deterministic tests and semantic/cognitive tests, without prematurely moving
the existing implementation modules.

## Scope

Add the logical engine catalog, dependency map and per-engine test matrix;
assign current modules and validators to ten domain engines; add a structural
catalog validator; and link the organization to the canonical CRUD mutation
boundary.

This Change Set does not activate V3, migrate vaults, modify local vault
caches, publish a release, connect MCP to GitHub, or require a physical source
refactor.

## Acceptance criteria

- exactly ten logical domain engines are cataloged;
- every engine has at least two deterministic and two semantic/cognitive cases;
- every engine declares its contract, current implementation surfaces and
  CRUD/write boundary;
- semantic fixtures explicitly remain review-bound and do not claim automated
  truth evaluation;
- dependency and transport boundaries are documented;
- catalog, repository and full V3 validators pass twice;
- V2.2 remains the active published line.

## Recovery

Revert the candidate branch commit. The change is logical documentation and
fixture validation; no real vault or external service is affected.
