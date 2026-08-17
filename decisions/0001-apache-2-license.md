# 0001 — Apache 2.0 License, not MIT

**Status:** Accepted

## Context

Hipocampo needs an open-source license for the public repositories (`hipocampo`, `hipocampo-toolkit`). The most common choice for small projects is MIT, for simplicity.

## Decision

Use the Apache License 2.0 for both public repositories.

## Rationale

Apache-2.0 has three properties that MIT lacks and that matter here:

1. **Explicit trademark clause** (Section 6 of the license) — protects the name "Hipocampo" separately from the freedom to use the code. MIT doesn't distinguish this; anyone could use the name "Hipocampo" for a fork or derivative product without violating the license.
2. **Requirement to state changes in modified files** (Section 4) — gives traceability to derivatives: whoever forks and alters the code must flag it, which helps distinguish the original spec from variations.
3. **Patent clause with retaliation** (Section 3) — protects contributors and users against patent litigation from a contributor; zero cost to include, since there's no intention to monetize via patents.

## Discarded alternatives

- **MIT** — simpler, but without the three properties above. Discarded because trademark protection (item 1) is specifically relevant: "Hipocampo" is the personal name of the method, and the intent is for it to remain identifiable as such even when used by third parties.
- **No license (all rights reserved)** — discarded because it contradicts the goal of the methodology itself being freely adoptable — only the name/trademark is restricted, not the content of the spec.
