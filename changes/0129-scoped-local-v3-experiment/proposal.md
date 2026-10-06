# Change Set 0129 — Scoped local V3 experiment

## Problem

The operator accepted three concrete entry decisions on 2026-10-06: a task
refresh protocol, candidate-skill use in four local vaults, and the canonical
persistence architecture in Decision 0116 / Change Set 0128. The earlier
candidate isolation rule prohibited real-vault use. Its exception needs a
durable scope without activating a release or changing the reviewed package.

## Proposed contract

Permit the explicitly authorized WRK-0074 experiment under Decision 0117.
Refresh a clean operational copy on main once per task, then use a dedicated
migration branch with source/context fingerprint checks. An isolated linked
worktree may remain inside its own vault's Git boundary; original dirty state,
indexes and uncertain locks remain untouched. This is an implementation of
the accepted refresh protocol, not permission to remove a lock.

Read legacy V2 knowledge through its compatible route. Exercise candidate V3
only on valid V3 Records using canonical read/CRUD, explicit authorization and
a cumulative Collection registry. Preserve proposed and accepted states.

## Acceptance criteria

- Bind the three operator decisions and scope in a Decision Record.
- Preserve candidate package files and their previously reviewed fingerprint.
- Require fresh main entry, exact remote and branch/source/context checks.
- Keep original state, private evidence and recovery within each vault.
- Never infer accepted Collections, mappings, reviews, privacy or recovery.
- Keep publishing, installation, ACL and released compatibility unchanged.

## Alternatives, risks and recovery

Blanket V3 activation is rejected; changing candidate text unnecessarily would
invalidate its semantic review binding. Direct Record writes remain forbidden.
Drift, incomplete authority or interrupted apply retains the affected scope.
Linked worktrees provide isolated indexes without deleting uncertain locks;
do not remove them or restore Records to conceal effects. End or reassess the
experiment at WRK-0074 completion, revocation or a failed control.

## Compatibility and status

Unreleased, narrowly scoped normative exception to candidate isolation; no
released SemVer change. The operator accepted the three underlying decisions,
not per-item proposals or a release. This Change Set projects that acceptance.

## Validation

Validate Decision Record structure, Change Sets, contracts, skill package and
candidate review binding. Exercise clean-main linked-worktree entry with real
Git fixtures while an original index lock and untracked file remain intact.
Verify every real entry separately; synthetic success is not real readiness.
