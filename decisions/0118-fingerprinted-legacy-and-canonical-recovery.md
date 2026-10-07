# 0118 — Fingerprinted legacy migration and canonical recovery

**Status:** Accepted direction for scoped implementation; real items unapproved

**Date:** 2026-10-06

## Context

The four-vault review preserved 338 proposed mappings but did not establish
effective V2.2 conformance or a canonical restoration operation. The operator
selected options 1B, 2A and 3A: implement a direct route for observed legacy,
implement and test canonical recovery, and present one pilot item per vault.

## Decision

Add the explicit `fingerprinted-legacy-v1` source contract to the internal
migration manifest. An unestablished version is represented as `unknown`,
with `source_version_status: not_established`. Require source evidence and
route-decision references, accepted mapping/review/privacy/governance gates,
exact original-body preservation and the complete parsed legacy frontmatter
in `record.legacy_frontmatter`. Malformed or absent YAML headers remain held.
The existing V2 execution route and released compatibility contract are unchanged.

Before a canonical migration write, the gateway asks its persistence adapter
to create an immutable recovery ticket in the same repository's Git
administration. It binds source bytes, expected migrated bytes, proposal,
vault, entity, task branch and originating commit. Add internal
`RecordCrud.recover_migration`, outside the MCP allow-list. Recovery requires
an exact-ticket approval and accepted review, validates hashes and branch
lineage, and atomically restores only those original bytes if the migrated
document has not changed. A later V3 update, moved path, edited ticket, foreign
vault/entity/branch, missing approval or lock blocks recovery without writes.

Reconciliation after interruption distinguishes migrated, source-present and
drifted states. Source-present after a crash is a no-write observation; it is
not proof that a migration or recovery occurred. No automatic reapply follows.

## Rationale

This preserves observed legacy and uncertainty while providing one mutation
boundary and a bounded byte-exact rollback. A schema-specific conversion
contract is not a claim that unknown version means compatible.

## Discarded alternatives

- Relabel content as V2.2: lacks conformance evidence.
- Restore files directly, reset Git or remove uncertain locks: bypasses CRUD
  or destroys unrelated state.
- Permit arbitrary snapshot restoration: exceeds a one-migration ticket.
- Treat operator direction as acceptance of 338 proposals: individual item
  governance, privacy, Collections and mappings remain separate.

## Constitutional and contract impact

Compatible with FF-CON-0001:2.2 and 2.6–2.11, sections 3–4. No constitutional
exception, ACL change, transport, global installation, publication or release.
Change Set 0130 projects this scoped candidate extension. The operator's
choice authorizes preparation and validation, not an unpresented real item.

## Validation

Exercise real Git with synthetic CRLF/Unicode sources, custom legacy fields,
attachments and relationships; migration/reload/recovery in fresh processes;
interruption before/after persistence; wrong ticket/branch/entity, source drift,
edited tickets, later V3 update, locks, rejected reviews and missing gates.
Keep real vaults read-only except administrative pilot proposals/checkpoints.

## Approval

The operator explicitly stated: "Eu autorizo seguir com 1b + 2a + 3A".
The accepted scope is direct-route and recovery implementation plus four pilot
decision sheets. Exact pilot content and all remaining gate evidence are not
accepted by that statement. Review the implemented contract and pilot sheets
before real Record writes; test results do not substitute human authority.
