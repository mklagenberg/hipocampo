# Change Set 0110 — V3 Search & Progressive Disclosure test reinforcement

## Intent

Close the deterministic and semantic coverage gaps identified by comparing the
Search & Progressive Disclosure engine with the other V3 engines and with the
runtime assertions already exercised by its validator.

## Scope

This Change Set adds five named deterministic cases for bounded request
context, vault authorization, positive authorized expansion, stale evidence
and restricted content. It adds two pending semantic review candidates for
cross-entity or cross-vault scope collision and for authorization that does
not settle epistemic conflict. It also aligns the result envelope so restricted
content reports a blocked privacy dimension.

The existing three Search semantic cases remain pending human confirmation.
The work uses sanitized fixtures only, remains local and read-only, and does
not alter the released v2.2.0 specification, real vault caches, MCP
integration, publication, migration, deploy or release state.

## Authority and compatibility

The existing accepted Search decisions `FF-DEC-0061` through `FF-DEC-0066` and
Decision Record `deliverable/decisions/0108-v3-search-progressive-disclosure.md`
already establish the relevant disclosure, privacy, scope, CRUD and semantic
boundaries. No new structural decision is introduced here. SemVer remains
`none` for the unreleased V3 candidate.

## Acceptance criteria

- all nine named deterministic Search cases have executable bindings;
- missing request context and unauthorized vault scope fail closed;
- explicit authorized expansion is tested positively without changing
  authority or epistemic status;
- stale evidence is capped and restricted content is privacy-blocked;
- two new semantic candidates are fixture-backed, constitutionally based and
  remain pending human confirmation;
- all Search, engine-catalog, semantic, constitutional, structural, contract,
  CRUD and Change Set validators pass twice;
- no Record, event, vault, cache, remote or release state is mutated.

## Recovery

Reverting this Change Set restores the previous Search test inventory and
runtime privacy mapping while leaving Change Sets `0108` and `0109` intact.
