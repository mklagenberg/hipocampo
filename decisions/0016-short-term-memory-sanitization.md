# 0016 — Short-term memory as a sanitization stage, not just raw capture

**Status:** Accepted

## Context

Section 5-A of SPEC.md (v1.2.0, DR0008) already describes four memory stations — sensory, attention gate, short-term, REM consolidation, long-term — but defines short-term shallowly: "item already captured in the canonical system (git), not yet curated," with `inbox/` as the minimum viable version. In practice (reported on 2026-07-30), consolidating directly from the inbox to long-term, repeatedly, over the evolution of a single subject, gradually makes a mess of the structure: atomicity is lost, file placement becomes inconsistent, with no intermediate stage forcing sanitization before the final promotion.

## Decision

Short-term now becomes explicitly a sanitization stage, not just a capture buffer. Revised definition of the three layers relevant to day-to-day operation (sensory memory and the attention gate remain as already described):

1. **Sensory:** lives outside any Hipocampo repository — the conversation/session itself, notes in Google Keep, documents in Google Drive, an attached file. Never versioned in git.
2. **Short-term:** already lives inside the repository (`inbox/`), already passed through the attention gate, but is not yet atomic nor necessarily in the right place — it needs sanitization (splitting by concept, reclassifying `category`/`visibility`, fixing naming) before becoming a long-term document.
3. **Long-term:** atomic, curated document, complete frontmatter, correctly placed — no change from the existing definition.

Each content repository has its own `inbox/` — maintenance rituals (REM, frontmatter audit, structural audit) always operate within the scope of one repository at a time, never globally across a person's/organization's repositories.

## Rationale

Without a recognized intermediate stage, every new consolidation is an isolated decision about where/how to structure that piece of knowledge — with no formal moment to reassess whether the accumulated structure still makes sense. Naming short-term as a sanitization stage gives an explicit place for this reassessment to happen before promotion to long-term, instead of after (when it has already become an "official" document and touching it carries more friction).

## Discarded alternatives

- **Keep the shallow definition of short-term (only "not curated yet"):** discarded because it does not address the reported problem — it does not say what needs to happen between capture and curation.
- **Sanitization happening only within REM consolidation, without naming short-term as a separate stage:** discarded because it dilutes responsibility — without a recognized name and place (`inbox/`), it stays implicit, and what is implicit in the methodology tends not to be followed consistently (same principle already applied to "never leave implicit" in local extensions, SPEC.md section 8).
