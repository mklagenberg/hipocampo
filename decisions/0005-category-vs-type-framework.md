# 0005 — `category: frameworks` and `type: framework` are orthogonal axes

**Status:** Accepted

## Context

Two frontmatter fields use the word "framework" in apparently overlapping ways: `category` (a free string field) can be `"frameworks"`, and `type` has the value `framework`. It was necessary to decide whether this is redundancy to be resolved or two genuinely different things.

## Decision

Keep both fields coexisting, without merging them. `category` decides where the document physically lives (a subfolder per topic, which only exists once there's critical mass). `type: framework` decides the authorship/ownership regime (SPEC.md section 3, DISCLAIMER.md), independent of folder.

## Rationale

A document can be `type: framework` (subject to the author/owner ownership regime) without yet having `category: frameworks` — not having reached critical mass of documents on the topic to justify a physical subfolder doesn't change the ownership regime of the content itself. The two fields answer different questions ("where does this live" vs. "who owns this") that only coincide in name by a vocabulary accident.

## Discarded alternatives

- **Merge the two into a single field** — discarded because an isolated `type: framework` document (without folder critical mass) would lose its ownership marking if `category` were the only field, or a document in `category: frameworks` that isn't subject to a special authorship regime would gain an incorrect classification if `type` were eliminated.
- **Rename one of the two to avoid the name coincidence** — considered, but each name is already the most descriptive one for what the field does; the explicit note in SPEC.md (section 4) resolves the confusion without needing to invent a worse name.
