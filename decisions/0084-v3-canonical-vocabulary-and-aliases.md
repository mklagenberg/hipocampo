# 0084 — V3 canonical vocabulary and conversational aliases

**Status:** Accepted for the unreleased V3 contract

## Context

V3 needs to understand natural, historical and colloquial wording without
creating a second persisted ontology. Conversational flexibility must not
silently change a type, destination or governance meaning.

## Decision

V3 uses one persisted English vocabulary for its canonical concepts. A
conversational alias may route to a canonical term or trigger a didactic
clarification question, but it never becomes a competing persisted type,
frontmatter value or manifest field. The resolver normalizes vocabulary only;
it does not infer authority, privacy, maturity, truth or ownership.

## Consequences

Natural language remains usable while storage stays deterministic and
auditable. Ambiguity becomes an explicit user interaction rather than a
silent agent decision.

## Rationale

A governed alias map preserves human usability while keeping persisted
vocabulary canonical, reviewable and stable across vault boundaries.

## Discarded alternatives

- Accepting free-form synonyms as persisted types.
- Resolving ambiguous vault or entity wording silently.
- Inferring authority, privacy or ownership from an alias.
