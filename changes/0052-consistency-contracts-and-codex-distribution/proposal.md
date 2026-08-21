# Change Set — 0052: consistency contracts and Codex distribution

## Summary

Resolves cross-surface contradictions left after v2.0.0: defines anchor registration, introduces unambiguous manifest names for curation and sensitive-data policy, completes invariant 6 in the skill, removes retired-router guidance, adds the first canonical Codex adapter, and adds deterministic contract validation.

## Class

**normative and operational** — the manifest and discovery contracts gain backward-compatible capabilities, while the skill, scaffold, validation, and distribution package are synchronized.

## Semver

**minor** — existing v2 instances remain valid. `instance.tier` and the legacy `AGENTS.md` declaration remain readable; new instances emit the unambiguous fields and upgrading is recommended, never automatic.

## Risks and recovery

The new fields could be mistaken for a required immediate migration. The specification, upgrade guide, and validator therefore distinguish accepted legacy input from newly generated output. If a host adapter proves unsuitable, it can be superseded without changing the portable core or a content instance.

## Acceptance criteria

- Fresh scaffold manifests use `curation_level` and `policy_profile`, never `instance.tier`.
- A direct invite can be registered only after target-manifest read and explicit confirmation.
- The skill, manifest, and Codex adapter declare compatibility and local anchor state consistently.
- All repository, skill, Change Set, and contract validators pass locally and in CI.

## Status

`implemented` — delivered by the PR that contains this Change Set.
