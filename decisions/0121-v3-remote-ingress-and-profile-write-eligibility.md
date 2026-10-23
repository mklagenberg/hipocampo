# 0121 — V3 remote ingress, profile write eligibility, and runtime-independent CRUD

**Status:** Proposed for the 3.1.0 release target

## Context

The V3 contract's discovery and Bootstrap wording can make a personal anchor
appear mandatory, although direct repository access can already identify a
target. Profile descriptions also say they grant no write access without
defining the distinct policy eligibility introduced for `personal` and `team`
by accepted management direction. Finally, a Python-first implementation can
mistake one validator runtime for the CRUD boundary, while direct writes would
violate the Constitution's canonical CRUD rule.

## Decision

1. A personal anchor and `discovery.registered_repositories` are optional
   discovery aids. A user may identify a target directly; the target's current
   manifest and operation-specific authorization remain authoritative.
2. GitHub MCP is the preferred remote operation surface when it exposes the
   required operation. Tool presence, read access, Git write permission,
   methodological eligibility, execution and durable confirmation are distinct
   facts. No one fact implies another.
3. New or adopted vault manifests declare `instance.vault_profile` as
   `personal`, `team` or `entity`, independently from
   `instance.policy_profile`. Confirmed read access to a `personal` or `team` vault grants methodological
   eligibility to propose Create, Update and Archive only within that profile's
   declared scope. Execution additionally requires GitHub write, matching MCP
   capability, canonical CRUD validation and a durable receipt. An `entity`
   vault remains read-only unless a current scoped grant is recorded in
   `governance.authorized_representatives`, bound to the stable authenticated
   account identifier, `instance.vault_id`, entity, actions, scope,
   `valid_from` and `valid_until`; null end means no scheduled expiry, subject
   to revocation. The bounded actions are `create`, `update`, `archive` and,
   when separately authorized, `manage_representatives`. Only the latter
   permits delegation or revocation. New or explicitly adopted vault manifests
   declare immutable `instance.vault_id`, independent of repository address.
   Legacy manifests retain the prior versioned authorization and CRUD rules
   until adoption; this does not infer a profile or confer new eligibility.
   Governed adoption is required before recording a new representative grant
   on a legacy vault.
   For an authorized read of a compatible legacy manifest without
   `instance.vault_id`, the current `meta/v3-collections.json` may supply the
   existing vault identifier only when the authenticated manifest and registry
   are verified against the same remote HEAD, account, session, target and
   entity. This read-context recovery does not adopt a profile, create a grant
   or change the legacy write route; missing or conflicting proof blocks it.
4. Grant, delegation and revocation changes are represented by append-only
   events in `meta/representative-events.yaml`; current state is checked before
   dependent operations. Each event records event ID/type, actor and subject
   account IDs, vault ID, entity, actions, scope, time, commit reference and
   basis. The initial grant event is mandatory for a new vault. These grants do
   not create epistemic Authority or apply across vault boundaries.
5. After entity confirmation and creation authorization, bind the human creator
   to the stable authenticated account identifier and register them as initial
   representative only for the new vault. This does not establish Owner or
   epistemic Authority, retroactively identify creators, or grant rights over
   an existing vault of that entity.
6. Every supported execution route, with or without Python, enforces the same
   canonical CRUD contract, including semantic review where required,
   deterministic structure/reference/version checks, expected-head/CAS,
   idempotency, persistence, durable receipt and readback. A remote Git-backed
   mutation commits its Record and receipt sidecar atomically in one Git tree/commit at
   `meta/operation-receipts/record-mutations/sha256-<key-hash>.yaml`. The path
   uses SHA-256 of the raw idempotency key; the raw key is never persisted. The
   receipt binds request fingerprint, target vault, Record ID/path, expected
   base HEAD, resulting Record hash/version, minimized actor/reason hash, methodology
   version, source method version and source implementation commit. It contains
   no resulting commit SHA, avoiding self-reference. A retry with the same key
   compares fingerprint/context (including the original base when supplied)
   and verifies the current Record hash/version
   against the receipt; drift is reported without replay-success claims or
   automatic reapplication. A key reused for another request conflicts without
   overwriting the receipt. Identical content under another key is a distinct
   operation. A route lacking atomic sidecar persistence or verified source
   identity blocks the mutation; direct file or contents-API writes are not a
   fallback.
7. These additions preserve existing V3 Record data contracts and legacy
   authorization/write behavior, so they are a MINOR change under Decision
   0023 relative to the last stable 3.0.0. The 3.1.0 candidate remains a
   release target until its publication gates complete. If evidence shows any
   previously conforming instance becomes invalid, reclassify before release.

## Reconciliation of prior decisions

- `0026` remains authoritative for epistemic information types and the
  Record/Chunk distinction; this decision does not redefine them.
- `0040` remains authoritative for multi-vault, multi-entity boundaries. Its
  personal-anchor-first premise is superseded only as a discovery and
  onboarding prerequisite; separation and non-reciprocity remain.
- `0044` remains valid for optional, operator-confirmed registration hints;
  registration is no longer required to access a directly identified target.
- `0045` remains valid for its onboarding and profile capture steps, except the
  requirement to instantiate a personal anchor before any other vault.
- `0052` remains valid for local-only pointers and source-of-truth boundaries;
  this decision adds no global router and no mirrored authority metadata.
- `0074` remains authoritative for independent profiles and governance roles.
  This decision defines scoped operational write eligibility without treating
  profile or grant as epistemic Authority.

No historical record is rewritten. Only the conflicting forward-looking
requirements are superseded for new operations; old instances remain readable.

## Consequences

The skill, scaffold, compatibility contract, and runtime adapters must use the
same eligibility distinctions and grant fields. Tests must cover missing,
expired, revoked, wrong-account and wrong-scope grants, no-anchor ingress, and
Python-present/absent parity. Remote publication, ACL changes, installation,
merge and release remain separate gated actions.

## Rationale

Separating methodological eligibility from technical execution allows a user
to operate a personal or team vault when the host supports the operation while
preserving the stronger grant boundary for entity-wide knowledge. Optional
discovery hints avoid turning an onboarding convention into a universal access
precondition. A runtime-independent CRUD contract keeps semantic and structural
invariants stable as adapters change.

## Discarded alternatives

- **Require a personal anchor before any other vault.** Rejected because it
  adds an unrelated onboarding prerequisite and blocks direct, authorized
  access to an existing target.
- **Treat GitHub write access as sufficient for entity writes.** Rejected
  because provider permission is not methodological authorization.
- **Require Python for all canonical CRUD.** Rejected because runtime choice
  must not redefine the governed operation; every supported route must prove
  the same checks or block the dependent operation.
- **Infer a representative for an existing vault from repository metadata.**
  Rejected because authorship or administration does not establish the human
  authority or scope of a current grant.
