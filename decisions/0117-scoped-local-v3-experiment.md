# 0117 — Scoped local V3 experiment

**Status:** Accepted for WRK-0074 only

**Date:** 2026-10-06

## Context

Candidate isolation prevented real-vault use while V3 remained unreleased.
The operator explicitly accepted three presented decisions: task refresh,
local candidate use, and canonical persistence under Decision 0116 / Change
Set 0128. Individual knowledge and Collection approvals were excluded.

## Decision

Allow the WRK-0074 local experiment in hipocampo-personal-vault,
hipocampo-concepts, hipocampo-company and hipocampo-company-vault. Keep the
personal and [Corporate entity] entities separated and enforce each vault's restrictions.
Use dedicated `migration/v3-*` local branches. Refresh clean main once per
task and bind the operational copy, remote, base and source/context hashes.
Preserved original copies with uncertain locks remain untouched; an isolated
linked worktree inside the same vault boundary may provide clean entry.

The candidate package is 2.0.0-rc.1 / ^3.0.0 with reviewed package fingerprint
91685f8106ef3e24d6a9c4e518e6b099f4ec2e760b90e93c29ad33bad90db3fa.
Its external experiment envelope overrides only the blanket real-vault
prohibition for this scope. Keep legacy V2 reads on the compatible route;
V3 requests require valid Records and canonical read/CRUD capabilities.

Do not install globally, activate V3 on main, push, open a PR, merge, tag,
release or change ACL. No Collection, mapping, semantic review, privacy claim,
recovery procedure or missing authority is accepted by this decision.

## Rationale

The explicit narrow authorization permits observable local experiments while
preserving the reviewed candidate package, released compatibility and the
single CRUD mutation boundary. Fixtures and actual operations remain separate.

## Discarded alternatives

- Activate V3 globally: outside authorization and release readiness.
- Remove uncertain locks to proceed: lacks the required proof/procedure.
- Treat technical acceptance as semantic approval: conflates separate gates.
- Rewrite the candidate package to encode one workspace: changes its binding
  without providing a general methodology capability.

## Constitutional and contract impact

Compatible with FF-CON-0001 sections 1.2–1.7, 2.2–2.11 and 3–4. This narrows
a specific isolation rule; it does not exempt privacy, provenance, CRUD or
reversibility. Change Set 0129 projects the decision. The authorization expires
at WRK-0074 completion or revocation; drift or failed controls suspend the
affected operation and require reconciliation before proceeding.

## Validation

Check exact package binding, compatible V2 reads, isolated clean-main refresh,
branch and authority evidence, cumulative registry and canonical reload.
Require separate pilot, recovery and real persistence evidence before scale.

## Approval

The operator explicitly accepted the three presented questions on 2026-10-06
and instructed execution to continue. This decision records that scope; it
does not accept individual proposals or confer release approval.

## Publication-boundary correction — 2026-10-08

The third-party entity identifier in the Decision was replaced with the
explicit placeholder `[Corporate entity]` under accepted Decision 0050 and
Change Set 0133. This is the narrow in-place anonymization expressly permitted
by Decision 0050 for accepted evidence. The four named repositories, original
authority evidence, restrictions and task scope remain unchanged; no new
authorization or exception is created. Detailed entity identity remains in
the authorized local governance boundary.
