# Change Set 0109 — V3 Search & Progressive Disclosure runtime

## Intent

Execute the first local read-only implementation of the Search & Progressive
Disclosure contract from Change Set `0108`, with CRUD-preserving access,
sanitized fixtures, negative cases and cross-engine validation.

## Scope

This Change Set covers the local `v3_search_engine.py` runtime and its
contract-level validator. It exercises items 1–6 of the approved sequence:
contract review, semantic-case review preparation, local implementation, CRUD
integration, expanded tests and V3 contract reconciliation.

The runtime accepts only bounded entity/vault/scope requests, reads Records
through canonical CRUD, returns explicit `L0`–`L4` disclosure, preserves
independent result dimensions, renders prose by default and emits only a
minimal redacted trail. It never writes a Record.

## Review outcome

The contract review required two clarifications: a request must distinguish
the search scope from the vaults the actor is authorized to read, and a search
query must be explicit. These fields were added to the candidate request
envelope. The three semantic cases remain pending human adjudication; the
runtime tests validate guardrails and disposition shape, not semantic truth.

## Acceptance criteria

- valid bounded requests use the canonical CRUD read boundary;
- missing or unauthorized scope is rejected;
- L4 expansion without explicit authorization is blocked at L0;
- stale or inaccessible evidence lowers disclosure and surfaces a limit;
- relevance remains independent from authority and epistemic status;
- prose is the default presentation and structured output requires an explicit
  request;
- no Record or CRUD event changes during search;
- all existing V3, CRUD, constitutional, semantic, structural and Change Set
  validators pass twice.

## Recovery and compatibility

The runtime and fixtures are local candidate artifacts. Removing this Change
Set leaves the 0108 contract and V2.2.0 untouched. No instance migration,
vault read, MCP integration, deploy, release or remote write is part of this
scope.
