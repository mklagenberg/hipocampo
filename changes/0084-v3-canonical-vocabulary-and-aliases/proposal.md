# Change Set 0084 — V3 canonical vocabulary and conversational aliases

## Intent

Implement D5.1 as an unreleased candidate contract with a single canonical
vocabulary, governed aliases and didactic clarification for ambiguity.

## Scope

The candidate documentation, resolver and fixtures are local to the
methodology repository. No v2 field is migrated and no alias is added to a
released schema.

## Acceptance criteria

- aliases resolve to canonical terms;
- methodology-routing aliases do not become persisted types;
- ambiguous destinations produce an explanatory question;
- vocabulary validation is deterministic;
- v2.1.1 remains the active released contract.

## Compatibility and recovery

V2 behavior is unchanged. Removing this candidate removes only the V3
resolver, fixtures and documentation; no vault content is modified.
