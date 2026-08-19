# 0048 — Step-classification scheme (`docs/step-classification.md`)

**Status:** Accepted

## Context

`SPEC.md` section 5-D already names a three-value scheme for how a step behaves — deterministic, discretionary, gated — calling it "orthogonal to" the Dispatcher/Routine/Mechanic/Action taxonomy defined in the same section. Section 14 uses the same distinction implicitly throughout its six failure-and-recovery modes, without naming it there either. Neither section, nor any other, enumerates every routine/mechanic/action the methodology currently defines against this scheme in one place — each addition (vault discovery, Bootstrap) classified only itself, at the point it was introduced (`decisions/0044`, `0045`), which is correct practice for each individual DR but leaves no single reference an operator or auditor can check against.

This gap is also named directly in `conformance/moda.yaml`'s `distribution_of_agency` control: "Still no single place classifying every step in the methodology as deterministic/agent-reasoned/tool-executed/human-decided/hybrid — each addition classifies itself at the point it's introduced, not retroactively across everything that came before." That note uses MODA's own five-value agency vocabulary, distinct from the three-value scheme `SPEC.md` already uses natively.

An earlier draft of this idea used a binary scheme (deterministic/permission-required), evaluated and rejected during the taxonomy revision's planning discussion: a binary split would have forced the large middle category — an agent applying judgment without a write gate (e.g., reading and caching a manifest, deciding a document's disposition before any write) — into whichever of the two buckets was less wrong, for lack of a third option. The three-value scheme was tested against two real cases before being adopted here: vault instantiation (gated) and manifest read+cache (deterministic/discretionary, ungated) — both held without needing to be forced.

## Decision

Create `docs/step-classification.md`: a single reference formalizing Hipocampo's own three-category step-behavior scheme (deterministic / discretionary / gated) and applying it to every routine, mechanic action, and failure-recovery mode `SPEC.md` currently defines.

**Not a mapping onto MODA's own agency vocabulary.** This document formalizes and enumerates against Hipocampo's existing three-value scheme, not MODA's five-value one. No translation table between the two is attempted — doing so honestly would require deciding how, for example, "discretionary" (Hipocampo) maps onto "agent-reasoned" vs. "hybrid" (MODA), which is a real question this DR does not resolve. `conformance/moda.yaml`'s `distribution_of_agency` control note is updated to say exactly this: the gap it names is narrowed, not closed, by this document.

**Granularity: per action-step, not only per mechanic/routine.** A single mechanic action can itself be discretionary-then-gated in sequence (Bootstrap's Interview: discretionary capture, then a gated write of `profile.md`) — classifying only at the mechanic level would lose that distinction and misrepresent some actions as uniformly one category when they aren't.

## Rationale

Formalizing this as its own reference document, rather than expanding section 5-D or section 14 in `SPEC.md` directly, follows the same reasoning already applied to `docs/evaluation-scenarios.md` (`decisions/0039`) and `docs/getting-started-non-technical.md`/`docs/invite-template.md` (`decisions/0045`): a comprehensive enumeration is reference material an operator or auditor consults, not normative prose that changes what's required — inlining it into `SPEC.md` would bloat the specification with a table that will need a new row every time a future mechanic or action is added, without changing the underlying rule (Invariant 5 already requires the gate; this document only says *where* it applies). Keeping it separate also makes the "known limitation" below honest and visible, rather than implying `SPEC.md` itself guarantees staying in sync.

## Discarded alternatives

- **Binary scheme (deterministic/permission-required).** Discarded during the planning discussion, before this DR — see Context above. Would force most of what an agent actually does (judgment without a write gate) into one of two wrong buckets.
- **Attempt a mapping onto MODA's five-value agency scheme instead of, or in addition to, Hipocampo's own three-value one.** Discarded — a credible mapping is a real, separate design question (there is no obvious 1:1 correspondence between "discretionary" and MODA's "agent-reasoned"/"hybrid" split), and attempting one here risked either an arbitrary mapping presented as settled, or delaying this document indefinitely on a question orthogonal to what it actually needs to do (enumerate Hipocampo's own steps against Hipocampo's own scheme).
- **Inline the enumeration into `SPEC.md` sections 5-D/14 directly.** Discarded — see Rationale above; a growing reference table doesn't belong in normative prose that already has its own growth discipline (new type/mechanic values only on critical mass, `SPEC.md` §3/§4's expansion rule).
