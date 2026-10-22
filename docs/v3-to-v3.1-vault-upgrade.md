# V3.0.0 vaults with the 3.1.0 methodology candidate

This procedure applies to a vault whose current, authorized remote manifest
declares `hipocampo.compatibility: ^3.0.0`. Methodology 3.1.0 preserves the
V3.0.0 Record, Chunk, frontmatter and CRUD baseline; skill 2.2.0 is a separate
client package. The version range covers 3.1.0, so a compatible vault needs
no Record conversion or manifest rewrite solely to use this candidate.

## Before selecting the new source

1. Read the target vault's `AGENTS.md`, `hipocampo.yaml` and local operation
   policy from the authorized GitHub repository at a recorded `main` commit.
   Check the declared entity, role, scope and any stricter local rule. A cache
   or a known repository address is not evidence of current remote state.
2. Choose the methodology channel. Stable requires the published immutable
   release, tag-resolved source and exact hashes. Until publication, explicit
   experimental use requires a pinned commit and verified distribution; emit
   the candidate WARNING. Never silently select mutable `main`.
3. Verify the independent skill version and package lock. Updating the client
   skill/plugin does not update a vault, and a vault's historical
   `skill.generated_by_version` records scaffold provenance, not the operator's
   installed skill. Do not replace that field with 2.2.0.
4. Evaluate the actual methodology/skill/vault tuple with
   `COMPATIBILITY.yaml` and `scripts/validate_compatibility.py`, using the
   remote manifest bytes and the selected source channel. A compatible result
   is a contract result, not proof of repository permission, host/MCP
   capability, actor authority, privacy clearance or a successful CRUD call.

## Preserve historical verification

Keep `hipocampo.verified_against: 3.0.0`, its verified commit and pinned
V3.0.0 links as the truthful evidence of the previous vault validation.
Do not change them to 3.1.0 merely because `^3.0.0` matches. Existing
instance validators may pin hashes of the V3.0.0 methodology source; run
those validators only against their recorded source. Their rejection of a
different source is not evidence that the vault's data contract is
incompatible. A new verification claim needs its own exact-source test and
review before changing durable provenance.

## Operate progressively

- Preserve all Records, Chunks, frontmatter, Collection membership, original
  sources and legacy content. No bulk rewrite or migration is caused by this
  compatible minor update. Continue local restrictions, including vaults
  intentionally limited to historical reading.
- For each actual operation, check GitHub MCP availability, repository
  permission, the actor's methodological eligibility, the vault's local policy
  and the canonical engine capability. Record writes still use RecordCrud.
  A compatibility result cannot grant a provider permission or authorize a
  write. A bounded V2 read remains operation support, not V3 compatibility.
- Compare a proved vault source version with the verified published stable
  version for the separate age WARNING. An unpublished 3.1.0 candidate is
  not a published stable reference. A WARNING does not itself demand migration.
- If a specific new operation fails, record the failing layer and evidence.
  Change only the affected contract in a scoped, reviewed vault branch after
  authorization; do not widen ACLs, move content or edit governed Records to
  make a version check pass.

## Verification record

Record the repository and `main` SHA, manifest blob SHA, selected methodology
commit and channel, skill version and package-lock hash, compatibility result,
local-policy findings, operation-specific checks and limitations. A manifest
test does not certify the entire Record corpus or a real host session. Keep
each vault's evidence separate. Publication of 3.1.0, client installation
and any later `verified_against` update are distinct decisions.
