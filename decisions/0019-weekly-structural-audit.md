# 0019 — Weekly structural audit: atomicity, placement, and sensitive data leakage

**Status:** Accepted

## Context

Neither the REM ritual (consolidation) nor the frontmatter audit (mechanical field check) assess the structural health of a repository as a whole — whether the atomicity of already-consolidated documents is still good, whether some file should change `category`/folder, and especially, whether any sensitive data has leaked into a repository of the wrong classification (for example, data that the privacy policy by instance, section 2-A and DR0009, prohibits in a corporate instance). This policy has existed as a rule since v1.3.0, but never had any periodic mechanism that actually verifies whether it is being followed.

## Decision

Structural audit is a new ritual, with a recommended weekly cadence, with three functions:

1. **Atomicity:** review whether recently consolidated documents (or those flagged by the maintenance queue, DR0017) still represent a single concept, or should be split.
2. **Placement:** assess whether the repository's `category`/folder structure still makes sense — whether newly accumulated critical mass justifies a subfolder that did not exist before (section 4), or whether a document is in the wrong place given the repository's declared scope (see scope declared in `AGENTS.md`, DR0015).
3. **Sensitive data leakage:** check, against the sensitive-data policy by instance type (section 2-A, DR0009), whether any document in the repository contains something that should not be there — this is the first time this policy gains a periodic verification mechanism, instead of just the rule.

Any structural audit finding is always presented to the human responsible for the instance before any action — moving, splitting, or removing a document never happens automatically (invariant 5).

## Rationale

Weekly cadence (more spaced out than the frontmatter audit/REM's daily cadence) reflects the nature of the check: structural problems and sensitive data leakage accumulate more slowly than new capture items, and structure review is more expensive (requires more judgment, potentially more document-body reading) than the mechanical frontmatter check. Placing the sensitive-data-leakage check here, rather than as a standalone ritual, avoids multiplying triggers for flows that already make sense to happen together (same principle already used in the decision to fold the `design-system` skill into `qualidade-visual`, a Personal Second Brain precedent).

## Discarded alternatives

- **Sensitive-data-leakage check as a standalone ritual, separate from the structural audit:** discarded for the same reason of not multiplying triggers unnecessarily — both require "looking at the whole repository with judgment," not just one document at a time.
- **Daily cadence, same as the frontmatter audit:** discarded due to cost disproportionate to the real pace of accumulation of the problem it solves — reassessing the entire structure every day is expensive and, in practice, would not see enough change to justify it.
