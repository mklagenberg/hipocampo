# Change Set 0102 — V3 `meta/` operational topology and no-inbox boundary

## Intent

Make the vault-local home of operational metadata explicit and remove the
ambiguity that historical V2 `inbox/` terminology might be mistaken for a V3
directory.

## Scope

Update the V3 candidate contract, Artifact provenance contract, operational
event contract, bilateral ledger contract, profile/audit contract, V2-to-V3
crosswalk and changelog. Add Decision Record 0102 and declare the canonical
`meta/` surfaces: Artifact index, events, ledgers, audits and the three
maintenance queues.

The Artifact index records traceability of the original source only. This
Change Set does not copy or replicate Artifacts, implement S3/Google
Drive/OneDrive connectors, store credentials, create a gateway, migrate a
vault, modify the four local vault caches, publish V3 or activate V3 behavior.

Historical V2 `inbox/` references remain where needed as compatibility and
migration evidence. No V3 `inbox/` directory is introduced.

## Acceptance criteria

- `docs/v3-contract.md` defines `meta/` as the V3 operational namespace and
  lists `README.md`, `artifact-index.yaml`, `events/`, `ledgers/`, `audits/`
  and the three queue files;
- Artifact, event, ledger and audit contracts identify their canonical `meta/`
  locations;
- `docs/v3-contract.md` and the crosswalk state that V3 has no `inbox/`
  destination, while preserving historical V2 `inbox/` as explicit migration
  input;
- the provenance index separates compact Record references from rich source
  metadata and excludes credentials and copied source content;
- repository, skill, Change Set, contract, Artifact, ingress, migration,
  inventory and F0 validation passes;
- no real vault, local vault cache, remote object, connector, publication or
  V3 activation is changed.

## Recovery

The change is documentation and contract-only. If rejected, revert the
candidate branch commit; no vault content or external Artifact is affected.
