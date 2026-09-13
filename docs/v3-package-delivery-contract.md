# Hipocampo V3 selective Package delivery — unreleased candidate

This document defines the selective Package, authority, conciliation and
revalidation boundary for the unreleased V3 candidate. It does not activate V3
for existing v2 instances.

## Separate authorities

V3 keeps these concepts separate:

- `source_authority`: authority over the knowledge within one entity and scope;
- `package_authority`: the vault that generated the specific Package version;
- destination authority: the contract that accepts or rejects the delivery.

The Package never transfers source authority. Its ledger entry records whether
the Package was sent or received, its generator vault, source and destination
entities, purpose, and conciliation state.

## Authority succession

An authority chain is ordered for one entity and scope. Resolution selects the
first eligible authority accessible to the operation, using the hereditary
order without persisting active/inactive state in Records or vaults. Loss of
access selects the next pre-authorized successor; it never creates a parallel
authority. An empty, invalid, or fully revoked chain blocks current-use
delivery. An inaccessible origin after an accepted Package creates a partial
audit frontier and does not by itself invalidate local use.

## Conciliation

The allowed relation states are:

- `equivalent`;
- `complementary`;
- `update`;
- `entity_specific`;
- `unresolved_conflict`;
- `irreconcilable_perspectives`.

All participating sources remain referenced. Conflicting positions stay in
separate Chunks, or in separate Records when entity or scope boundaries differ.
No Package may hide the conflict in an aggregated text.

## Package purpose gate

- `discussion`, `review`, and `analysis` Packages may carry explicit conflict;
- `current_use` Packages block unresolved conflict;
- `irreconcilable_perspectives` may be used only when the destination
  explicitly accepts multiple perspectives;
- stale or revalidation-required material cannot be delivered for current use;
- a Package without resolved source authority or package authority is blocked.

After delivery, revalidation compares Record identity, source staleness,
authority resolution and conciliation state. A revoked authority, stale source
or changed conciliation invalidates the Package for current use and requires a
new governed assembly. An inaccessible but not revoked authority is recorded as
an audit frontier and may continue locally when the Package is intact and
accepted.

Delivery remains selective. It does not alter source maturity, epistemic
nature, authority, or Record content.

## L4R closure: logical authority, local receipt and audit

Authority is resolved by `entity + scope + origin` in the operation context. A
vault or Record does not persist `active`/`inactive` access state. An origin
that is unavailable to the current operation creates a partial audit frontier;
it is not automatically revoked.

The Package carries a compact origin and authority snapshot, the generating
vault identity, destination, selected Chunks and Artifacts, and a deterministic
fingerprint. The generating vault is authoritative for that Package version;
this does not transfer authority over the source knowledge to the destination.

Receipt creates a destination-local Record in `processing_state: new` and
`curation_status: pending_rem`. The local representation must pass REM before
being treated as curated or current knowledge.

Every delivery is represented in both local `packages-sent` and
`packages-received` ledgers. The deterministic audit crosses these entries and
reports coverage, integrity, circulation, and governance separately. Missing
counterparts are transparent alerts; fingerprint, destination, selection, and
authorization mismatches fail closed. Each ledger event records who and when
(`recorded_by` and `recorded_at`). Semantic conciliation, applicability,
split and curation remain human or agent-reasoned decisions recorded by the
deterministic ledger, not replaced by it.

The full ledger and audit contract is in
`docs/v3-ledger-audit-contract.md`.

## Validation boundary

`scripts/v3_package_engine.py` and
`scripts/validate_v3_package_delivery.py` exercise the contract in memory.
They do not prove remote authorization, transport, migration, semantic truth,
or universal host enforcement.
