# 0018 — Frontmatter validation at read time (extension of CRUD/READ mechanics)

**Status:** Accepted

## Context

Section 2-B of SPEC.md (DR0012) already establishes that READ should read frontmatter first, for token economy — but it does not say that READ should *validate* that frontmatter against the current norm before delivering the content. Today, a document with an expired `ttl` is read and used as if it were current information, unless the frontmatter audit (DR0017) has already passed over it and someone has seen the queue. This leaves a window where outdated information is consumed without any flag, between one audit and the next.

## Decision

Every READ operation of the CRUD mechanic (section 2-B) now includes a light validation of the frontmatter read against the section 2 norm, in addition to the section 5 staleness check — regardless of whether the frontmatter audit (batch ritual, DR0017) has already passed over that specific document. If validation finds a problem, the agent explicitly flags to the user what is wrong and what needs to be done, before or alongside the response based on that content. In the specific case of an expired `ttl`: the agent makes it explicit that the information is outdated, and suggests revalidation via research when the document is `source: url` (a fact about the external world) — the same mechanism already covered by the `deep-research` skill, now also triggered by this signal, not only by explicit request.

This read-time validation never changes `status` or any field of the document on its own — it only flags. Changing `status` still requires the same already-established process (REM ritual or explicit request, invariant 5).

## Rationale

Frontmatter audit (batch ritual, daily) and read-time validation (mechanical, on every READ) are complementary, not redundant: the audit guarantees complete, periodic coverage, even of documents no one happens to access; read-time validation guarantees that no one consumes outdated information in the window between one audit and the next, exactly when the document is actually used. Having both covers both the "forgotten document" case and the "document accessed right after it expired, before the next audit" case.

## Discarded alternatives

- **Rely only on the batch frontmatter audit, without a read-time check:** discarded due to the exposure window between audit runs, especially relevant for `ephemeral` documents with a short `ttl`.
- **READ refuses to return content with an expired `ttl`, instead of flagging and returning it anyway:** discarded — the content is still generally useful (it is the best available information until revalidation), and refusing outright would hinder more than it would help; flagging clearly is enough to keep the usage decision with the human.
