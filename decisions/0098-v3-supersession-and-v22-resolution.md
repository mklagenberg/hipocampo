# 0098 — V3 supersession and V2.2 resolution

**Status:** Accepted for the unreleased V3 candidate

## Context

Hipocampo `v2.2.0` introduced explicit compatibility, verification,
connector, session, onboarding, recovery and pending-access boundaries. The
unreleased V3 candidate implements a broader contract for entities, vaults,
privacy, authority, provenance, packages, operational events and phased
verification.

The V3 candidate must not leave V2.2 as a competing normative source or
silently carry forward a provisional V2.2 rule after V3 is accepted.

## Decision

V3 is sovereign over V2.2.

Every V2.2 capability receives an explicit disposition in the V2.2-to-V3
resolution matrix:

- `incorporated` — retained without a material semantic change;
- `superseded` — the problem remains in scope, but V3 provides the governing
  rule or a stronger mechanism;
- `retained-outside-contract` — retained as skill, host or operational
  procedure, not as a V3 content-contract rule;
- `deferred` — not yet resolved, with an explicit boundary and owner for the
  next decision;
- `retired` — no longer valid and must not be applied to V3.

V2.2 remains readable historical material and evidence. Existing V2.2 vaults
are not silently migrated, and the published `v2.2.0` tag is not rewritten.
V3 migration is a separate, explicit, reversible operation governed by
`MIGRATIONS.md`, compatibility gates, privacy rechecks and human approval.

## Resolution rules

1. A V3 Decision Record outranks a V2.2 proposal, fixture, procedure or
   implementation note.
2. V2.2 behavior may remain as a compatibility input only when it does not
   contradict the V3 contract.
3. A V2.2 claim of validation is not promoted into a V3 claim unless the V3
   evidence boundary and acceptance criteria are satisfied.
4. A V2.2 limitation is not treated as solved merely because V3 names a
   related concept. The V3 contract must state the actual coverage and limit.
5. Skill recovery, host capability and connector authorization remain
   operational boundaries unless a V3 contract explicitly adopts them.
6. The V2.2 pending-access fallback is superseded by V3's privacy,
   authority, minimization, acceptance and destination policy.

## Rationale

This preserves continuity without allowing a minor-release procedure or a
provisional fallback to constrain the major V3 design. It also makes every
gap visible before migration and LTE, while preserving V2.2 as a regression
baseline.

## Consequences

- The V3 crosswalk must cover Change Sets `0058` through `0069`, not only the
  older V2 schema surfaces.
- `2.x -> 3.0` requires a dedicated migration section and fixture set.
- The active V2.2 metadata ambiguity is recorded as a release-line issue;
  this decision does not rewrite the historical tag or release.
- The canonical compatibility state name is `compatible_with_upgrade`.
- The V3 candidate remains unreleased and does not activate behavior in an
  existing vault.

## Discarded alternatives

- Treating V2.2 and V3 as co-equal authorities was rejected because it would
  leave conflicts unresolved and make the effective contract depend on
  document order.
- Copying every V2.2 procedure into V3 was rejected because skill, host and
  methodology boundaries are different kinds of artifacts.
- Declaring all V2.2 limitations solved by analogy was rejected because it
  would overclaim remote authorization and runtime enforcement.
- Rewriting the published `v2.2.0` tag was rejected because historical release
  identity must remain stable.

## Validation plan

- Each V2.2 Change Set has exactly one disposition in
  `docs/v3-v22-resolution-matrix.yaml`.
- Every `incorporated` or `superseded` row points to a V3 contract, decision,
  fixture or explicit deferred boundary.
- The V3 crosswalk and `MIGRATIONS.md` agree on the migration boundary.
- V2.2 regression fixtures remain readable and V3 fixtures exercise the
  stronger policy.
- No real vault, remote transport, publication or V3 activation occurs in
  this change set.
