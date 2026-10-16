# Hipocampo — release checklist

This checklist implements Decisions 0014/0021/0023/0037 and 0120. Use one
cohesive Change Set, not a publication loop that leaves essential work afterward.

## Before the final tag

- [ ] Classify public impact and independent methodology/skill/runtime versions.
- [ ] Synchronize SPEC, decisions, taxonomy/vocabulary, README, changelog,
  COMPATIBILITY, skill manifest/references, scaffold and upgrade/migration guidance.
- [ ] Install the complete distribution in isolation; preserve the previous install.
- [ ] Exercise actual entrypoint and canonical engines. Explicit experimental/RC
  execution emits WARNING and completes valid operations without a GitHub Release.
- [ ] Preserve failure controls for integrity, actual compatibility and authorization.
- [ ] Verify new-session use, recovery, dependency install and declared host modes.
- [ ] Justify any actual RC tag by an additional test; otherwise issue no RC.
  RC can be tag-only and requires neither final approval nor future stable tag.
- [ ] Freeze/test operational payload and bind independent AI/human review to its
  digest outside that payload. Never embed the payload's own final hash in itself.
- [ ] Verify PR integration on main and correspondence to the tested fingerprint.
- [ ] Run repository/package/contracts, complete engine suite and differential
  Change Set checks. Run the aggregate final preflight with external review receipt.
- [ ] No known essential documentation, manifest, runtime or readiness gap remains.
- [ ] Draft includes every distribution asset, inventory/checksums, receipt and
  final notes. The exact English human form is generated only when gates pass.
- [ ] Reconfirm exact resolved commit/tag absence, protection settings and future
  release immutability before the human creates the stable tag and GitHub Release.

## After publication

Verify the actual tag, resolved source, attached bytes/hashes, channel and
immutable:true through the consumer path. Use provider release/asset verification
where applicable; generated source archives are not attested attached assets.
This confirms the prepared distribution; it is not the moment to finish README,
change a manifest or implement a missing adapter. Fix newly discovered file
defects in another version, never move/reuse the old identity. Editable release
notes do not repair immutable files.

## Channels and repetition

Default stable requires verified immutable publication before installation.
Explicit experimental use pins source/inventory and treats final-readiness gaps
as warnings, preserving all operation gates. Signed/annotated tags and tag rules
have distinct identity/protection properties; tag-only RC is not an immutable
GitHub Release. Human merge/tag/release control remains applicable.

Rerun checks affected by source, dependency, policy or instruction drift. If a
change is strictly external evidence and digest remains identical, do not repeat
unrelated work by habit. No final gate depends on the future tag it authorizes.
