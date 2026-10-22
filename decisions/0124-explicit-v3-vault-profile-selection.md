# 0124 — Explicit V3 vault-profile selection at creation

**Status:** Accepted direction from the operator on 2026-10-22

## Context

Decision 0074 defines the three V3 policy profiles, but the V3 scaffold still
omits `instance.vault_profile`. Several compatible V3.0.0 manifests also omit
it. The older bootstrap narrative assumes that a personal anchor is always
created first, contrary to the accepted first-use direction in management
Decision FF-DEC-0088. The two absences require different responses.

## Decision

Every newly created V3 Vault must have exactly one operator-selected
`instance.vault_profile`: `team`, `personal`, or `entity`. Present all three
with their practical read/write, scope, privacy and curation consequences.
Recommend `team` as the initial choice, but require an explicit answer and
confirmation in the exact creation plan before any repository or manifest
write. A default is a user-interface suggestion, not an inferred persisted
value. Ask for the entity separately; do not derive it from the profile or
scaffold profile name. Record the authenticated creator as the initial
representative of this new Vault only, separately from knowledge Authority.

An existing compatible V3 Vault lacking `instance.vault_profile` retains its
previously governed operations and emits a profile-undeclared WARNING. The
missing field does not become `team`, invalidate compatibility, or authorize
new profile-dependent eligibility. Adopting a profile is a selected-vault,
confirmed, reviewed metadata change under the V3-to-3.1 upgrade procedure.
A newly created but incomplete Vault has no legacy exception: report the
partial creation and reconcile it before profile-dependent operation.
V2/V2.1 bounded read support remains separate from V3 compatibility.

A personal anchor is optional for access to another entity's authorized
Vault. Without one, use bounded discovery and temporary project-local hints,
revalidate the remote target, and never claim a complete canonical inventory.
Offer personal-Vault creation when a permitted personal write requires a
destination; refusal means no personal material is persisted.

`team`/`personal` profile selection supplies methodological write eligibility
under the current contract; `entity` writes require a valid scoped registered
grant. No profile supplies GitHub permission, MCP operations, RecordCrud
capability, privacy clearance, or epistemic Authority. Decision 0074's
statement that a profile does not grant write access refers to those separate
permissions, and is read with this distinction.

## Consequences

- Add the field to V3 scaffold inputs and output, and synchronize skill
  instructions, bootstrap, taxonomy, upgrade, fixtures and diagnostics.
- Bump the independent bundled skill version because its instructions change;
  bump scaffold profile/engine versions for the new creation contract.
- Keep existing V3 Records, historical verification, vault manifests and GitHub
  ACLs untouched. No constitutional exception or incompatible migration is
  authorized.
- Check both semantic instructions and deterministic assertions where both
  exist, and review affected older use cases for contradictory outcomes.

This decision applies FF-CON-0001 clauses 1.5–1.7, 2.4, 2.6–2.11 and its
conflict procedure. It narrows the creation default without widening access.

## Rationale

A suggested `team` choice reduces setup effort without inventing a governance
declaration. Separate treatment for old and incomplete manifests preserves
compatible use while withholding new profile-dependent policy until its
premises are known. Asking entity independently prevents profile labels from
crossing organizational boundaries.

## Discarded alternatives

- Silently persist `team` when the operator does not answer: creates an
  unreviewed policy and can widen eligibility in a pre-existing Vault.
- Require every existing V3 manifest to adopt a profile before reading:
  mistakes an optional new policy for a compatibility requirement.
- Restore mandatory personal-anchor creation: blocks authorized entity reads
  and creates a personal Vault without a current persistence need.
