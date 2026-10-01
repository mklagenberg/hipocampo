# V3 maintenance rituals

The rituals remain scoped to one authorized vault at a time. They are
read/assessment workflows, not permission to expand scope or persist changes.
Full V3 state and validation rules remain in the canonical specification and
contracts.

## Order in a daily cycle

1. Run the deterministic frontmatter audit.
2. Review its findings semantically through REM.
3. Present proposed changes and wait for the required human authorization
   before CRUD persistence.

The structural audit runs separately on its declared cadence.

## 1. Frontmatter audit — deterministic

Inspect only the explicitly authorized repository/vault scope. Check declared
schema, required metadata, controlled vocabulary and mechanical freshness
conditions. Do not scan Record bodies as part of the frontmatter-only pass.
Produce findings with source reference, field and rule; do not decide truth,
authority, merge or disposition, and do not write records.

## 2. REM — semantic review and governed change proposal

For each finding or inbox item:

- review context, provenance, entity, scope, vault, authority, privacy, maturity,
  staleness and conflict;
- keep facts, accounts, opinions, memories, inferences, hypotheses,
  recommendations and decision candidates distinct;
- preserve multiple perspectives in separate Records or Chunks where required;
- recommend create, update, archive, supersede, discard or revalidation only
  with reasons, evidence and uncertainty;
- present the complete plan before any mutation.

REM is not an automatic write. Once explicitly authorized, a governed change
must pass semantic review and deterministic validation through canonical CRUD.
Unresolved meaning, authority, privacy or intent stays blocked or
`needs_review` for human decision.

## 3. Structural audit — periodic

Within the confirmed scope, review:

1. **Atomicity:** whether each Record remains one coherent governed unit;
2. **Placement:** whether its entity, vault, scope and Collection are correct;
3. **Privacy, security and provenance:** whether access, minimization,
   redaction and source lineage remain valid;
4. **Lifecycle and freshness:** whether maturity, staleness, conflicts,
   supersession and relevant source versions are represented honestly;
5. **Relationships:** whether Chunk parentage, Artifact versions and
   cross-vault references remain explicit and valid.

Never turn an audit into a broad historical sweep just because a methodology
version changed. Findings are reported first. Moves, splits, merges, state
changes and deletion are governed mutations and require human approval and the
CRUD path.

## Reporting

Separate deterministic findings, AI semantic interpretation, unavailable
evidence and human decisions. State which vault and scope were inspected, the
source/version checked, what was not inspected, and which actions remain
pending. A green structural audit does not establish truth or grant migration
or publication authority.
