# 0042 — Dispatcher decoupled from the REM ritual

**Status:** Accepted

## Context

In practice, REM (`SPEC.md` section 5-A) is the only process the methodology's recommended daily cadence schedules today. Mau's own clarification during the taxonomy review toward v2.0.0: REM's first action, in the operating model as actually used, is effectively to read the instructions for whatever processes are registered (frontmatter audit, weekly structural audit, anything added later) and decide whether and in what order to run each. Nothing in `SPEC.md` names this top-level scheduling role separately from REM itself.

REM already carries a precise biological metaphor — memory consolidation during REM sleep — and the rest of section 5-A's vocabulary (sensory memory, short-term memory, long-term memory) leans on that precision, following the Atkinson-Shiffrin model cited there. Frontmatter audit (section 5-B) and the weekly structural audit (section 5-C) are structural-maintenance rituals, not memory consolidation. If REM's name is stretched to cover triggering them too, the name stops matching what the process does most of the time.

## Decision

Introduce the **Dispatcher**: a separate, neutral, top-level scheduling concept, decoupled from REM. The Dispatcher triggers each **routine** — REM, frontmatter audit, weekly structural audit — on schedule. REM's own scope is unchanged: Consolidate and Update old memories only (`SPEC.md` section 5-A, unchanged by this Decision Record). It does not gain responsibility for triggering the other two rituals; they become sibling routines under the Dispatcher, not children of REM.

Execution order among the three routines remains fixed, exactly as already documented: frontmatter audit runs before REM in the same daily cycle (section 5-A, already the case before this Decision Record); the weekly structural audit runs on its own separate cadence (section 5-C). Whether the Dispatcher should instead decide execution order dynamically, from metadata declared per routine, is an open question — deferred, not decided here. None of these rituals is actually automated in practice yet for any real instance (dogfooding pending, per `AGENTS.md`), so building a dynamic-ordering mechanism now would be structure ahead of a real need — the same principle `decisions/0029`/`0030` already used to decline premature structure elsewhere in this methodology.

The format of the process registry the Dispatcher would read — to know what routines exist and, eventually, in what order to run them — is a future artifact, not designed by this Decision Record.

## Rationale

Keeping REM's scope exactly as documented preserves the precision the rest of section 5-A's vocabulary depends on; introducing a differently-named top-level concept for scheduling avoids the alternative of either overloading REM's name or leaving the scheduling role unnamed indefinitely. Deferring dynamic execution order matches the same don't-structure-before-the-real-need principle this methodology has already applied more than once (`decisions/0029`, `decisions/0030`).

## Discarded alternatives

- **Have REM itself trigger frontmatter audit and the structural audit.** This was the status quo before this Decision Record, implicit rather than decided. Discarded going forward — it is the exact scope-creep this Decision Record fixes.
- **Rename REM to a more generic term that could cover all three rituals.** Discarded — REM is an established, already-referenced name across `CHANGELOG.md` and `decisions/0008`/`0016`; renaming it would be more disruptive than adding a distinct concept above it, and would still cost the biological-metaphor precision this Decision Record is trying to preserve.
- **Design the process registry and a dynamic execution-order mechanism now, as part of this same Decision Record.** Discarded — no real instance runs these rituals yet, so the actual shape a registry needs is not yet known; building it now risks guessing wrong ahead of real use.
