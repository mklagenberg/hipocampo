# 0026 — Taxonomy of information type in corporate instance

**Status:** Proposed

## Context

Corporate instance today doesn't distinguish types of statement within a document — everything is treated with the same epistemic weight, whether it's a confirmed fact, something someone reported without verification, a subjective judgment by the author, or a reconstructive personal memory. Frontmatter already resolves *who* is accountable for a document (`author`, invariant 2) and, for a new document, *who else* contributed (`contributors`, `decisions/0006`) — but neither resolves *what type* of statement is being made within the body.

Real example: `org-gauge/gauge-latam-observacoes.md`, in `hipocampo-company`, mixes observation ("LATAM budgets wrong — review it, with a tech and opec lens") and a recommendation about a named person ("Fábio to be coordinator") in a `confidential` document, never reviewed since the migration, under a real person's name, in a repository colleagues have access to. There is currently no gate that asks whether that judgment should be there, nor a marking that differentiates it from the factual account next to it.

Organic precedent, already present in the corpus itself before this decision existed: `org-gauge/modelo-matricial-gauge-e-papel-do-principal.md` already labels passages as "reported" and closes with "internal facts reported at the source and must be confirmed before being used as official institutional data" — organically distinguishing account from confirmed fact, without a formal convention. This is evidence that an account/opinion binary is not sufficient — at least a third state is missing (confirmed fact) and a fourth categorically different from the other three (personal memory).

## Decision

1. A document body that mixes more than one type of statement labels the relevant passages with one of these four prefixes:
   - **Fact:** verified/confirmed statement — can be treated as institutional data with confidence.
   - **Account:** what was said or observed, not yet confirmed — a snapshot of what was reported, not necessarily established truth.
   - **Opinion:** value judgment of the author or a contributor — with a different author, the conclusion may diverge.
   - **Memory:** reconstructive personal recollection — subject to bias and memory erosion; categorically different from an account (it's not what someone reported) and from an opinion (it's not a value judgment, it's a reconstruction of a lived event). The name was deliberately chosen to differ from "memory" so as not to collide with the already-established concept of "memory layers" (SPEC.md, section 5-A — sensory/short-term/long-term), which is about the processing stage of an item entering the system, not about the reliability of a statement.

   A document that is entirely of a single type doesn't need to label sentence by sentence — labeling exists only for mixed documents (same principle of not imposing disproportionate structure on the common case, `BEST-PRACTICES.md`, item 1).

2. Frontmatter field `contains_subjective_content: true|false` (default `false`), relevant when `owner` is filled in (corporate instance). Covers only **Opinion** and **Memory** — the two categories with real risk of personal accountability, since `author` is always a real person (invariant 2) and both are subjective, not independently verifiable. **Fact** and **Account** don't trigger this field — they carry precision risk, not personal accountability risk for the writer. This lets the frontmatter audit (section 5-B) and the weekly structural audit (section 5-C) find these documents without reading the entire body of every candidate (keeps the frontmatter-first principle, section 2-B).

3. The `@handle` is only appended to the label when the document has `contributors` filled in (`decisions/0006`) — a signal that more than one person contributed content to that specific document, making `author` alone insufficient to know whose each passage is. A single-author document (without `contributors`) does not need the inline handle; the frontmatter's `author` already resolves attribution without redundancy.

4. Write gate: before any Create/Update writes a new Opinion or Memory (`contains_subjective_content` becoming `true`) into a corporate instance, the agent explicitly asks whether that content should stay there, marked, or go to the personal instance of the responsible author/contributor. Without explicit confirmation of "yes, it stays," it goes to personal — never guesses (same principle as the repository router). This also applies to the REM ritual's consolidation function (section 5-A) when triaging `inbox/` destined for the corporate instance, and to the Promote action (section 13, `decisions/0027`) when reassessing labels in the new context.

5. `SPEC.md`, section 2 (unified schema): `contributors` now explicitly appears in the central field listing — it already existed and was already in real use (`decisions/0006`, `CONTRIBUTORS.md` of corporate instances), but never appeared in the schema's main listing, only in the Decision Record that instituted it. A documentation-gap fix, not a new capability.

## Rationale

`author` is always a real person, never the AI (invariant 2) — this already creates exposure risk when the content is subjective, not factual, in a repository that outlives the writer's time at the company and that other people with access to the repository can read. An account is, in principle, verifiable against an event or decision; opinion and memory are not — with a different author, or when revisiting the memory, the conclusion may diverge. A fact, once confirmed, can be treated as institutional data without that caveat. This doesn't conflict with `type: decision` (section 7): that is judgment about the architecture of the instance itself, an already-sanctioned category distinct from opinion about business, strategy, or third parties. Reusing `contributors` instead of creating a parallel attribution mechanism avoids duplicating a field that already answers exactly this question ("who else wrote this").

## Discarded alternatives

- **Keep this decision's original account/opinion binary.** Rejected: the corpus itself already demonstrates the need for a third state (confirmed fact, see `modelo-matricial-gauge-e-papel-do-principal.md`) and a fourth categorically distinct one (personal memory, reconstructive by nature, different from a third party's account and from a value judgment).
- **A frontmatter field per category (`contains_fact`, `contains_account`, etc.).** Rejected: only Opinion and Memory carry the personal-accountability risk that justifies discovery via frontmatter without reading the body; Fact and Account don't need this treatment, so a single field (`contains_subjective_content`) covering the two risk categories is sufficient, without bloating the schema.
- **Mark `@handle` on every sentence, always, regardless of single authorship.** Rejected: redundant when `author` alone already resolves it, and contrary to the principle of not imposing disproportionate structure too early.
- **Ban opinion/memory from the corporate repository.** Rejected: sometimes the recorded judgment or memory is the institutional decision worth preserving with attribution — the problem isn't its existing there, it's existing without being explicit and without the author's opt-in.
- **New `type` value (`type: opinion`) instead of a frontmatter flag.** Rejected: violates the `type` expansion rule (section 3, requires critical mass) and doesn't solve the common case, which is a mixed document.
- **A new `contributors` field, parallel to the existing one.** Rejected after review: `decisions/0006` already resolves exactly this need for a new document; creating a second mechanism would duplicate the schema without gain.
