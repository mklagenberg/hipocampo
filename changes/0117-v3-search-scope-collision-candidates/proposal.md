# Change Set 0117 — V3 Search scope-collision candidates

## Intent

Implement Decision `0111`: keep same-term Search candidates separate across
authorized vaults and exclude records outside the requested entity, vault set
or knowledge scope.

## Scope

Clarify the Search contract, fixture, semantic review, constitutional basis,
deterministic binding and sanitized runtime validator. The existing local
engine already filters by entity, vault and knowledge scope and emits separate
Record results; this Change Set binds those behaviors to an executable case.

## Authority and compatibility

This Change Set implements Decision `0111` under Constitution clauses `2.4`,
`2.5`, `2.7`, `2.9` and section `4`. It clarifies the unreleased V3 Search
contract and does not alter released v2.2.0. Classification is normative
within the candidate; SemVer is `none` until release classification.

## Acceptance criteria

- Search excludes same-term Records from another entity or knowledge scope;
- eligible candidates from multiple authorized vaults remain separate;
- lexical overlap does not merge Records, select a winner or infer authority;
- each result preserves its own provenance and governance dimensions;
- the semantic collision remains review-required for any combined answer;
- sanitized fixtures and the integrated V3 engine suite pass.

## Recovery

Reverting this Change Set removes this candidate clarification and its
executable evidence. The released contract, real vaults and Record data are
unchanged.
