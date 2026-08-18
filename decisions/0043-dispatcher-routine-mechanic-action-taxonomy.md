# 0043 — Dispatcher/Routine/Mechanic/Action: a four-layer taxonomy

**Status:** Accepted

## Context

Several concepts already operate normatively in this methodology without ever having been placed on a shared taxonomy explaining how they relate to one another: CRUD (`SPEC.md` section 2-B, `decisions/0012`), Promote/Depromote/Redbutton (section 13, `decisions/0027`/`0028`/`0030`), and the three scheduled rituals now organized under the Dispatcher (REM, frontmatter audit, weekly structural audit — `decisions/0042`). A separate, already-existing scheme classifies *how* an individual step behaves (deterministic, discretionary, or gated by invariant 5) — that scheme is orthogonal to this one: it says nothing about what *kind* of thing a piece of behavior is in the first place.

Without a shared vocabulary for "kind of thing," each new addition to the methodology (most recently, the Promote/Depromote/Redbutton actions and the Dispatcher itself) has had to informally reuse words like "action" and "mechanic" without a declared meaning, and a forthcoming Bootstrap capability (a later lote of this same taxonomy revision) would otherwise need to invent its own category from scratch rather than fit into one that already exists.

A naming risk surfaced while drafting this Decision Record: an earlier working name for the Redbutton-governing mechanic was "sequenced deletion." That name directly contradicts invariant 3 (`SPEC.md` section 8 — a document is never physically deleted, only archived or superseded), which Redbutton itself already respects: it replaces content with a tombstone, it does not delete without a trace (section 13, `decisions/0010`). The name was promising a behavior the mechanic does not have.

## Decision

A four-layer taxonomy, naming what already exists rather than introducing new behavior:

- **Dispatcher** — triggers routines, by schedule (`decisions/0042`).
- **Routine** — a scheduled process: REM, frontmatter audit, weekly structural audit. Orchestrates sequences of actions, applying judgment where the routine itself requires it.
- **Mechanic** — the ruleset a family of actions must follow. Not itself an event — the rulebook an action follows when invoked.
- **Action** — the concrete operation, invocable on demand or by a routine as a building block (for example, REM's Consolidate function invokes the CRUD mechanic's Create action when writing a new document, `SPEC.md` section 5-A).

Three mechanics are formally named by this Decision Record — the actions themselves are unchanged, already normative:

1. **CRUD mechanic** — Create, Read, Update, Delete (`SPEC.md` section 2-B, `decisions/0012`).
2. **Publication mechanic** — Promote, Depromote (`SPEC.md` section 13, `decisions/0027`, `decisions/0030`).
3. **Sequenced-removal mechanic** — Redbutton (`SPEC.md` section 13, `decisions/0027`, `decisions/0028`). Named "sequenced removal," not "sequenced deletion," to avoid the invariant-3 conflict identified above. Kept as a mechanic separate from publication because the trigger profile differs (a deliberate curation decision, for publication, versus incident response, for sequenced removal) — each is expected to grow independent depth over time.

This taxonomy is orthogonal to the existing step-classification scheme (deterministic / discretionary / gated, `SPEC.md` sections 8/14): that scheme classifies how a step behaves; this one classifies what kind of thing it is. Both can apply to the same action at once (for example, CRUD's Create action is gated when it results in a durable write, per invariant 5).

## Rationale

Naming an already-real structure, rather than inventing new behavior, follows the same principle already used for the repository-type taxonomy (`decisions/0029`) and for CRUD's own original naming (`decisions/0012`) — both cases of formalizing vocabulary for something the methodology was already doing. Establishing the taxonomy now, rather than after the Bootstrap mechanic ships in a later lote, avoids retrofitting a shared category onto Bootstrap after the fact, which would be more disruptive than fitting it in from the start.

## Discarded alternatives

- **Leave CRUD, Promote/Depromote, and Redbutton without any shared taxonomy.** Discarded — the forthcoming Bootstrap mechanic (a later lote) needs a category to belong to; retrofitting a taxonomy after Bootstrap ships would touch more surface area than introducing it now, before Bootstrap exists.
- **A single flat "action" category, with no routine/mechanic distinction.** Discarded — collapses a real distinction this methodology already relies on: a scheduled orchestrator (a routine, like REM) is not the same kind of thing as a ruleset an operation follows (a mechanic, like CRUD).
- **Keep the working name "sequenced deletion" for the Redbutton-governing mechanic.** Discarded — direct conflict with invariant 3 (`SPEC.md` section 8); the same category of naming defect already corrected once in this same taxonomy revision (`decisions/0042`, REM/Dispatcher).
