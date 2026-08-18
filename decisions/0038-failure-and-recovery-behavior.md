# 0038 — Failure and recovery behavior

**Status:** Accepted

## Context

Major finding 6 from the 2026-08-17 MODA self-audit (`audits/moda/2026-08-17-v1.0.0-self-audit.md`): the "failure and recovery" design dimension (MODA SPEC, 4.12) was entirely unaddressed — `SPEC.md` defined rules for the correct path only, with no explicit guidance for what an agent does when something goes wrong. The audit's own action plan (section 6, "Onda 4") named six concrete failure modes to cover: insufficient evidence, frontmatter↔body contradiction, unavailable tool, interruption mid-ritual, unsafe request, incompatible migration.

Hipocampo already had an implicit "flag, don't guess" posture scattered across several places — invariant 5 (`SPEC.md` section 8, the agent never writes without an explicit request), the read-time frontmatter validation rule (section 2-B, an expired `ttl` or deprecated vocabulary value is flagged, never silently fixed), and the real `.github/workflows/` permission blocker documented transparently in `decisions/0036` during Fase G. None of it had been consolidated into a single, explicit rule set that an agent — or an auditor — could check against as a whole.

## Decision

Add `SPEC.md` section 14, "Behavior under failure and recovery," defining the required agent behavior under each of the six failure modes named by the audit. Every mode is governed by the same underlying posture: never silently guess, never silently refuse, name the problem in plain terms, and hand the decision to the human when the decision is genuinely the human's to make. This is stated once, at the top of the section, rather than repeated six times.

The six modes and their concrete rule:

1. **Insufficient evidence** — state what is and isn't known; propose how to check, when checkable; never fill the gap with a plausible-sounding guess.
2. **Frontmatter↔body contradiction** — flag it; never silently prefer one side; never resolve it without an explicit instruction.
3. **Unavailable tool** — name exactly what couldn't be done and why; complete whatever doesn't depend on it; never silently drop the affected part while reporting the rest as done; never silently fall back to an unrequested mechanism.
4. **Interruption mid-ritual** — re-derive ritual state from the repository itself on resuming, not from memory of the interrupted conversation; tell the human it was left incomplete and from where it's resuming; invariant 5 applies again at resumption.
5. **Unsafe request** — refuse at the specific point of violation, not the whole surrounding task; name the invariant/policy at stake; offer a compliant alternative where one exists.
6. **Incompatible migration** — name the version gap; point at the relevant `MIGRATIONS.md` entry; confirm with the human how to proceed, never silently assume or silently apply the migration.

## Rationale

Every one of the six modes is grounded in something that has already happened in this methodology's own real use, or is a direct, predictable consequence of running an agent against fallible tools and incomplete/inconsistent input — not invented in the abstract. Keeping this as one `SPEC.md` section, in the same style as section 8's invariant list, mirrors how the methodology already handles "one underlying posture, several concrete instances" rather than treating each mode as an unrelated rule.

## Discarded alternatives

- **A separate `docs/failure-and-recovery.md`.** Rejected — the six modes are short enough to state directly in `SPEC.md`, unlike more elaborate mapped topics (e.g., `docs/MULTI-TOOL-USAGE.md`); a new top-level doc for six paragraphs would be disproportionate to the content.
- **Leaving it as scattered convention, relying on invariant 5 alone.** Rejected — invariant 5 only covers "don't write without request." It doesn't reach the other five modes MODA's dimension actually asks about (contradiction, tool failure, interruption, unsafe requests beyond the five enumerated invariants, incompatible migration); there was no single place for a reviewer or auditor to check the methodology's stance on any of them.
- **Making each failure mode's response deterministic/scripted, the way the frontmatter audit is (section 5-B).** Rejected — these are judgment calls by nature (is this evidence actually insufficient? is this contradiction real or a stale link?), not mechanically checkable the way a Decision Record template or a link target is (`decisions/0036`). Forcing determinism here would either be narrow enough to miss real cases, or broad enough to become another audit ritual with its own maintenance cost — disproportionate to what's being fixed.
