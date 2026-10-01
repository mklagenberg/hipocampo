# Change Set 0114 — V3 Record content and Artifact accessibility boundary

## Intent

Implement the accepted V3 clarification that a Record is content-bearing and
that access to a referenced Artifact is independent from access to the
persisted Record prose.

## Scope

This Change Set synchronizes the Record, Artifact and Search & Progressive
Disclosure contracts, local runtime gates, sanitized deterministic fixtures,
semantic review candidates, taxonomy and validation bindings. The runtime
requires non-empty prose content for a Record, preserves that content when a
linked Artifact is unavailable, and blocks only when the Record content read
itself is unavailable. Artifact reconstruction remains an audit or
revalidation operation and is never a display or search prerequisite.

Historical Decision Records and the historical semantic baseline remain
unchanged. The new semantic Search case is candidate-only and remains pending
human confirmation. The work is limited to the unreleased V3 candidate and
does not activate V3, alter v2.2.0, read real vault caches, use MCP, migrate,
publish, deploy or release.

## Authority and compatibility

Decision Record `0109-v3-record-content-independent-of-artifact-accessibility`
is the governing V3 clarification. It applies Constitution clauses 2.1, 2.2,
2.3, 2.6, 2.8, 2.9 and the action order in section 4. Existing Decision
Record `0073` and Search Decision Record `0108` remain historical authority
and receive additive implementation clarification through this Change Set;
they are not silently rewritten. SemVer is `none` because this is an
unreleased candidate change.

## Acceptance criteria

- every Artifact-linked Record fixture carries non-empty prose and an explicit
  `format: prose` representation;
- CRUD validation rejects missing or empty Record prose;
- Artifact unavailability produces an explicit limitation without blocking a
  readable Record, while unavailable Record content fails closed at L0;
- Search does not fetch or reconstruct an Artifact for display and preserves
  the canonical CRUD read boundary and `mutation: none`;
- deterministic and semantic Search/Artifact fixtures, engine bindings,
  taxonomy, vocabulary and constitutional basis are synchronized;
- historical semantic reviews remain unchanged and the new Search semantic
  candidate remains pending human confirmation;
- the focused validators, integrated engine suite, semantic validators,
  structural validators, contract validators and Change Set validator pass;
- no real vault, private capture, remote repository, MCP surface, release or
  deployment state is changed.

## Recovery

Reverting this Change Set restores the previous candidate interpretation and
test inventory while leaving accepted Decision Record `0109` and historical
records intact. No vault migration or irreversible operation is part of this
Change Set.
