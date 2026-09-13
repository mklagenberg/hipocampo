# Hipocampo V3 CRUD contract — unreleased candidate

This document defines the CRUD and Package boundary for the unreleased V3
candidate. It does not activate V3 for existing v2 instances.

## Governed objects

```yaml
record:
  record_id: "stable-id"
  record_version: 1
  entity: "entity-id"
  scope: "knowledge-scope"
  source:
    source_id: "stable-source-id"
    source_kind: "conversation"
  vault:
    id: "vault-id"
    profile: "entity | team | personal"
    role: "anchor | additional"
  governance:
    owner: "owner-id"
    authority: "authority-id-or-chain"
  physical_path: "records/example.md"
  status: "active"
  visibility: "internal"
  staleness: "current"
  collection_ids: ["collection-general"]
  chunks:
    - chunk_id: "chunk-1"
      parent_record_id: "stable-id"
      text_ref: "body-section-1"
      visibility: "internal" # optional; may only be more restrictive
      staleness: "current"   # optional; may only be more restrictive
  artifacts:
    - artifact_id: "artifact-1"
      role: "supporting-material"
      version: 1
      reference: "non-secret-reference"
      visibility: "internal"
```

`Collection`, `Artifact`, and `Package` are separate objects. A Record must
reference at least one active Collection. A Chunk must reference its parent
Record and cannot be presented without parent context. The physical path may
change without changing identity.

## CRUD behavior

- **Create:** validate the full Record, active Collection membership, unique
  Chunk IDs, Artifact references, and monotonic restrictions before persistence.
- **Read:** read frontmatter first; a Chunk read includes `record_id`, parent
  title/context, effective restrictions, and provenance. READ itself does not
  write.
- **Update:** preserve `record_id`, increment `record_version` for governed
  changes, validate all relationships, and preserve the original Record when a
  split is needed. A Chunk is not independently versioned by default.
- **Delete:** use the existing lifecycle (`archived`/`superseded`), not physical
  deletion, except for the narrow existing legal-remediation mechanism.
- **Move:** update physical path only; Collection membership and root index
  remain logical and stable.
- **Artifact update:** version the Artifact and flag the Record for review; do
  not silently rewrite the Record.

## Entity-aware operation boundary

Before Create, Read, Update, Chunk selection, or Package assembly, the
operation resolves:

1. actor and role (`Owner`, `Authority`, `Curator`, or `User`);
2. `Source` and provenance;
3. entity and knowledge scope;
4. source vault and vault profile;
5. visibility, maturity, staleness, and authority;
6. whether an entity-bound split is required;
7. destination-vault contract;
8. local, intra-entity, or inter-entity transfer mode.

`Source` is not a governance role. A Source may feed separate Records or Chunks
for different entities, preserving common lineage. A Chunk remains a child of a
Record and cannot become an autonomous CRUD object. A split preserves the
original Record and creates explicit entity-bound representations; it never
silently synchronizes them. A cross-entity split is delivery-governed: it
requires destination acceptance, Owner approval, and minimization.

The `entity`, `team`, and `personal` profiles are policy profiles, not
authority or maturity levels. `instance.entity` and `instance.role` remain
separate manifest concepts. Profile selection cannot grant write access or
automatic access to an anchor vault.

Same-entity sending uses the entity contract but still validates restrictions,
staleness, integrity, and authority. Cross-entity sending requires destination
compatibility, authorization, minimization, and destination acceptance; source
authority is not inherited.

## Package behavior

A Package records source, destination, composition, selection, context,
provenance, effective visibility, staleness, compatibility, and integrity. A
partial selection is explicit. A destination with weaker handling than the
effective visibility is blocked. A current-use send is blocked when the
selected material is stale or requires revalidation. A Chunk without a valid
parent is blocked.

The Package also records the source entity, destination entity, source-vault
profile, destination-vault profile, transfer mode, actor role, authority
resolution, and whether the selection came from an explicit governed split.

## Validation and migration boundary

`scripts/validate_v3_crud.py` exercises the contract with positive and
negative fixtures. The validator does not perform real vault migration,
remote transport, or authorization enforcement. A v2→v3 migration remains a
separate Change Set and must preserve IDs, relations, history, and rollback.

See `decisions/0072-v3-record-chunk-crud-contract.md`,
`docs/v3-contract.md`, and `docs/v3-artifact-contract.md`.
