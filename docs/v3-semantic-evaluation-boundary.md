# V3 semantic evaluation boundary

This document describes a reusable evaluation surface prepared for the
unreleased V3 work. It is not the V3 normative contract and does not change
the v2.1.1 frontmatter schema.

## What a semantic fixture tests

Each fixture describes a situation where structure alone is insufficient. It
must state:

- the input and its declared context;
- the expected epistemic or provisional classification;
- the maturity and staleness guard;
- the provenance behavior;
- the negative behavior that must not happen;
- the part that remains human or agent-reviewed.

The fixture may be evaluated against an authorized local corpus. The corpus
remains outside this repository and read-only. The evaluation record stores
only sanitized summaries, source references, hashes when useful, and limits.

## Deterministic boundary

`scripts/validate_semantic_fixtures.py` checks identifiers, required fields,
allowed vocabularies, and explicit review boundaries. It does not decide
whether a claim is true, whether two records should merge, whether a source
is authoritative, or whether a provisional item should be promoted.

Therefore:

- a green validator result means that the test package is well-formed;
- a semantic result must be recorded separately as reviewed, ambiguous, or
  blocked;
- `new`, provisional, stale, or conflicting material must not become current
  factual knowledge merely because it was retrieved or structurally valid;
- no result authorizes a write, migration, promotion, connector access, or
  publication.

See `docs/verification-boundaries.yaml` and
`decisions/0039-minimal-evaluation-scenarios.md`.

