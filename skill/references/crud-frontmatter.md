# V3 CRUD and read validation

Full contract: `docs/v3-crud-contract.md`. V3 has one governed Record
read/write boundary: the canonical CRUD gateway. Host, filesystem and GitHub
APIs are transports or adapters; they do not become alternate persistence
paths.

## Read

Before a governed Read, identify the authenticated actor, exact repository,
entity and scope, and verify current GitHub MCP read access to that vault.
Lack of a personal anchor or explicit vault registration does not block
presentation through `internal`. An asserted `authorized_vault_ids` value,
invitation, current login, cached clone or visibility label alone is not
proof of access. `confidential` and `restricted` require separate current
clearance under the target vault policy. If the host cannot filter before
exposing a higher-classification body, that read mode is unavailable.

Read frontmatter first and validate the record/version, entity, scope, vault,
visibility, maturity, staleness and provenance at the time of the Read. Fetch
the body only when needed for the stated intent. A Chunk is never presented
without its parent Record context and effective restrictions. Read the stored
Record prose directly; an unavailable Artifact does not make the Record
unreadable. Read does not fetch or reconstruct Artifacts and never writes.

Report stale, partial, conflicting or inaccessible source state. A Read does
not settle truth, authority or conflict. Never update metadata or repair a
Record while reading.

## Governed changes

Every Create, Update or governed Delete proposal carries the actor, reason,
expected Record version, required semantic-review reference and idempotency
key, along with provenance and the relevant entity/scope/vault context.

1. **Semantic review:** assess provenance, authority, privacy, applicability,
   conflict, maturity and staleness. Record a finding, uncertainty or human
   gate when any item cannot be resolved. The review proposes; it does not
   persist.
2. **Deterministic validation:** the canonical CRUD gateway independently
   enforces schema, references, versions, immutable identity, allowed state
   transitions, idempotency and atomicity before persistence. Python is one
   implementation, not a prerequisite. Without Python, collect reproducible
   evidence through GitHub MCP for every required check; a semantic assertion
   is not a substitute for an expected head, hash or version check.
3. **Commit:** only that gateway may persist after both required validations
   pass. For remote vaults, the gateway uses GitHub MCP transport and verifies
   the resulting ref and readback. Persist the Record and its key-hashed
   idempotency receipt sidecar atomically in the same expected-head Git commit;
   reconcile retries against the receipt and current Record before reporting
   success. Direct file writes and convenience APIs
   outside the gateway are prohibited. Missing MCP capability or permission
   blocks the dependent remote mutation without implying a policy denial.

Metadata-only normalization may use the deterministic CRUD path only when it
does not make a semantic claim or change governed meaning.

## Operation rules

- **Create:** validate the full Record, active Collection membership, unique
  Chunk IDs, Artifact references and monotonic restrictions.
- **Update:** preserve `record_id`; advance `record_version` for governed
  changes; preserve the original Record when splitting; keep entities separate.
- **Delete:** use `archived` or `superseded`, never physical deletion except
  through the narrow legal-remediation process and an explicit human decision.
- **Move:** change physical path only; preserve identity and logical Collection
  membership.
- **Artifact update:** version the Artifact and submit a CRUD mutation that
  flags the Record for review. Do not replace the historically used Artifact
  version silently.

## Scope and privacy

Resolve actor/role, Source, entity, knowledge scope, source vault, visibility,
maturity, staleness, authority, destination contract and transfer mode before
any mutation or package assembly. A shared Source can support separate
entity-bound Records with common lineage; it does not authorize synchronization
or merging. Cross-entity transfer requires destination acceptance, Owner
approval and minimization. Privacy and authority are independent gates.

Never retain credentials or non-public financial values. Do not treat a
methodology upgrade as permission for a repository-wide historical sweep.
Raise findings first; remediate only within a confirmed scope and through the
governed CRUD/REM flow.
