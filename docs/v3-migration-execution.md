# V3 migration execution — unreleased candidate

This procedure describes the deterministic executor for an explicitly mapped
V2.2-to-V3 migration. It does not activate V3, create semantic mappings, prove
privacy, or authorize any vault by itself.

## Responsibilities

- The operator and semantic reviewer decide how each source Record maps to a
  complete V3 Record. Ambiguous fields, splits, merges, entity, scope,
  authority, visibility, maturity, Collections, Chunks, and Artifact or Package
  lineage cannot be inferred by the executor.
- The migration manifest carries the reviewed proposal, references to the
  mapping and privacy assessments, and the exact source fingerprints. It is
  vault-local operational input and may contain governed Record content.
- `v3_migration_executor.py` checks the manifest and source, supports a
  no-write dry run, and submits each approved proposal to `RecordCrud.migrate`.
- `RecordCrud` validates the complete Record and accepted semantic review, then
  invokes `MarkdownRecordStore`. The store compares the source hash and replaces
  that one Markdown file atomically in the same directory.
- `RecordCrud.create` and `RecordCrud.update` use the same storage boundary for
  later V3 writes. A new gateway instance can load and validate existing V3
  Records from Markdown before serving reads or updates.

## Required manifest

The manifest is a YAML mapping with these fields:

```yaml
source_version: "2.2.0"
target_version: "3.0.0"
mapping: complete
privacy: proven
rollback: tested
target_contract: verified
human_approval: present
approved_vault_id: "exact-vault-id"
vault_id: "exact-vault-id"
approval_scope: "v2.2-to-v3-branch-local"
approval_ref: "review-or-approval-reference"
source_inventory_sha256: "64 lowercase hexadecimal characters"
semantic_review_status: complete
unsafe_raw_fallback: false
execution_state: not_started
actor: "authorized-operator-id"
active_collections:
  collection-id: {collection_id: "collection-id", active: true}
records:
  - source_path: "records/stable-id.md"
    source_sha256: "64 lowercase hexadecimal characters"
    mapping_ref: "vault-local-mapping-reference"
    privacy_review_ref: "vault-local-privacy-review-reference"
    semantic_review: {review_id: "...", target_id: "...", reviewer: "...", purpose: "...", evidence_refs: ["..."], rationale: "...", reviewed_at: "...", decision: accepted}
    reason: "approved V2-to-V3 transformation"
    idempotency_key: "vault-id:record-id:v3-migration"
    record: {complete: "V3 Record proposal matching the source_path"}
```

`source_inventory_sha256` is checked against the sorted `(source_path,
source_sha256)` entries in the manifest. This proves that the manifest entries
were not accidentally changed after fingerprinting; it does not prove that the
manifest includes every migratable document in the vault. The separate vault
inventory and completed resolution matrix remain required.

The executor does not print Record content, frontmatter values, paths, or
Record identifiers in its summary. It reports counts and a bounded gate status.

## Commands

Run the dry run first:

```powershell
python scripts/v3_migration_executor.py --vault-root <vault-repository> --manifest <vault-local-manifest.yaml> --mode dry-run
```

Only after the dry run is reviewed, execute on that vault's dedicated branch:

```powershell
python scripts/v3_migration_executor.py --vault-root <vault-repository> --manifest <vault-local-manifest.yaml> --mode apply
```

`apply` requires the repository root itself, a branch beginning `migration/`,
the branch to include local `main`, a clean working tree, exact-vault approval,
complete mappings and reviews, a verified destination, and tested rollback.
Each Record replacement is atomic. A whole-vault batch is not one filesystem
transaction: if execution stops after some Records, the branch contains that
partial state and the executor blocks another apply. Do not reset or discard
it automatically. Recovery must first inspect the branch and use the approved
rollback or recovery procedure; the main branch remains unchanged.

The request idempotency key prevents duplicate effects when the same request
is repeated inside one live CRUD process. It is not a cross-process recovery
token; the clean-branch and `execution_state: not_started` gates still block a
new apply after an interruption.

The input's approval and review references are declarations checked for
completeness and scope by the script. The script does not authenticate those
references or determine whether a semantic review is correct. It also does not
prove that an external artifact is accessible, that the remote vault is current,
or that a human has accepted the resulting Git diff. Those checks remain
separate gates under `MIGRATIONS.md`.

## Current execution boundary

### Explicit observed-legacy route and canonical recovery

Decision 0118 defines an additional scoped source contract. Its manifest uses
`source_contract: fingerprinted-legacy-v1`, `source_version: unknown`,
`source_version_status: not_established`, `source_contract_status: accepted`,
`source_contract_approval_ref`, `source_evidence_ref`, and
`approval_scope: fingerprinted-legacy-to-v3-branch-local`. It also carries
non-empty repository-relative `context_files` mapped to exact SHA-256 hashes.
An absent `profile.md` may be explicitly represented by `absent`; its absence
is evidence, not a fulfilled profile or governance requirement. Appearance of
that file invalidates the context binding until reconciliation.
Each entry binds `source_context_sha256` to the canonical context map hash and
provides `legacy_source_evidence_ref`. The complete initial Record preserves
the exact body in `content`, every parsed original field in
`legacy_frontmatter` and the original hash in `legacy_source_sha256`.
Malformed, absent or V3 headers are held; this is not a raw-content fallback.
All mapping, privacy, governance, Collection, semantic review, destination,
branch and tested-recovery gates remain mandatory.

Before its atomic replacement, canonical CRUD creates an immutable ticket
under the originating repository's Git administration directory. Ticket
identity and hash are an operational receipt, never an approval by themselves.
After interruption, inspect the ticket and actual bytes before another action.
`RecordCrud.recover_migration` requires exact ticket ID/hash, vault/entity,
`human_approval: present`, `approval_scope:
canonical-migration-recovery-branch-local`, `approval_ref`, `procedure_ref`,
and an accepted semantic review. Only an unchanged initial migration result
can be restored. Later version, target drift, ticket drift, branch/lineage
change or a surviving lock blocks it. Unrelated dirty files remain untouched.

Recovery returns `restored` after a verified atomic byte-exact replacement, or
`source_present_no_write` when the source bytes are already present. The latter
does not prove any migration or recovery happened. Retained tickets block
same-source reexecution, even after restoration; a new attempt needs its own
governed procedure. These internal operations remain outside the MCP surface.

The route and recovery are tested with synthetic content and actual Git.
Their results do not establish real-vault privacy, authority, item approval,
or a completed real pilot. The existing V2 execution mode remains available
with its original gates.

The executor and Markdown store have been run only against sanitized synthetic
Git fixtures. No real-vault migration manifest with complete mappings,
privacy reviews, and rollback evidence exists in this candidate. Running
against the four real vault branches without such a manifest must return
`mapping_manifest_required` and write nothing.
