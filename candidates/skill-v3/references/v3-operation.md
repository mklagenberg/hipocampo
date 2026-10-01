# V3 operation and compatibility

This is the skill-side operating guide for the unreleased V3.0.0 candidate. The
normative method remains in the canonical contracts; this document routes an
agent through their gates. It does not activate V3 for an existing instance.

## 1. Verify the tuple before operation

Establish each value from its authoritative source:

- the methodology release and contract baseline;
- the exact skill package version and integrity lock;
- the target vault's manifest, declared compatibility and verified-against
  source/version information.

Evaluate the declared methodology/skill/vault tuple through the compatibility
contract. A V2-compatible skill presented with V3 is
`unsupported_or_unknown`; block durable V3 operation. A V3-compatible skill
with a V2 vault yields `migration_required`; diagnose without V3 writes. An
unavailable source yields `access_unavailable`; do not infer compatibility.
An intact V3 tuple is only a compatibility result. It does not grant authority,
privacy permission or a host capability.

Do not equate these distinct facts:

- `compatibility` range: contracts the instance says it can support;
- `verified_against`: the version a responsible operator reports checking;
- source version/hash: the specific material examined;
- actual content state: what a bounded, authorized inventory establishes.

Never infer that a vault contains V2.2 content because the methodology's
released baseline is V2.2, or infer V3 readiness from `compatibility: ^3.0.0`.
Preserve unknown or conflicting values as unknown or conflicting.

## 2. Confirm authority, scope and operation capability

Before reading governed content, identify the actor and role, entity, knowledge
scope, source vault and explicit non-empty `authorized_vault_ids`. The requested
vault must be covered. Missing, empty, ambiguous or mismatched authorization
blocks the read. Resolve each entity and vault independently; do not widen
scope from shared access, matching labels, account membership or a Git remote.

Check tool capability for the requested operation separately from version
compatibility. Use a host adapter only as a transport to the canonical method.
If the host cannot supply the required authorization context or invoke the
canonical CRUD boundary, mark that operation unavailable and stop. Do not
fall back to direct repository/file writes or claim that a connector test
proves remote authorization.

## 3. Read and preserve source state

Use the V3 CRUD `read` operation. Read frontmatter first and validate the
request, version, entity, vault, scope, visibility, maturity, staleness and
provenance at read time. A Chunk result includes its parent Record context and
effective restrictions. A Record remains readable as prose when a referenced
Artifact is unavailable; do not fetch, reconstruct or substitute an Artifact
as an implicit part of Read.

Preserve source status. Stale, conflicting, inaccessible, provisional or
unknown information does not become current or factual because it was
retrieved, recent, relevant, hashed or authorized for disclosure. Keep
conflicting Records and evidence separate. Use `needs_review` when the contract
requires interpretation and state when no conclusion was consolidated.

## 4. Propose and commit governed changes

For a governed change, first prepare a proposal with actor, reason, expected
Record version, source/provenance, entity, scope, vault and required semantic
review reference. Evaluate contextual admissibility, privacy, authority,
applicability, conflict, maturity and staleness. Resolve uncertainty as a
finding or human gate; do not invent missing values.

Only after semantic admissibility, send the proposal through the canonical CRUD
gateway for deterministic schema, relationship, reference, version,
immutability, state-transition, idempotency and atomicity validation. Both
stages are required when governed knowledge changes. Neither stage replaces
the other. CRUD alone persists; a semantic reviewer, engine, MCP transport or
host file API never writes directly.

- **Create:** validate the complete Record, active Collection, unique child
  Chunk IDs, Artifact references and monotonic restrictions.
- **Update:** preserve `record_id`, advance `record_version` for a governed
  change, and preserve the source Record when a split is required.
- **Delete:** use `archived`/`superseded`; physical removal requires the narrow
  legal-remediation process and explicit human decision.
- **Move:** change physical path without silently changing identity or
  Collection relationships.
- **Artifact change:** version the Artifact and flag linked Records for review;
  never silently replace the version historically used.

## 5. Prepare a V2-to-V3 migration

A V2 vault is a migration source, not a V3 write target. First establish the
released target tuple, source version and exact vault/scope authorization.
Then prepare a complete vault-specific inventory and crosswalk for Records,
Chunks, Artifacts, Packages, references and inaccessible sources. Classify each
mapping and preserve unknowns as blocked or partial. Recheck privacy, authority
and acceptance separately for source, destination and derived representations.

Run synthetic fixtures first. A real migration additionally requires an
approved mapping, a destination contract, a tested rollback, a migration
receipt and explicit human approval for that exact vault and scope. Execute
only through canonical CRUD, preserve the V2 source, run required validation
and REM before any V3 item becomes `current` or `curated`, and reconcile the
source/destination ledgers. Migration approval does not approve publication or
LTE.

## 6. Preserve the V3.0.0 baseline

Treat raw V3.0.0 contract behavior as the compatibility baseline for every
later V3 minor and patch. A facade or adapter may translate host-specific
behavior, but it must preserve the V3.0.0 contract and observable guarantees.
The host is not the version authority. If a later version cannot preserve the
baseline, report incompatibility and require a separately approved transition;
do not relabel it as a compatible minor or patch.

## 7. Report result and limits

Report compatibility, authority/privacy, tool capability, semantic
interpretation and human decision as separate outcomes. State the exact source
and version checked, what was inaccessible or unverified, whether any semantic
result is partial, and what gate remains. A deterministic pass proves only
reproducible properties. AI review is interpretation, not truth proof. The
human remains the final authority for unresolved intent, risk acceptance,
migration, promotion and publication.
