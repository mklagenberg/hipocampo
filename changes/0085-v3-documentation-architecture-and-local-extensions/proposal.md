# Change Set 0085 — V3 documentation architecture and local extensions

## Intent

Implement D5.3 as a candidate architecture for methodology, vault and
human-facing documentation surfaces.

## Scope

Define authority layers, local extension boundaries, README purpose and
source-discovery behavior. This does not create or migrate a real vault.

## Acceptance criteria

- canonical SPEC and accepted decisions are identified;
- vault extensions are additive or restrictive only;
- README is explicitly non-normative and human-facing;
- local manifest and instructions are discoverable;
- conflicts are reported rather than silently resolved.

## Compatibility and recovery

The active v2.1.1 specification remains authoritative for released instances.
Removing the candidate documentation does not alter vaults.
