# V3 bilateral ledger and deterministic audit contract — unreleased candidate

This document defines the deterministic transparency and traceability boundary
for the unreleased V3 Package candidate. It does not decide semantic truth,
applicability, conciliation, or curation.

## Paired local ledgers

When persisted locally, the ledgers belong under `meta/ledgers/`. Their
logical streams are:

- `packages-sent` in the generating/source vault;
- `packages-received` in the destination vault.

Every governed delivery creates two local events when both sides are available:

- `packages-sent` in the generating/source vault;
- `packages-received` in the destination vault.

The entries are paired by `delivery_id`, `package_id`, `package_version`, and
`fingerprint`. The source entry proves that a Package was assembled and sent;
the destination entry proves that the same Package was received and records its
local acceptance and Record representation. Both events record `recorded_by`
and `recorded_at`, so an investigation can identify who performed the
circulation operation and when it was recorded.

The ledger is an operational transparency record, not a second knowledge
source. Content remains in the Package, Record, Chunk, or Artifact referenced by
the ledger entry.

## Local received representation

Receipt creates a local representation with:

```yaml
processing_state: new
curation_status: pending_rem
```

The representation is not curated knowledge and cannot be treated as current
use until REM, validation, and any required semantic reconciliation complete.
The immutable Package remains the delivery envelope and carries origin,
authority snapshot, destination, selection, and fingerprint context.

## Audit dimensions

The deterministic auditor reports independent dimensions:

```yaml
coverage: complete | partial
integrity: valid | mismatch | broken
circulation: confirmed | sent_unconfirmed | received_orphan
governance: accepted | revoked | revalidation_required
```

An inaccessible or unregistered vault creates a `partial` coverage frontier.
It does not prove revocation or invalidate an otherwise accepted, intact
Package. Missing bilateral entries are alerts. Fingerprint, source/destination,
selection, or authorization mismatches are deterministic failures.

The auditor follows provenance backward and circulation forward. It can begin
at any accessible local Record and reports the oldest verifiable origin rather
than claiming an absolute origin beyond an unavailable frontier.

## Privacy boundary

Ledger visibility follows content visibility: a User with access to a Record
may inspect its relevant circulation trail, while unrelated entity and vault
metadata remain outside that user's view. Entries minimize content duplication
and preserve identifiers, purpose, destination, selection, versions, and
fingerprints needed for a later investigation.

Revocation and privacy incidents create durable control events or tombstones,
preserve the trace, and block current use according to the destination
contract. They do not silently erase the circulation history.

## Verification boundary

`scripts/v3_audit_engine.py` proves graph references, bilateral pairing,
fingerprints, selection and access frontiers in memory. It cannot prove remote
authorization, transport security, semantic truth, actual host permissions,
or that a human's semantic decision was correct.
