# Change Set 0108 — V3 Search & Progressive Disclosure

## Intent

Define the read-side `Search & Progressive Disclosure` engine for the
unreleased V3 candidate, preserving the canonical Record CRUD mutation
boundary while making relevance, authority, privacy, epistemic state,
provenance, disclosure and limits independently auditable.

## Current contract

V3 already defines Records, Chunks, provenance, governance, delivery and
operational audit, but the engine catalog has no explicit search/disclosure
boundary. The active released contract is v2.2.0. Search is not implemented
against real vault caches or MCP in this Change Set.

## Proposed contract

Add one logical engine with a local read-only first gate:

- five explicit disclosure levels, `L0` through `L4`;
- independent result dimensions for relevance, authority, privacy, epistemic
  state, evidence and limits;
- didactic prose by default, with separated fields or tables only on explicit
  request;
- deterministic guardrails for identity, scope, disclosure, provenance,
  privacy, no mutation and the redacted operational trail;
- semantic review for intent, relevance, conflict, applicability, contextual
  authority and abstention;
- CRUD remains the only Record mutation boundary, and host/MCP integration is
  deferred to a later gate.

## Taxonomy and test package

The engine, disclosure levels, result dimensions and presentation modes are
registered in `docs/taxonomy.md` and the vocabulary review is recorded here.
The deterministic package validates the contract envelope and four sanitized
fixtures. Three semantic cases are added to the review matrix and
constitutional basis; they remain review-bound and do not become automated
truth claims.

## Discarded alternatives

- One confidence score combining relevance, authority and epistemic status;
- automatic disclosure escalation based on ranking or recency;
- immediate physical module separation;
- immediate MCP/host integration;
- a default structured dump that would expose internal fields without an
  explicit request.

## Risks and mitigations

The main risk is that a useful search result is read as authorized or true.
Independent dimensions, fail-closed disclosure, explicit limits and semantic
review mitigate that risk. A second risk is accidental Record mutation; the
contract, CRUD wording, fixture `mutation: none` assertions and matrix binding
keep the write boundary explicit. A third risk is premature integration with a
host that cannot prove authorization; local sanitized fixtures keep this gate
bounded.

## Acceptance criteria

- the Change Set, Decision Record, contract, taxonomy and engine catalog agree;
- `L0`–`L4` are declared once as the controlled disclosure scale;
- every new deterministic case has an executable binding and assertion;
- every new semantic case has a fixture, disposition, constitutional basis and
  Decision Record references;
- the validator proves the deterministic contract envelope without claiming
  semantic truth;
- the V2.2.0 specification, real vault caches, private capture, MCP and remote
  state remain unchanged;
- declared validation passes twice on the same commit.

## Compatibility, migration and recovery

This is an unreleased V3 candidate addition. The active v2.2.0 contract and
existing instances require no migration. If the candidate is rejected, revert
only the new contract, taxonomy, matrix, fixtures, validator and projections;
no vault or Record state needs recovery. Any future activation or migration
requires a separate release/migration gate and human approval.
