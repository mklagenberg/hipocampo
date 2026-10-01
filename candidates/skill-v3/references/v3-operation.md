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

## 3. Progressive-disclosure read

Use the canonical V3 Search and CRUD Read capabilities; a host adapter is only
transport. If the environment cannot enforce the requested vault authorization
and disclosure level through those boundaries, stop and report that capability
gap. Do not simulate a governed read by scanning vault files directly.

1. **Bound the request.** Establish the exact actor, entity, target vaults,
   knowledge scope, intent and non-empty `authorized_vault_ids`. Verify the
   compatibility tuple and privacy/visibility constraints before content is
   disclosed. Exclude candidates outside the authorized entity, vault and
   scope before relevance ranking.
2. **Search at the minimum level.** Submit a bounded Search request. Treat the
   requested disclosure as an upper bound; relevance, recency or a matching
   term never increases it. Start with safe metadata (`L1`) when it can answer
   the intent; otherwise request only the Record envelope (`L2`) needed to
   select a candidate.
3. **Filter from frontmatter.** Validate Record identity and version, entity,
   vault, scope, visibility, maturity, status, staleness and provenance at read
   time. Keep each Record distinct. Mark conflicts or unresolved authority as
   `needs_review`; do not rank them into a winner.
4. **Open selected content only.** Read the body of a selected Record only when
   its envelope cannot answer the stated intent. Read only the selected
   matching Chunk at `L3`, with its parent Record context and effective
   restrictions. Do not load neighboring bodies merely because a link or
   similarity score exists.
5. **Expand only on explicit authorization.** `L4` requires specific
   authorization for the additional content and all earlier gates. It is not
   implied by the user asking a broad question, by repository access, or by a
   high score. If authorization is absent or ambiguous, remain at the lower
   permitted level or block.
6. **Resolve only relevant adjacencies.** When a retrieved item raises a
   methodology question, consult the official repository declared by this
   package's `manifest.yaml` (`source_repository`). Use the immutable release
   tag matching the verified methodology version for normative behavior; pin
   the tag/commit and the exact file paths examined. Follow only direct links
   and dependency references needed to resolve the question, then stop. Use
   `main` only to check release/update availability, not to silently replace
   the contract of an already verified release. If the matching release or
   source commit cannot be established, report the methodology interpretation
   as unknown and do not infer a rule.

   This official-repository lookup is separate from vault relationships. To
   resolve a vault's `$alias:path.md` or `related` reference, use the authorized
   registry procedure for that vault scope; the public methodology repository
   is not a vault registry and does not authorize cross-vault reads.
7. **Return the smallest useful result.** Preserve source, entity, vault,
   scope, epistemic status, freshness and limits. Do not fetch or reconstruct a
   linked Artifact as part of Read. State `needs_review`, partial or blocked
   limits as applicable; retrieval and disclosure do not establish truth.

The contract's disclosure levels are `L0` none, `L1` metadata, `L2` Record
envelope/frontmatter, `L3` selected Chunk and `L4` explicitly authorized
expansion. See [Search & Progressive Disclosure](../../../docs/v3-search-progressive-disclosure-contract.md)
for the normative candidate contract.

## 4. Read and preserve source state

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

## 5. Propose and commit governed changes

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

## 6. Prepare a V2-to-V3 migration

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

## 7. Preserve the V3.0.0 baseline

Treat raw V3.0.0 contract behavior as the compatibility baseline for every
later V3 minor and patch. A facade or adapter may translate host-specific
behavior, but it must preserve the V3.0.0 contract and observable guarantees.
The host is not the version authority. If a later version cannot preserve the
baseline, report incompatibility and require a separately approved transition;
do not relabel it as a compatible minor or patch.

## 8. Report result and limits

Report compatibility, authority/privacy, tool capability, semantic
interpretation and human decision as separate outcomes. State the exact source
and version checked, what was inaccessible or unverified, whether any semantic
result is partial, and what gate remains. A deterministic pass proves only
reproducible properties. AI review is interpretation, not truth proof. The
human remains the final authority for unresolved intent, risk acceptance,
migration, promotion and publication.
