# 0008 — REM ritual and three-layer memory model

**Status:** Accepted

## Context

SPEC.md (section 5) formalizes how an already-existing document ages (`temporality`/`ttl`/staleness routine), but doesn't formalize how a new item — a raw capture, not yet curated — enters the system and becomes a consolidated document. Without this made explicit in the methodology, each instance reinvents (or lacks) its own capture→consolidation pipeline. An instance predating Hipocampo already operates this pipeline under the name REM ritual — a name that is, incidentally, the conceptual origin of the name "Hipocampo" itself (consolidation of memory from short- to long-term, in the brain, via the hippocampus during REM sleep).

## Decision

Hipocampo adopts a model of four memory stations and a consolidation ritual between them (SPEC.md, new section 5-A):

1. **Sensory memory** — raw perception buffer (e.g., the conversation window). High loss by design; it's not Hipocampo's role to retain this.
2. **Attention gate** — explicit mechanism that decides what crosses from sensory to short-term (e.g., a session "check-in"/dump). Only what passes through the gate enters the canonical system.
3. **Short-term memory** — item already captured in the canonical system (git), not yet curated. Minimum viable: a versioned `inbox/` folder in the repository itself — cloud infrastructure (queue, state store) is an optional "Local Extension," never a baseline.
4. **REM ritual (consolidation)** — reads only from short-term memory, never directly from sensory. Runs periodically or on request. For each pending item, decides between becoming a new document, merging with an existing one, or being discarded. The full plan is always presented before any execution (the same invariant of "the agent never writes without an explicit request," section 8, applied to this ritual).
5. **Long-term memory** — atomic, curated document with complete frontmatter. It's the main body of any Hipocampo content repository, already existing since v1.0.0 — not a new capability.

Additional rules: atomicity (a consolidated document = a single concept; raw material with N ideas becomes N documents); an agent harness `memory.md` and a handoff snapshot are neither sensory memory nor subject to the REM ritual (distinct mechanisms); schema evolution is reactive, growing only by critical mass (reinforcing the already-general principle from section 4).

## Rationale

Formalizes a pattern that already operates in practice in one instance, instead of leaving it implicit and subject to divergent reinvention by each new instance. It's strictly additive — no existing instance breaks because of this; adopting the ritual is optional, as the rest of the staleness routine already is in practice. Closes the conceptual circle between the project's name and the metaphor that originated it.

## Discarded alternatives

- **Keep it as an implicit convention, undocumented in the SPEC.** Discarded — this is exactly the problem that motivated this DR: real operational knowledge trapped in one instance, not reusable as methodology.
- **Bring cloud infrastructure (queue/state store) in as a mandatory part of the model.** Discarded — it breaks the scope's simplicity invariant ("git + markdown + AI rituals," section 1). It remains only as an example of a possible Local Extension.
- **Formalize only the (already-existing) staleness routine as sufficient.** Discarded — staleness covers the aging of an already-consolidated document; it doesn't resolve capture→consolidation.
