# Change Set 0115 — V3 CRUD read authorization context

## Intent

Correct a fail-open path in the unreleased V3 CRUD candidate: a logical Record
read currently succeeds when the request omits `authorized_vault_ids`. Require
an explicit, non-empty vault authorization context before returning Record
content.

## Scope

The change is limited to the local V3 CRUD boundary and its sanitized
validators. Missing, empty, malformed, or non-matching vault authorization
contexts are rejected. Authorized reads remain read-only. The context is an
input to this local candidate; this change does not authenticate an actor,
integrate a host, or prove production access enforcement.

## Authority and compatibility

This implements the existing V3 CRUD contract: Read resolves actor and scope,
and the project fails closed when authorization is absent. It does not create a
new authority rule or amend the released v2.2.0 contract. The Change Set is
normative within the unreleased V3 candidate; SemVer is `none` until a release
is classified.

Applicable project principles are Constitution clauses 2.6 (CRUD boundary),
2.7 (verification limits), 2.9 (privacy and least privilege), 2.10
(traceability), and the resolution procedure in section 4.

## Acceptance criteria

- a Read without an actor authorization context is blocked;
- missing, empty, malformed, or non-matching `authorized_vault_ids` are
  blocked;
- a Read whose Record vault is explicitly included succeeds without mutation;
- both the logical MCP Read and public CRUD read method require the explicit
  context;
- the engine matrix binds the new deterministic case to an executable test;
- the integrated V3 engine suite and repository/Change Set validators pass;
- the local-versus-host authentication limitation remains explicit.

## Recovery

Reverting this Change Set restores the prior behavior in the unreleased
candidate. The released v2.2.0 contract and existing vaults are unaffected.
