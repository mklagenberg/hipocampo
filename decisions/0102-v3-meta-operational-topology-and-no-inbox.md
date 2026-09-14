# 0102 — V3 `meta/` operational topology and no-inbox boundary

**Status:** Accepted for the unreleased V3 candidate

## Context

The V3 candidate already defines Artifact provenance, operational events,
paired delivery ledgers, scoped audits and three maintenance queues. Their
logical contracts existed, but the vault-local persistence boundary was not
declared in one place. That omission makes it unclear where an Artifact index,
an audit trail or a queue belongs, and leaves the historical V2 `inbox/`
terminology easy to misread as a V3 directory.

## Decision

Use `meta/` as the canonical operational metadata namespace of every V3 vault.
It contains or owns the following surfaces:

- `meta/README.md` — explanation of the local operational namespace;
- `meta/artifact-index.yaml` — provenance index for original Artifact versions
  used as references;
- `meta/events/` — durable, bounded operational events;
- `meta/ledgers/` — local `packages-sent` and `packages-received` delivery
  ledgers;
- `meta/audits/` — scoped audit indexes and detailed violation/control
  records;
- `meta/fila-frontmatter.yaml` — deterministic frontmatter findings;
- `meta/fila-staleness.yaml` — deterministic staleness findings;
- `meta/fila-semantica.yaml` — semantic, privacy, routing and conflict
  findings.

The namespace is operational metadata, not a second knowledge base. `registry.md`
continues to address cross-vault aliases and repositories; it is not replaced
by the Artifact index. Artifact records in knowledge remain compact references
to `artifact_id`, version and role, while the index holds the richer original
name, path or URI, source kind, hash, author, dates, accessibility, visibility
and limitations when known.

The index preserves traceability of the original Artifact only. It does not
copy bytes, create a local mirror, fetch from S3/Google Drive/OneDrive, or
grant authorization. Credentials and tokens never belong in `meta/`. A future
replication or storage gateway is a separate capability.

V3 has no `inbox/` directory. Raw or sensory capture remains outside the
durable vault; processed ingress admits minimized, redacted and authorized
material, including material that begins with `processing_state: new`. A V2
`inbox/` is preserved as historical source context and may be considered only
through an explicit migration or ingress plan. This decision does not rename,
delete, copy or migrate existing V2 content.

## Rationale

One namespace makes operational metadata discoverable without mixing it with
knowledge content. Separating the index from Record bodies avoids repeating
provenance while preserving investigation paths. Declaring no V3 `inbox/`
removes the ambiguity between historical short-term memory and the processed
ingress boundary, without destroying migration evidence.

## Consequences

- New V3 vault topology documentation and scaffolding must point operational
  metadata to `meta/`.
- Event, ledger and audit contracts can choose file granularity locally, but
  their durable records remain under the declared namespace.
- Historical V2 `inbox/` references remain searchable as history and migration
  input; they are not evidence that V3 creates an inbox.
- Artifact traceability can be inventoried without implementing a connector or
  replication service.
- Existing vaults require a separate migration Change Set before adopting V3
  topology; this decision does not perform that migration.

## Discarded alternatives

- Keeping each metadata class at an unrelated repository root was rejected
  because it makes the operational boundary hard to discover and audit.
- Reusing `registry.md` for Artifact provenance was rejected because aliases
  and Artifact versions have different identity, lifecycle and privacy needs.
- Retaining `inbox/` as a V3 destination was rejected because V3 requires
  processed ingress and must not turn the vault into a raw capture store.
- Copying referenced Artifacts into `meta/` was rejected because this scope is
  original-source traceability, not replication or storage management.

## Validation plan

- Confirm the V3 contract lists every canonical `meta/` surface and explicitly
  excludes `inbox/` from V3 topology.
- Confirm Artifact, event, ledger and audit contracts point to their `meta/`
  namespaces.
- Confirm the V2-to-V3 crosswalk labels `inbox/` as historical input only.
- Run the repository, skill, Change Set, contract, Artifact, ingress,
  migration, inventory and F0 validators.
- Verify no local vault cache or real vault is changed by this Change Set.
