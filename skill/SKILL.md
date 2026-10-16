---
name: hipocampo
description: >
  Operates an instance of the Hipocampo V3 methodology through the tools and
  adapters available in the current environment. Use for authorized,
  version-aware, multi-vault knowledge operations, CRUD, migration preparation,
  and maintenance rituals. Verify the published package and instance
  compatibility tuple before real-vault operations.
---

# Hipocampo V3 Skill

**Skill package:** `2.0.1`. **Methodology compatibility:**
`^3.0.0`. **Release state:** verify the exact published immutable release, tag target and package hashes; a preparation branch is not a release. The compatibility file's `release_state` records the state when that source snapshot was prepared; it can remain `prepared-unreleased` inside a later published tag. It is not publication evidence and must not override verified release metadata. Require the GitHub Release's `immutable: true`, matching tag target, pinned commit and package hashes before installation; stop if immutability cannot be established. This package preserves the raw
V3.0.0 contract. Later V3 minors and patches must remain compatible with that
baseline, including when an implementation uses an adapter or facade. The AI
host is not part of the version tuple.

Installation makes the client-side instructions available; it does not
activate a vault or prove that the host implements V3 operations. Before using
the skill with a real vault, verify the published release, exact tag-resolved
commit and locked package hashes. Then independently verify the instance tuple,
authorization, privacy/scope and operation-specific tool capabilities. The
released V2 skill remains a separate package and contract.

## Session entry and compatibility

Before a durable operation, follow **[V3 operation and compatibility](references/v3-operation.md)**.
Determine the exact methodology release, skill package and vault declaration;
do not infer content version from a manifest's compatibility range alone.
Continue only when the tuple is compatible and the required authority,
privacy, scope and operation-specific capability checks pass. Treat unknown,
inaccessible or stale version evidence as a blocker or explicitly partial
result.

Keep these questions separate:

1. **Compatibility:** does this skill version support the methodology version,
   and does the vault declare a compatible contract?
2. **Authority and privacy:** may this actor perform this operation for this
   entity, scope and vault?
3. **Tool capability:** does this environment expose the required V3 operation
   through the canonical boundary?

A host name or shared Git provider answers none of those questions by itself.

## Configure the personal anchor

This generic package contains no user-specific vault address or identity
registry. Read **[personalization](references/personalization.md)** and keep
only the personal anchor pointer in host-local state. Discover other
repositories from authorized, current manifests; never store a second router
or infer authorization from discovery or account access.

## Discover vaults and entities

At the start of a session that needs repository context, identify the
requested operation and its entity, knowledge scope and target vaults. Read
only the required manifests and metadata through an available authorized metadata-read capability, separate from RecordCrud.read. Preserve each vault as a separate authority and source.
Shared access, account, Git provider, entity name or similar content does not
join their governance. If actor authorization or a non-empty authorized-vault
set is missing, empty or mismatched, block the V3 read.

For content retrieval, follow the bounded **progressive-disclosure read** in
**[V3 operation and compatibility](references/v3-operation.md#3-progressive-disclosure-read)**.
Do not replace it with a repository-wide body scan or direct filesystem read.

## Run a CRUD operation

Use **[V3 CRUD and read validation](references/crud-frontmatter.md)**. Semantic
review and deterministic validation are separate ordered stages. A semantic
review may return findings or a proposal; only the canonical CRUD gateway may
persist a governed Record change after both required stages pass. Never write
Records directly through a filesystem tool, GitHub contents API, MCP transport,
engine, normalizer, migration routine or host convenience feature.

If the environment does not expose the required canonical CRUD operation with
its actor, reason, expected version, authorization scope and idempotency
context, stop that durable operation. Do not replace it with direct file edits.

## Bootstrap, invitation and repository creation

Keep using the established procedures in
**[instantiation](references/instantiation.md)**, with the V3 operation
boundary above. A repository address is not trusted discovery; confirm its
manifest and declared scope. Any durable registration or Record mutation goes
through the authorized V3 path. If a host cannot perform the required governed
operation, present the plan and report the capability gap without writing.

## Maintenance rituals

Use **[V3 maintenance rituals](references/routines.md)**. Deterministic scans
report reproducible structural findings; semantic interpretation remains a
separate AI review; human approval remains necessary for changes, migrations,
promotion and unresolved authority or privacy decisions. Run one authorized
vault at a time. A request to inspect one scope does not authorize a repository
wide historical sweep.

## Invariants

Read **[V3 invariants](references/invariants.md)** before a consequential
operation. Repository instructions and declared instance contracts outrank
cached skill state. Privacy, entity and vault boundaries, provenance,
uncertainty, reversibility and human authority remain explicit throughout.

## Update this skill

The skill package version is independent from the methodology and host-adapter
versions. Verify a released package against its published release, the tag's
resolved commit and its package lock. Never install from an unverified branch,
self-update, or change client-local files without the operator's confirmation.
The intended package release is `v3.0.1`; verify that its tag and published
release resolve to the same source commit and that every package-lock hash
matches before installation. Pin the resolved commit for the session; a branch
is not a release. Keep operator confirmation, instance compatibility,
authorization and runtime-capability checks separate from package integrity.
