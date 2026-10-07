# V3 CRUD and read validation

Full contract: `docs/v3-crud-contract.md`. V3 has one governed Record
read/write boundary: the canonical CRUD gateway. Host, filesystem and GitHub
APIs are transports or adapters; they do not become alternate persistence
paths.

## Read

Before a governed Read, require an explicit actor and authorization context
covering the requested vault. The context must include a non-empty
`authorized_vault_ids` set containing that vault. Missing, empty, ambiguous or
mismatched authority fails closed. Do not infer access from repository
visibility, current login, invitation, shared Git provider or remembered
identity.

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
   transitions, idempotency and atomicity before persistence.
3. **Commit:** only that gateway may persist after both required validations
   pass. Direct file writes and convenience APIs are prohibited.

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
