# Change Set 0140 — Vault noun and V3 profile clarification

## Problem and current contract

Decision 0041 already generalized Vault to every governed knowledge repository;
Decision 0074 defined the V3 policy profiles as `entity`, `team` and
`personal`. The active SPEC names both dimensions but does not state their
relationship explicitly. A historical V2 guide still contrasts a general
repository with a confidential "vault" and lacks a prominent version banner.
Four accessible V3-compatible manifests omit `instance.vault_profile`, while
Pearson declares `team` in its local extension. Their older
`curation_level: content | vault` cannot establish a V3 profile.

## Proposed clarification

State Vault as the noun for every Hipocampo knowledge repository and limit the
V3 profile vocabulary to the three existing values. Identify `concepts` as a
subject, scope or historical repository name, never a competing repository
kind. Mark the two V2 guides as historical, update current navigation and
taxonomy, and add negative coverage for obsolete/subject labels in the
existing CRUD validator. No new schema, permission, Record or vault manifest
mutation is introduced. Decisions 0041 and 0074 already authorize the rule;
no new structural choice or Decision Record is needed.

## Compatibility and risk

Legacy `instance.curation_level` and `instance.policy_profile` remain readable
for their original purposes. The compatible V3.0.0 range and prior governed
operations remain intact when a manifest lacks `instance.vault_profile`.
Profile-dependent new operations still require a separately confirmed value
under `docs/v3-to-v3.1-vault-upgrade.md`; no profile is inferred from name,
curation level, older policy profile or repository ownership. Historical
Decision Records and repository names are preserved as provenance.

## Acceptance and recovery

- Current entrypoints, SPEC, V3 vocabulary/CRUD contracts and taxonomy agree.
- V2 guides identify their historical scope without rewriting their contract.
- The deterministic CRUD validator rejects `concepts`, `content` and `vault`
  as V3 profile values while retaining its three accepted values.
- Repository, contract, skill and Change Set validators pass; diff is limited.
- If rejected, revert this documentation and regression case. No real vault
  content, metadata, ACL or installed skill needs rollback.
