# 0012 — CRUD mechanics and frontmatter-first reading

**Status:** Accepted

## Context

The lifecycle of a Hipocampo document (`draft`→`active`→`stale`→`archived`→`superseded`, SPEC.md section 2) already implements, in practice, the four operations of a CRUD (Create, Read, Update, Delete): Create is the creation of the document with complete frontmatter; Read is the query performed by an agent or human; Update is content editing with a `revision` increment; Delete is mitigated by invariant 3 (never physically delete, only `archived`/`superseded`, with the narrow exception of `decisions/0010`). This mechanic was never explicitly named "CRUD" in SPEC.md, which makes it harder to communicate the model to those who already know the term from other technical contexts (databases, APIs). Furthermore, how an AI agent should spend tokens while operating this mechanic was never specified: today nothing stops an agent from reading the entire body of every candidate document during a search, which is costly and unnecessary when the frontmatter already carries enough metadata to filter (`type`, `tags`, `status`, `temporality`, `related`).

## Decision

Explicitly name the lifecycle mechanic as CRUD (SPEC.md, new subsection 2-B), mapping Create/Read/Update/Delete to the operations that already exist. Add a recommended reading rule for the agent: when operating over multiple documents (search, triage, staleness), always read the frontmatter first — YAML, low token cost, enough to filter and decide relevance — and only read the document's full body afterward, once the frontmatter has established that this specific document needs a full read. This is not a new behavior rule — it is the formalization of an efficient practice that should already have been obvious, but was never written down.

## Rationale

Naming the mechanic as CRUD takes advantage of vocabulary already familiar to people coming from other technical fields, easing communication without inventing new terminology. The frontmatter-first rule is purely a matter of cost efficiency (tokens), which becomes increasingly relevant as an instance grows — an instance with hundreds of documents should not cost hundreds of full reads just to decide which three are relevant to a question.

## Discarded alternatives

- **Not naming the mechanic, leaving it implicit.** Discarded: it makes it harder to explain the methodology to those who already know the term CRUD from another context, with no gain from not naming it.
- **Requiring a full read always, with no frontmatter-first stage.** Discarded: it wastes tokens in any instance with a reasonable volume of documents, unnecessarily — the frontmatter already carries enough metadata to filter in most cases.
