# 0052 — Consistency contracts, anchor registration, and Codex distribution

**Status:** Accepted

## Context

Version 2.0.0 established repository-side discovery and the sixth invariant, but the operational surfaces did not fully converge. The skill still omitted invariant 6; `UPGRADE.md` still instructed operators to maintain the retired router; the manifest used `tier` for curation level while the specification used the same word for exposure; and `AGENTS.md` duplicated a policy-relevant field without a canonical manifest location. The discovery procedure also required an anchor manifest to enumerate reachable repositories without defining the registration structure that makes this possible, especially after a direct collaborator invitation.

The repository now also has CI and deterministic structural validation, but no check that these cross-surface contracts stay aligned. Codex remains a valid platform-agnostic host but has no canonical, versioned adapter in the published skill.

## Decision

1. `SPEC.md` is the normative contract; Decision Records record durable rationale and decisions; all other repository artifacts are derived operational projections. A projection may add host-specific procedure, but may not weaken or contradict the specification or an accepted Decision Record.
2. Every anchor manifest may declare `discovery.registered_repositories`, a list of repository addresses already confirmed by the operator. The list carries addresses only. The agent reads each target manifest for `entity`, `role`, and scope; it never mirrors those fields into the anchor and no target vault points at siblings. Adding an address is a gated registration action after the target manifest has been read and the user has explicitly confirmed it.
3. The irreducibly local pointer to the first anchor is stored only in client-local state. The portable core names the field `anchor_repository`; each host adapter declares its local storage mechanism. It is not committed to a vault and is not a repository router.
4. `instance.curation_level` (`content | vault`) replaces the ambiguous `instance.tier` for newly generated manifests. Existing `instance.tier` remains accepted as a deprecated compatibility alias until the next MAJOR release. Exposure tier remains a separate repository-naming concept.
5. `instance.policy_profile` (`personal | corporate`) becomes the sole machine-readable selector for the sensitive-data policy. It replaces the duplicate `AGENTS.md` “Instance type” field for new instances. Existing instances remain readable from that legacy declaration until upgraded.
6. The canonical skill is version 1.1.0 and supports Hipocampo ^2.1.0. Its portable core remains host-neutral; Codex is added as a thin, declared adapter with local-state and update behavior.
7. Deterministic validation checks the consistency of these contracts across the specification, scaffold, skill, manifest, and repository disclosures.

## Rationale

This keeps discovery authoritative without restoring a client-side router: the anchor stores only operator-confirmed addresses, while each reachable repository remains authoritative for its own declaration. Separating curation level from exposure tier removes a field-name collision without invalidating existing manifests. `policy_profile` preserves the safety decision that used to depend on “Instance type” while eliminating duplicate repository-side declarations, which invariant 6 explicitly forbids.

The adapter makes Codex support explicit without making the methodology dependent on one host product. Cross-surface validation makes the methodology's actual operational package auditable rather than relying on manual recollection after a release.

## Discarded alternatives

- **Restore a router or identity table in the installed skill.** Discarded because it would recreate a client-side second source of truth.
- **Derive policy from `entity` and `role`.** Discarded because those fields do not distinguish every personal, family, and corporate entity safely.
- **Rename `instance.tier` and reject it immediately.** Discarded because it would make already-valid v2 manifests incompatible and require a MAJOR release.
- **Treat Codex as implicitly supported because the methodology is platform-agnostic.** Discarded because host limitations and local-state behavior must be declared to be operable and auditable.
