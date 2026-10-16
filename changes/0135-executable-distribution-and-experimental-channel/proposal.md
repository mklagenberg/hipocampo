# 0135 — Executable distribution and experimental execution

## Problem

Users can install instructions yet lack a callable CRUD runtime. Stable-only
release rules prevent candidate testing and stale entry points contradict the
published source. A new immutable release must not freeze another incomplete
onboarding flow.

## Proposed change

Implement Decision 0120: methodology 3.1.0, skill 2.1.0, separate local CLI
runtime, explicit experimental channel and optional tag-only RC, structured
warnings, scoped authorization, isolated install and aggregate preflight.
Close all active publication/install documentation before the next final tag.

## Compatibility and migration

Compatible MINOR additions; preserve the 3.0.0 data contract and ^3.0.0
instances. No V3 data migration or private-instance rollout is required.
Scaffold engine/profile identities stay independent. No global installation,
ACL change, automated merge or tag/release creation is included.

## Risks and recovery

Local policy relies on instance filesystem/repository ACLs and is not remote
IAM. Host loading and operations need real observations. Isolated installation
never overwrites a prior installation; incomplete copies remain distinguishable.
Review evidence is external to its operational payload. Never retag a release.

## Acceptance and validation

Real installed RC CLI reaches CRUD/Search with WARNING and successful result;
all engine catalogue checks run through the same channel policy. Invalid
integrity, authorization and contract actions remain blocked. Repository,
package, cross-contract, Change Set and preflight tests must pass. Final human
approval, independent challenge and declared-host evidence remain separate
truthful gates; experimental use does not require those final-only decisions.
