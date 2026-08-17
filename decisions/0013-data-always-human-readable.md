# 0013 — Data always human-readable, independent of AI product

**Status:** Accepted

## Context

The Hipocampo methodology is already, by design, git + markdown — but the reason for this design was never articulated as an explicit principle. Real instabilities of AI products reinforce why this matters in practice, not just in theory: Claude Cowork had multiple outages in July 2026 (July 6, 14, 21, and 25). If an instance's knowledge could only be read through a specific interface or product, an outage of that product would leave the user without access to their own knowledge — not just without the convenience of operating it with AI.

## Decision

Formalize as an explicit principle (DISCLAIMER.md, new section): all data in a Hipocampo instance must remain legible and navigable by a human using only the repository's native tools — GitHub's own markdown viewer, any text editor, `git log`/`git show` — without depending on any specific AI product being online. This is not a limitation of the methodology — it is the same characteristic that already guarantees, in section 2 (`visibility`) and in `DISCLAIMER.md`, that access permission is always resolved at the GitHub level, never by a third-party product layered on top of it.

## Rationale

Vendor lock-in is a real and growing risk as more functionality gets built on top of specific AI products (skills, MCPs, agents). An outage, a product discontinuation, or a pricing change should never put access to the knowledge itself at risk. The Claude Cowork outage in July 2026 is used here as factual validation of a generic risk, not as a specific reason against that product — the same argument would hold for any other.

## Discarded alternatives

- **Not formalizing, leaving it implicit in the design that already exists (markdown + git).** Discarded: same reasoning as `decisions/0012` — a principle that already exists in practice, but was never written down, risks being eroded by a future decision that seems reasonable in isolation (for example, storing some data only in a binary/proprietary format "because it's more efficient").
- **Formalizing while citing the Cowork outage as the central and specific motivation.** Discarded: it would tie the principle to a specific incident and product, when the risk is generic to any AI product — the outage is evidence that the risk is real, not the cause of the principle.
