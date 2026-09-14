# V3 governed CRUD use cases and validation plan

**Status:** unreleased V3 candidate; normative implementation gate.

## Boundary

Every mutation of a V3 Record crosses the canonical CRUD gateway. MCP is the
caller-facing transport in these cases. Engines prepare proposals and findings;
they do not persist Records. The gateway performs semantic admissibility before
deterministic commit.

Semantic validation is complete when the review covers provenance, authority,
entity, scope, destination vault, privacy, applicability, epistemic status,
maturity, staleness, conflicts and unresolved questions. It is not an
automated claim that the knowledge is true.

## Use-case matrix

| ID | Use case | Deterministic assertion | Semantic assertion |
|---|---|---|---|
| UC-CRUD-01 | Authorized read | no mutation or mutation event | access purpose and vault scope fit |
| UC-CRUD-02 | Unauthorized read | content is not returned | cross-vault boundary is respected |
| UC-CRUD-03 | Valid create | complete schema, references and event | source, authority and destination fit |
| UC-CRUD-04 | Invalid structure | no partial write | no semantic approval is implied |
| UC-CRUD-05 | Incomplete review | write is held | missing context or evidence is exposed |
| UC-CRUD-06 | Versioned update | expected version and atomic increment | evidence justifies the change |
| UC-CRUD-07 | Concurrent update | stale writer is rejected | writer must reread and reconcile |
| UC-CRUD-08 | Immutable field update | identity and history cannot be rewritten | correction uses an additive governed update |
| UC-CRUD-09 | Artifact divergence | used version remains; review flag is added | reviewer decides whether knowledge remains applicable |
| UC-CRUD-10 | Processed ingress | required processing proofs and CRUD path | minimization preserves sufficient meaning |
| UC-CRUD-11 | Raw ingress | no Record is created | privacy or reprocessing decision is recorded |
| UC-CRUD-12 | Current-use promotion | state, maturity, staleness and review gates pass | current applicability and authority are accepted |
| UC-CRUD-13 | Stale current-use | promotion is blocked without mutation | revalidation scope is defined |
| UC-CRUD-14 | Migration preflight | missing or invalid versions block | mapping preserves meaning and rollback |
| UC-CRUD-15 | Fingerprint audit | Record and ledgers must agree | hash scope and inaccessible frontier are interpreted |
| UC-CRUD-16 | Archive/tombstone | archive is versioned; history remains | retention and dependency impact are accepted |
| UC-CRUD-17 | MCP retry | idempotency produces one mutation | retry cannot create a second decision |
| UC-CRUD-18 | Bypass attempt | unsupported write and direct normalizer write are blocked | no exceptional route circumvents governance |

## Execution gates

1. Run `validate_v3_crud.py` and the existing V3 validators.
2. Run `validate_v3_crud_use_cases.py` and preserve all negative cases.
3. Run the semantic review cases with sanitized evidence and record an outcome
   of `accepted`, `provisional`, `needs_review`, `blocked` or `rework_required`.
4. Confirm that all Record writes in the implementation route through the CRUD
   module; operational queue and audit files remain separate metadata writes.
5. Run the complete suite twice, inspect the diff, and verify that no V2.2
   behavior, vault cache or real vault was changed.

The test package proves the boundary and the completeness of review records. It
does not authorize migration, publication, V3 activation or remote writes.
