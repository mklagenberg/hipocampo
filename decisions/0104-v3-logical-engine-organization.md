# 0104 — V3 logical engine organization

**Status:** Accepted for the unreleased V3 candidate

## Context

V3 has several related implementation modules, but physical module boundaries
do not by themselves explain the methodology's capabilities or their test
responsibilities. A physical refactor now would add risk without proving that
the boundaries are mature.

## Decision

Organize V3 capabilities as logical engines for explanation, use cases, tests,
and controlled evolution. The canonical engines are Record CRUD, Artifact &
Provenance, Ingress, REM/Curation, Package, Delivery/Transfer, Governance,
Operational Audit, Migration/Compatibility and Maintenance.

The logical engine definition is independent from Python package layout. The
existing modules remain where they are unless a later Change Set demonstrates
that a physical refactor improves consistency or operability.

Each engine must declare deterministic cases and semantic/cognitive cases.
Deterministic tests prove structure, state, identity, version, reference,
authorization predicates and side-effect boundaries. Semantic cases provide a
complete reviewed context and disposition; they do not claim that automation
can prove semantic truth.

F0 and `validate_*.py` remain Verification infrastructure. The MCP adapter
remains transport infrastructure. Neither is a domain engine.

## Rationale

Logical organization gives each capability a stable explanatory and testing
boundary while avoiding premature code movement. It also makes dependencies,
CRUD authority, semantic review and future ForgeFlow/plugin integration
explicit without coupling the methodology to a particular transport.

## Discarded alternatives

- A physical one-directory-per-engine refactor was rejected until evidence
  justifies its cost and regression risk.
- Keeping only a flat script list was rejected because it obscures capability
  ownership and test coverage.
- Treating every validator or helper as a domain engine was rejected because
  verification and transport have different responsibilities.

## Consequences

- The logical catalog and dependency map are normative navigation surfaces for
  the unreleased V3 candidate.
- Every engine receives deterministic and semantic/cognitive test assignments.
- Cross-engine mutations continue to return to the canonical CRUD gateway.
- The matrix can evolve independently from physical source layout.

## Validation

Run `scripts/validate_v3_engine_catalog.py --root .`, the per-engine commands
listed in `docs/engines/test-matrix.yaml`, and the complete repository suite.
Run the final validation twice and preserve the V2.2 compatibility boundary.
