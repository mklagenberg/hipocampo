# 0027 — Promote, Depromote, and Redbutton: cross-repository lifecycle actions

**Status:** Accepted

## Context

CRUD (section 2-B) operates within a single repository. But content legitimately needs to move between repositories over time — personal knowledge that matures and is worth turning into corporate knowledge, corporate content shared more broadly than necessary that needs to be restricted, or content that violates the sensitive-data policy (section 2-A) and needs to be removed even without a formal request from a data subject. Today there is no formal mechanism for any of the three cases — the risk is ad hoc: manually copying and pasting (reintroducing the silent-divergence problem that `decisions/0002` already rejected), or having no path at all to remediate misplaced content beyond what `decisions/0010` covers (data subject request only).

The first line of protection against misplaced content remains the curation of the REM ritual itself (section 5-A, Consolidate function) — deciding at intake whether an item is born personal or corporate. This decision's actions are the complement: for when intake curation fails, or when an already-existing document needs to deliberately change classification, after the fact.

## Decision

Three new actions, documented normatively in `SPEC.md`, section 13:

### 1. Promote (personal → corporate)

Two paths, always presented together before any write (invariant 5):

- **Elegant (default recommended):** creates a new document in the corporate repository, following the discipline of `decisions/0011` — frontmatter rewritten from scratch for the destination's schema/policy, never copied verbatim; body depersonalized as needed; sensitive-data policy conformance check (section 2-A) before writing; `author` corrected to the corporate identity (`decisions/0020`); information-type labels (`decisions/0026`) reassessed in the new context. The originating personal document **does not change `status`** — it stays active, and just gains a new `related` (`$alias:`) pointing to the corporate document, with `revision_note` recording the date and nature of the derivation. The corporate document points back to the personal one the same way. The two evolve independently from then on — this is not replication in the sense vetoed by `decisions/0002`, because there was never an expectation of sync between the two.

- **Literal (rare):** the personal document is actually transferred — `status: superseded`, `superseded_by: $alias:destination`, `temporality: historical`, content preserved as it was at the moment of promotion. Before any write on this path, the agent explicitly explains: (a) this transfers ownership of the content to the company, per `decisions/0007` — the corporate repository's `LICENSE` declares the company as owner; (b) this is not trivially reversible. It only proceeds with explicit confirmation after this warning.

### 2. Depromote (level downgrade, same ownership domain)

Moves content between repositories of the same owner (e.g., `empresa-público` → `empresa-confidencial`, or between personal variants) without crossing the personal/corporate boundary — that's why it doesn't carry the ownership question of the literal Promote, and doesn't need the same explicit warning. Mechanics: `status: superseded` at the origin, `superseded_by: $alias:destination`. Literal reversal of Promote (corporate → personal, crossing the ownership boundary back) is out of scope for this action — it is not automated; it's a case-by-case decision by the responsible human, outside the normal Hipocampo flow, in the same spirit as `DISCLAIMER.md` ("does not replace legal compliance").

### 3. Redbutton (remediation of a 2-A policy violation)

Extension of the trigger from `decisions/0010` — see `decisions/0028` for the full detail. Summary: the same physical-deletion + tombstone mechanism from `0010` becomes triggerable also when the structural audit (5-C) or the instance operator identifies content that violates the sensitive-data policy (section 2-A), even without a formal request from the data subject.

### 4. Cross-repository `superseded_by`

`superseded_by`, used by Promote (literal path) and by Depromote, now formally accepts the same `$alias:` syntax already documented for `related` (section 6) — necessary for both actions to point to a document in another repository.

## Rationale

Elegant Promote avoids reintroducing the problem `decisions/0002` already solved (replication with silent-divergence risk) by treating the derivation as a new Create with documented provenance, not a copy with an expectation of sync. The literal path exists because sometimes the real intent is indeed to transfer — but the decision to do so, knowing it changes who is the legal owner of the content (`decisions/0007`), must be the human's, informed, never assumed by the agent. Depromote is deliberately simpler than Promote because it doesn't cross the same ownership boundary — treating both with the same weight would be disproportionate friction relative to the real risk of the common case (correcting over-exposure within the same company).

## Discarded alternatives

- **Generic Move/Copy/Delete, without direction distinction.** Discarded: "Copy" as a loosely maintained duplicate collides with `decisions/0002`; a single "Move" doesn't capture the risk asymmetry between crossing the personal/corporate boundary (real ownership question) and moving within the same domain (access reclassification, no ownership question).
- **Promote with a single (literal) path.** Discarded: hides the low-risk option (derivation, without transfer) from the user behind the only high-risk option (ownership transfer), when in practice most promotion cases don't need to be an actual transfer.
- **Depromote as an automated, symmetric reversal of Promote.** Discarded: the reversal crossing back into the personal domain faces the same ownership question as literal Promote, only without an equivalent clear legal basis — it's not a routine action the agent should automate.
