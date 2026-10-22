---
name: hipocampo
description: >
  Operates an instance of the Hipocampo V3 methodology through the tools and
  adapters available in the current environment. Use for authorized,
  version-aware, multi-vault knowledge operations, CRUD, migration preparation,
  and maintenance rituals. Verify the selected source channel and instance
  compatibility tuple before real-vault operations.
---

# Hipocampo V3 Skill

**Skill package:** `2.4.0`. **Methodology compatibility:**
`^3.0.0`. **Execution channel:** stable is the default and requires the exact
published immutable release, tag-resolved commit and package hashes.
Explicit experimental execution verifies a pinned source commit/inventory;
a candidate or RC tag needs no GitHub Release or future stable publication.
Emit WARNING and allow valid engine operations. Publication/final-review
pending states do not block experimental execution. Integrity, authorization,
privacy and actual contract failures still block the affected action.
See [runtime and channels](references/runtime.md). This package preserves the raw
V3.0.0 contract. Later V3 minors and patches must remain compatible with that
baseline, including when an implementation uses an adapter or facade. The AI
host is not part of the version tuple.

Installation makes the client-side instructions available; it does not
activate a vault or prove that the host implements V3 operations. Before using the skill with a real vault, verify the chosen channel and pinned
source, full distribution integrity, compatible instance tuple and operation
capability/authorization. Stable verifies immutable publication; explicit
experimental use emits WARNING and does not wait for the future stable tag.

## Session entry and compatibility

Before a durable operation, follow **[V3 operation and compatibility](references/v3-operation.md)**.
Determine the selected methodology version/source, skill package and vault declaration;
do not infer content version from a manifest's compatibility range alone.
Continue only when the tuple is compatible and the required authority,
privacy, scope and operation-specific capability checks pass. Treat unknown,
inaccessible or stale version evidence as a blocker or explicitly partial
result.

For a **V2 read request**, use the separate bounded
[legacy read procedure](references/legacy-read.md). General compatibility
remains `migration_required`; a validated read adapter is operation support,
not V2/V3 compatibility. Do not route V2 through V3 RecordCrud or use the V3
compatibility result alone to deny an otherwise proven read-only adaptation.

Keep these questions separate:

1. **Compatibility:** does this skill version support the methodology version,
   and does the vault declare a compatible contract?
2. **Authority and privacy:** may this actor perform this operation for this
   entity, scope and vault?
3. **Tool capability:** does this environment expose the required V3 operation
   through the canonical boundary?

A host name or shared Git provider answers none of those questions by itself.

## Discover a vault

This generic package contains no user-specific vault address or identity
registry. Keep only an optional personal anchor pointer in host-local state.
Use [personalization](references/personalization.md) for that path and direct
invitations. Without an anchor, use bounded candidate discovery and verify
the current remote target; do not require a personal Vault for authorized
entity reading. An address, repository listing or local hint is neither a
permission grant nor a complete Vault inventory.

## Discover vaults and entities

At first use, on entry to a new vault or entity, or after a change of account,
skill or connector, run the operation-level diagnostic in
**[V3 operation and compatibility](references/v3-operation.md)**. Identify the
requested operation, entity, scope and exact repository. Use GitHub MCP to
confirm the actor, remote manifest and permission for that repository. A
confirmed repository read permits Hipocampo presentation up to `internal`
without a prior vault registration or personal anchor. Higher classifications
need the vault's separate clearance proof. Shared access does not join vault
governance or confer writing or epistemic authority.

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

When Python is available, use the compatible canonical engine. Otherwise
follow the semantic CRUD procedure and perform the same required reproducible
checks with GitHub MCP evidence. If a required check or transport operation
cannot be performed, stop only the affected durable action. The MCP's file
functions are transport inside CRUD, never a shortcut around it.

## Bootstrap, invitation and repository creation

Keep using the established procedures in
**[instantiation](references/instantiation.md)**, with the V3 operation
boundary above. A repository address is a candidate, not an authorization;
confirm its manifest and declared scope. Joining an entity vault for read does
not require a personal anchor. Any durable registration or Record mutation
goes through its authorized V3 path. If a host cannot perform the required
operation, present the plan and report the exact capability gap without writing.

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
For Claude, Copilot/VS Code and Codex/ChatGPT, follow the selected host's
supported install/update surface and `docs/host-installation.md` in the
verified distribution. Updating the client never migrates a vault. Record package,
runtime, GitHub MCP and vault versions separately.
The stable target is `v3.1.0`; a target declaration is not publication proof.
For an explicitly requested experimental install, use the pinned snapshot and
full distribution hashes instead of demanding the future stable release.
Never silently change an installed version or overwrite a previous install.
