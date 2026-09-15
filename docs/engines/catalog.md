# V3 logical engine catalog

**Status:** unreleased V3 candidate; logical organization only.

An engine is a capability boundary used to explain behavior, organize use
cases, assign tests and evolve the methodology consistently. It is not
necessarily a Python package or directory. Existing modules remain in place
until a physical refactor is justified by evidence.

Every engine has a deterministic boundary and, where meaning or context is
involved, a semantic/cognitive boundary. Semantic evaluation records a
reviewed disposition; it does not claim that an automated test can prove
knowledge truth.

## Canonical engines

| Engine | Primary responsibility | Current implementation surfaces |
|---|---|---|
| Record CRUD | sole Record mutation boundary | `v3_crud_engine.py`, `v3_mcp_crud_adapter.py` |
| Artifact & Provenance | Artifact identity, versions, hashes and representations | `v3_artifact_engine.py` |
| Ingress | processed, minimized and authorized destination entry | `v3_ingress_engine.py` |
| REM / Curation | review orchestration, queues, maturity and staleness disposition | `v3_queue_engine.py`, semantic fixtures |
| Package | selection, composition, fingerprint and package context | `v3_package_engine.py` |
| Delivery / Transfer | send, receive, acceptance, retraction and current-use transition | `v3_transfer_engine.py` |
| Governance | policy, privacy, authority, profiles and multivault boundaries | policy, privacy, profile and multivault engines |
| Operational Audit | events, correlation, ledgers, audit and revocation reach | event and audit engines |
| Migration / Compatibility | V2.2 to V3 preflight, mapping, rollback and readiness | migration, inventory and compatibility validators |
| Maintenance | frontmatter, vocabulary, aliases and mechanical queues | vocabulary, queue and normalizer surfaces |
| Learning & Evolution | discover and qualify new cases from events, logs and lessons learned | `v3_learning_engine.py` |
| Search & Progressive Disclosure | select relevant material and bound its authorized disclosure | `scripts/v3_search_engine.py`, `docs/v3-search-progressive-disclosure-contract.md`, local runtime and contract validators |

F0 and the `validate_*.py` scripts are Verification infrastructure, not domain
engines. The MCP adapter is transport infrastructure and may call only the
canonical CRUD boundary.

## Common engine contract

Each engine declares its input context, output disposition, evidence, limits,
allowed side effects and CRUD relationship. The common dispositions are
`accepted`, `blocked`, `needs_review`, `partial`, `authorization_required` and
`rework_required`.

An engine may produce a proposal, finding, review request, Package, ledger
entry or operational event. Only the CRUD engine may commit a Record mutation.
Operational metadata under `meta/` remains distinct from knowledge Records.

The complete case and test assignment is maintained in
`docs/engines/test-matrix.yaml` and checked by
`scripts/validate_v3_engine_catalog.py`. The executable deterministic runner
is `scripts/validate_v3_engine_suite.py`; semantic cases remain review-bound
and are checked for valid fixture references and complete review boundaries.

Search & Progressive Disclosure is a logical read-side boundary in the
unreleased candidate. Its first gate is now implemented as a fixture-backed,
local read-only runtime through the canonical CRUD read boundary. This does not
claim that an MCP or host integration exists; that remains a separate future
capability and authorization gate.
