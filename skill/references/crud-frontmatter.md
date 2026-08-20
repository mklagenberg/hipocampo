# CRUD mechanics and frontmatter-first reading

Full reference: `hipocampo/SPEC.md`, section 2-B (decision 0012, decision 0018).

## Reading rule

When operating on multiple documents (search, triage, staleness), always read the **frontmatter first** — YAML, low token cost, enough to filter by `type`, `tags`, `status`, `temporality`, `related`. Only read the **full body** after deciding, from the frontmatter, that that specific document needs it. Do not read the entire body of every candidate by default — it is avoidable token waste, especially in an instance with many documents.

## Validation at read time (independent of the batch frontmatter audit)

Every READ operation — even a one-off query, outside any scheduled ritual — validates the document's frontmatter against the norm (section 2 schema) and the staleness check (section 5) **at the moment of reading**, regardless of whether the batch frontmatter audit (reference `routines.md`) has already gone through that document.

The same touchpoint performs a proportional privacy check of the body actually needed for the request: obvious credentials, non-public financial values, and a public financial value without its URL/date citation are findings. READ reports without rewriting; CREATE, UPDATE, and REM must make new or touched content conformant through an explicitly confirmed plan. Do not turn a methodology upgrade into a full-repository inspection.

If the validation finds a problem, explicitly flag what it is and what to do. Never change `status` or any field on your own as part of this validation — only flag it. Concrete cases:

- **Expired `ttl`:** warn that the information may be outdated. If `source: url`, suggest revalidation via research (the same trigger that activates the `deep-research` skill) before treating the content as current.
- **Missing required field:** point out which field is missing, without inventing a value.
- **`temporality: contextual` with `context_anchor` pointing to a document that is already `archived`/`superseded`:** flag that the document may be outdated even though its `ttl` has not yet expired — the anchor changed state before the deadline.

## Example

> User: "what do we know about vendor X?"
>
> The agent reads the candidates' frontmatter by `tags`/`type: company`. It finds a document with `ttl: 2026-03-01` (already expired) and `source: url`. Response: "I found a document about vendor X, but the `ttl` expired in March and the original source is a URL — the information may be outdated. Do you want me to revalidate it via research before answering, or would you rather see the content as-is, with that caveat?"

CRUD itself (Create/Read/Update/Delete) maps to the lifecycle of the `status` field (SPEC section 2) — Delete is always mitigated by invariant 3 (never physically delete), except for the narrow exception in decision 0010.
