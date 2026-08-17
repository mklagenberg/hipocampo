# Invariants — what and why

Five rules that no Hipocampo instance overrides, under any circumstance (`hipocampo/SPEC.md`, section 8). Each one exists for a specific structural reason, not arbitrary convention — it's important to know why, in order to recognize when a new situation still falls under the rule, even when it isn't obvious at first glance.

## 1. No knowledge repository is public to the internet

`visibility` in the frontmatter (`public | internal | confidential | restricted`) is just a label of intent — GitHub applies real permission per **repository**, not per file within it. A `confidential` label on a public repository does not stop anyone from reading the file; it is decorative. The only enforcement layer the host actually applies is the repository's visibility. That's why this rule is a structural invariant, not a suggestion.

## 2. `author` is always a person, never the AI

An agent may write the text, but who decided that it became valid knowledge — who stands behind the recorded statement — is always human. Without this, the second brain becomes a black box of claims with no traceable owner. The exception is scoped only to historical/migrated content with no individual authorship recoverable at the source (`CONTRIBUTORS.md`, `@section-name`) — a new document never uses this exception.

## 3. A document is never physically deleted — only archived or superseded

It preserves decision history (including "why I used to think that"), avoids silent loss of context, and creates deliberate friction against deleting out of convenience. Formal and narrow exception: a genuine legal obligation to erase personal data (LGPD Art. 16 / GDPR Art. 17) — always with an explicit human decision, never decided by the agent alone, and always replaced by a minimal record of the fact ("tombstone"), never zero trace.

## 4. Access separation is always by repository, never by a label within a shared repository

Same logic as invariant 1, applied within a repository with multiple people: GitHub's actual permission granularity is the repository. `visibility: restricted` on a repository the whole team accesses does not stop anyone on the team from reading that specific file. Content that genuinely needs technical enforcement goes into a separate repository with restricted permission — never just a frontmatter label on a more open repository.

## 5. The agent never writes, edits, or deletes content without an explicit user request in the current conversation

A human control point against autonomous drift. Even the recurring rituals (frontmatter audit, REM, structural audit) only get as far as a **proposed plan** on their own — actually executing any content change always waits for explicit confirmation in that conversation. "Running the REM" is not the same thing as "applying the REM's decisions without review".