# Change Set 0141 — Explicit V3 Vault profile selection

## Problem and evidence

The V3 scaffold emits no `instance.vault_profile`, although V3 defines only
`entity`, `team` and `personal`. EVL-0205 found four compatible real V3
manifests without the field. A missing declaration in a new Vault and a
missing declaration in an existing compatible Vault cannot share a silent
default. Active bootstrap references still imply that a personal anchor is
required before an authorized entity read.

## Proposed contract

Decision 0124 makes `team` a visible suggested choice at creation, never a
persisted value without an explicit choice and approved plan. Generate the
confirmed field in the V3 scaffold, distinguish creation recovery from legacy
compatibility, and align bootstrap and skill instructions with optional
personal anchors. Preserve old V3 Record and manifest data; any existing-Vault
adoption is a separate scoped review. Keep V2/V2.1 bounded read support.

## Acceptance and evidence

- Three explicit creation choices generate the matching manifest value;
  missing/ambiguous answer and missing confirmation do not create a Vault.
- Existing compatible V3 without the field retains its previous governed
  route with a WARNING; new profile-dependent policy is not inferred.
- An interrupted creation cannot invoke the legacy exception or overwrite
  an existing output; invalid/conflicting declarations are blocked.
- No personal anchor is required for a separately authorized entity read.
- Profile declaration never supplies GitHub/MCP/CRUD permission or Authority.
- Semantic procedure and deterministic selection cases agree; previously
  published use cases receive explicit review for contradictory expectations.
- Manifest, skill, scaffold versions and package lock agree. No real Vault,
  Record, ACL, host installation, tag or GitHub Release is changed by this PR.

## Classification and recovery

Normative, compatible MINOR behavior within the unreleased 3.1.0 methodology
candidate. Bundled skill 2.2.0 → 2.3.0 and scaffold 2.0.0 → 2.1.0 reflect
independent behavior changes. Reject or revert the branch if review fails;
never rewrite a real Vault to rescue a failed candidate.
