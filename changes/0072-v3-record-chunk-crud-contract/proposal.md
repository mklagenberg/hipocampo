# Change Set 0072 — V3 Record–Chunk CRUD and Package integrity

## Intent

Implement and exercise the governed CRUD boundary for Record, Chunk,
Collection, Artifact, and Package while preserving parent context, stable
identity, monotonic restrictions, and explicit partial selection.

## Scope

This Change Set adds the unreleased V3 CRUD contract, in-memory contract
primitives, positive/negative fixtures, and a validator. It does not execute a
real vault migration, send a remote Package, change an Artifact in an
external store, or introduce the deferred general projection layer.

## Acceptance

- valid Records persist with active Collection membership;
- orphan and duplicate Chunks are blocked;
- Chunk reads carry parent context;
- weaker visibility and staleness restrictions are blocked;
- physical moves preserve identity and logical membership;
- partial Packages are explicit and carry context and restrictions;
- incompatible destinations and stale current-use sends fail closed;
- Artifact version changes do not rewrite a Record silently.

## Compatibility and recovery

V2 instances remain readable; no migration runs. Reverting the Change Set
removes the candidate CRUD tooling without deleting historical decisions or
changing a vault. V3 publication still requires the release gate and a
separate migration plan.

