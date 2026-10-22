# Bounded read support for V2 vaults

This contract implements `SPEC.md` §2-E and Decision 0121. It does not make a
V2 vault generally compatible with V3. A known V2 vault remains
`migration_required` for V3 operation as a whole; V3 writes require a
separate governed migration. Read support is declared per exact source
release in `OPERATION-SUPPORT.yaml`, with evidence level and host observation
reported independently.

## Entry and source proof

1. Identify the requested vault, repository, entity, knowledge scope and
   operation. Confirm the remote GitHub source and the caller's actual read
   permission through the current GitHub MCP. A local clone is not proof of
   remote permission or currentness. A proto-vault with no remote is a
   separate local boundary.
2. Pin a remote ref/HEAD and obtain version evidence from the vault's
   manifest and its versioned instructions, or an authenticated historical
   source reference. `compatibility: ^2.x` alone does not identify the exact
   source release. Contradictions yield `source_unknown`, never a permissive
   guess. Current adapter entries cover the exact releases V2.0.0, V2.1.0,
   V2.1.1 and V2.2.0; other commits need review and fixtures before support is
   claimed.
3. Confirm the adapter's `validated_synthetic` evidence level, then inspect
   the host/MCP read operation, repository permission, classification and
   privacy grant separately. Verify the immutable published stable release
   before using it in a warning; the experimental candidate is separate. A
   catalog entry is no technical permission.

## Privacy before body retrieval

Select a bounded path using trusted metadata. The V2 `visibility` field is
`public`, `internal`, `confidential` or `restricted`; missing or ambiguous
labels fail closed. GitHub repository read access ordinarily suffices for
methodological presentation up to `internal` when the source class is proven.
`confidential` and `restricted` need a specific methodological grant.

GitHub Contents-style MCP calls may return a whole file rather than only its
header. The local parser can prevent *presentation* after parsing but cannot
undo transport of protected bytes into a host. Before such a fetch, require a
trusted path/classification boundary or other authorized metadata that proves
the candidate is within the actor's allowed class. If unavailable, return a
metadata-only/blocked result and identify the missing capability. Do not
claim that a post-fetch privacy check was a pre-retrieval gate. Do not bypass
this boundary with a local cache.

## Deterministic and semantic paths

The pure Python adapter in `scripts/v2_legacy_reader.py` accepts only bytes
already supplied by a trusted, authorized transport. It verifies the exact
source-release entry, bounded UTF-8 YAML frontmatter, classification, source
ref and selected path. It returns the original fields and prose without
creating a V3 Record or changing the vault. This parser is not a GitHub MCP
transport or an authorization service. Synthetic fixtures test its logic;
they do not prove host exposure or a real-vault read.

When Python cannot run, the agent follows the same steps through an available
GitHub MCP: verify source and ref; inspect metadata and pre-retrieval privacy;
select one authorized file; interpret V2 fields under the source contract;
withhold unknown/high-class bodies; preserve original fields and provenance;
return a visible version WARNING. If any invariant cannot be met, return a
typed unavailable or partial result. Semantic instructions and script outputs
must agree for their shared cases; neither path is mandatory where it cannot
be supported. The shared-case review and unresolved boundaries are recorded in
the [parity review](legacy-read-parity.md).

## Result and warning

Report general compatibility, declared adapter support, actual operation
outcome, source version/ref/commit, repository/path, classification, limits
and any unchanged source fields. WARNING identifies the verified old version,
current published stable reference, read-only scope and V2-to-V3 migration
needed before V3 writes. An experimental candidate creates a separate notice;
it does not make a published stable version retroactively old. Never imply a
specific vulnerability merely from age. Recheck the ref if it changes before
the body is presented. Keep results isolated by vault and entity.

The pure `scripts/vault_version_notice.py` helper tests the age comparison for
both V2 and V3. Its caller must first prove the source version and immutable
published stable reference; the helper's inputs do not authenticate either.
For a V3 source older than stable, emit a proportional upgrade WARNING while
keeping the V3 compatibility result separate. When the source equals the
published stable version, an experimental candidate alone creates no age
WARNING.

## Recovery and host proof

On unsupported version, unvalidated adapter, missing MCP read, denied GitHub
access, unresolved privacy, changed ref or parser failure, disclose no body.
Retain a small diagnostic with cause and next step. Observe Claude, Copilot in
VS Code and Codex/ChatGPT separately before claiming their host support.
