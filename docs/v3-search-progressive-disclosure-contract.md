# V3 Search & Progressive Disclosure contract — unreleased candidate

This document defines the read-side contract for the logical `Search &
Progressive Disclosure` engine. It is a candidate V3 contract and does not
activate V3 or alter the released v2.2.0 specification.

## Purpose and boundary

The engine locates potentially relevant Records or Chunks and determines the
maximum content that an already authorized flow may disclose. It does not
decide knowledge truth, create authority, grant access, or mutate a Record.

Search is local and read-only in the first implementation gate. Sanitized
fixtures are the only test material in this Change Set; the four real vault
caches remain outside its scope. MCP and host integration require a later
capability and authorization gate.

## Request envelope

A governed request declares, at minimum:

```yaml
request_id: "non-secret-stable-id"
intent: "didactic description of the retrieval need"
query: "bounded search terms"
entity: "entity-id"
vault_scope: ["vault-id"]
authorized_vault_ids: ["vault-id"]
knowledge_scope: "bounded-scope"
requested_disclosure: "L0 | L1 | L2 | L3 | L4"
explicit_expansion_authorization: false
presentation: "prose-default | structured-on-request"
```

The request must identify the entity, vault and knowledge scope. Missing,
ambiguous or inaccessible boundaries produce a blocked or partial result; the
engine does not infer a broader scope from a matching term.
The request declares one entity and one knowledge scope. Candidates outside
that entity, the requested/authorized vault set or the knowledge scope are
excluded before relevance ranking. When multiple authorized vaults within the
declared entity and knowledge scope return candidates for the same term, each
candidate remains a separate result with its own provenance and governance;
lexical overlap does not authorize merging or selecting a winner. A semantic
collision remains review-required.

## Result envelope

Every result carries these independent dimensions:

```yaml
record_ref: "non-secret-stable-reference"
relevance: "semantic assessment or bounded score; never authority"
authority: "declared | contextual | unknown | conflicting"
privacy: "allowed | redacted | blocked"
epistemic_status: "preserved source status"
interpretation_status: "needs_review | not_assessed"
disclosure_level: "L0 | L1 | L2 | L3 | L4"
evidence: ["non-secret source references"]
limits: ["access, freshness, scope or semantic limitations"]
freshness_note: "optional user-facing source-version boundary"
retrieval_path: "redacted operational path"
mutation: "none"
```

The output must preserve source provenance, entity, vault, scope, temporal
limits and epistemic status. A result may be relevant and still be
`unknown`, `conflicting`, `redacted`, stale, partial or blocked.
An explicit authorization may permit the requested content level, including
`L4`, when all privacy, scope and Record-read gates pass. This authorizes
disclosure only: it does not resolve a conflict, upgrade authority or settle
epistemic status. Preserve each Record and its evidence references separately;
do not merge conflicting sources or present a consolidated conclusion.
Operation `status: accepted` reports that the requested read/disclosure
completed within its gates. It does not mean that the retrieved knowledge is
accepted as true. The result and top-level `interpretation_status` must remain
`needs_review` whenever an included Record carries `unresolved-conflict` or
`conflicting`; otherwise Search reports `not_assessed`, not a truth judgment.
Default prose must make a material unresolved conflict visible and state that
no conclusion was consolidated.
When a record is privacy-blocked or has restricted visibility, the result
envelope reports `privacy: blocked`; disclosure authorization never changes
that privacy classification.

Record content and Artifact access are independent gates. A Record with
persisted prose remains readable when a linked Artifact is unavailable; the
structured result preserves the prose-derived disclosure and the internal
limit `artifact_access_unavailable`. The default user-facing prose describes
the version boundary instead of exposing that availability label: when
`observed_at` exists, it states the last-read timestamp and that later
updates were not verified or reflected; when the timestamp is missing, it says
the last-read date is unrecorded and later updates are unverified. `observed_at`
must be a valid timezone-qualified ISO-8601 timestamp. `checked_at` is an
availability-check time, not a content-read time, and must not substitute for
`observed_at`. This limit constrains direct Artifact verification,
currentness and Artifact-dependent operations, but it does not mean that the
Record content is missing. An inaccessible Record read is a different
condition and must be blocked with `record_content_unavailable`.

## Disclosure levels

Disclosure is explicit and monotonic. The requested level is an upper bound,
not an entitlement; privacy, authorization, provenance and state gates can
lower the returned level or block the result.

| Level | Meaning | Permitted content |
|---|---|---|
| `L0` | None | No Record or Chunk content; safe refusal or limitation only. |
| `L1` | Metadata | Stable identity, bounded provenance and safe operational metadata. |
| `L2` | Record envelope | The governed Record envelope and frontmatter; no Chunk body. |
| `L3` | Chunk content | Selected Chunk content when scope, privacy and authorization pass. |
| `L4` | Expanded authorized content | Additional related content only with explicit authorization and all prior gates. |

Recency, lexical match, ranking or semantic relevance never escalates a result
from one level to another.

## Presentation policy

The default response is integrated didactic prose that states what was found,
why it matters, the applicable limits and what remains uncertain. The engine
must expose separate dimensions or a table only when the requester explicitly
asks for a separated or structured view. Presentation mode does not change
the underlying access, privacy, provenance or disclosure decision.

## Guardrails and semantic boundary

Deterministic validation checks the presence and allowed shape of identity,
entity, vault, scope, disclosure, provenance, state, privacy, mutation, trail
and limits. Semantic review is required for intent, relevance, conflict,
applicability, contextual authority, epistemic interpretation and abstention.

The engine must fail closed when required Record content is inaccessible, a
privacy boundary is uncertain, or a requested expansion lacks explicit
authorization. An unavailable linked Artifact produces a bounded partial
result when the Record prose is readable; it must not trigger Artifact
reconstruction for display. The engine must preserve a limitation rather than
fabricate missing content.

## CRUD and operational trail

Search is not a second mutation route. It may call a canonical CRUD read when
the governed Record envelope is required, and any write-requiring flow must
hand off to canonical Record CRUD. No Search, disclosure, MCP or host adapter
may write directly to a Record.

The engine may emit a minimal redacted recovery trail under `meta/`. The trail
contains request identity, bounded scope, returned level, disposition,
redacted path and limits; it contains no Record body, secret, credential or
authority claim. The trail proves what path and limits were observed, not that
the returned knowledge is true.

## Compatibility and recovery

V2 frontmatter remains valid for v2 operation. A V3 consumer treats missing V3
metadata as legacy/unmapped and does not silently migrate it. An inaccessible
linked Artifact returns bounded Record content with an explicit limitation; an
inaccessible Record, unsupported host capability or interrupted Record read
returns a bounded partial or blocked disposition with the limitation
preserved. No retry may expand scope or disclosure implicitly.

See `decisions/0108-v3-search-progressive-disclosure.md` for the governing
decision and `docs/v3-contract.md` for the V3 candidate index.
