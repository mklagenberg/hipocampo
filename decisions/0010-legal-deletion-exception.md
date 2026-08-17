# 0010 — Physical-erasure exception for legal obligation

**Status:** Accepted

## Context

Invariant 3 exists to guarantee full auditability — no content decision disappears without leaving a trace, even when a document becomes `archived` or `superseded`. This is a real strength of Hipocampo. But this same strength collides with a legal obligation: if a document contains personal data of an identifiable person (a colleague, a client contact) and that person exercises the legally provided right to erasure, "never physically delete" isn't a valid option — it's noncompliance.

Two things reduce the practical frequency of this problem, without eliminating it:

1. **The privacy-by-instance policy (`decisions/0009`) already bans most sensitive personal data** from the corporate instance (health, personal contact, performance review, salary/vendor figures). What remains permitted — full name, job title, professional contact, with a year citation — is still personal data under the law, just of much lower severity. This exception should be seen as coverage for the residue, not for the bulk of the content.
2. **LGPD Art. 4, I** excludes from the law's scope the "processing of personal data carried out by a natural person for exclusively personal and non-economic purposes" — which likely takes a private personal instance with no economic purpose out of the law's scope by definition, not just in practice. The real, recurring exposure is concentrated in the corporate instance, where the law actually applies and the `owner` (the organization) acts as Controller.

## Decision

Invariant 3 continues to hold for the normal lifecycle of knowledge — nothing is deleted just because it became outdated, wrong, or was replaced; that continues to be resolved by `archived`/`superseded`, with no exception.

A formal, narrow, and documented exception is created: **physical deletion of the specific personal content is permitted when, and only when, triggered by a legitimate erasure request from an identifiable data subject, with a real legal basis** (LGPD Art. 16 / GDPR Art. 17). It's not an open door to "clean up" the repository for convenience — it's a response to an exercised right.

When this exception is triggered:

1. **The agent never decides alone.** Same principle as Invariant 5 and `decisions/0009`: the legitimacy of the request (is it really a valid erasure right, or is there a legal basis that authorizes keeping the data — compliance with a legal obligation, an ongoing proceeding, etc.) is assessed by the human responsible for the instance, not by the agent.
2. **The specific personal content is replaced by a "tombstone"** — a minimal record that preserves only the fact that a removal occurred, the date, the legal basis invoked, and a generic description of the type of content removed (e.g., "name and job title of an individual removed at the data subject's request, LGPD Art. 16, on YYYY-MM-DD"), never the data itself. This preserves the auditability of the fact of the removal, without preserving what was removed.
3. **Acknowledged, not hidden, technical limitation:** replacing the content in the repository's current state (HEAD) resolves the common use case (whoever reads the repository today no longer sees the data). But git history, by default, still contains the original content in old commits — anyone with access to the repository can check an earlier commit and see the removed data. If the request requires complete removal from the history as well, that requires a second, manual and explicit step (history rewrite via `git filter-repo`/BFG), outside Hipocampo's normal flow, decided case by case by the responsible human — never automatic, because rewriting history is a destructive and rare operation, with side effects on any existing clone of the repository.

## Rationale

Without this exception, Invariant 3 forces Hipocampo to break a real law whenever a data subject exercises a legitimate right — this isn't a remote hypothesis, it's a direct legal risk for any corporate instance. The exception is designed to be the smallest possible deviation from the original invariant: it doesn't open a general deletion door, it keeps the record of the fact (preserving the spirit of auditability), and it honestly acknowledges the difference between "disappearing from the current state" and "disappearing from the complete history" — in the same spirit as `DISCLAIMER.md`, which already openly acknowledges that `visibility` isn't technical enforcement. Pretending the problem doesn't exist would be worse than documenting it with a partial, honest solution.

## Discarded alternatives

- **Keep Invariant 3 with no exception at all.** Discarded: it puts any corporate instance in a state of automatic legal noncompliance in the face of a valid request.
- **Allow free deletion, for any reason, reverting Invariant 3 across the board.** Discarded: it destroys the auditability that is the method's main strength — it would open room to delete inconvenient decisions, not just to comply with a legal right.
- **Automatically rewrite git history every time the exception is triggered.** Discarded: it's a destructive operation, too rare to automate; deciding whether it's worth it (and coordinating with whoever has clones of the repository) needs to be a human, case by case.
- **Create a new `status` value (e.g., `erased`) just for this case.** Discarded for now — reusing `revision_note` to record the reason and the legal basis is already sufficient and avoids inflating the `status` enum for a rare case (the same reactive-expansion rule from SPEC.md sections 3/4).
