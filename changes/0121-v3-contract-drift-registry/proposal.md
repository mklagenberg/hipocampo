# Change Set 0121 — V3 contract-drift registry

## Intent

Close the migration-preparation residual in the V2.2-to-V3 resolution matrix by
linking migration-relevant V3 surfaces to their authority, existing drift
classification, permitted action, fixture and deterministic validator.

## Scope

Add a YAML crosswalk for the five existing drift classifications; link it from
the drift procedure; extend the deterministic validator to verify references,
classification/action consistency and fixture outcomes; and update the
verification-boundary coverage and resolution-matrix residual.

This change adds no drift class, permission, migration behavior, release state
or claim about a real vault. It does not inspect, read, write or migrate any
vault. The crosswalk remains a traceability aid under the existing authorities.

## Authority and compatibility

The applicable constitutional clauses are 2.7 (deterministic proof versus
semantic interpretation), 2.8 (preserve uncertainty), 2.9 (privacy and least
privilege) and 2.10 (reversible, traceable change), with the resolution process
in section 4. This implements accepted Decisions 0058, 0088, 0097 and 0098 and
the migration boundary in Decision 0100. No new structural or normative
decision is introduced.

## Acceptance criteria

- all five existing classifications map to existing V3 surfaces, authority
  references, actions, fixtures and validators;
- every declared file reference resolves and each fixture has the expected
  classification and outcome;
- deterministic negative cases reject a missing surface, missing fixture,
  missing authority, unsupported classification and mismatched action;
- no existing action or classification changes, and no real vault is read or
  altered;
- the resolution matrix no longer describes the registry crosswalk as open,
  while keeping real-vault preflight explicitly unobserved;
- canonical repository and Change Set validators pass, and links and the final
  diff are reviewed.

## Recovery

Revert Change Set 0121 to restore the prior generic drift validator and
resolution-matrix wording. This does not alter vault state or require data
recovery.
