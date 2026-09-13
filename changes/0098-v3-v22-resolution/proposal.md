# Change Set 0098 — V3 supersession and V2.2 resolution

## Intent

Make V3's normative sovereignty over V2.2 explicit and provide a complete,
traceable disposition for the capabilities introduced by V2.2.

## Scope

This Change Set covers the V2.2-to-V3 resolution matrix, the V3 crosswalk,
the candidate `2.x -> 3.0` migration boundary, and the canonical naming of
the compatibility state `compatible_with_upgrade`.

It does not migrate vaults, modify the published V2.2 tag, publish a release,
install a skill, access third-party vaults or activate V3.

## Acceptance criteria

- V3 sovereignty is recorded in a Decision Record;
- Change Sets `0058` through `0069` each have one explicit disposition;
- every V2.2 capability is either mapped to V3 or has a named retained,
  deferred or retired boundary;
- `MIGRATIONS.md` describes the candidate `2.x -> 3.0` migration without
  claiming that migration has occurred;
- the compatibility state vocabulary is internally consistent;
- the published V2.2 release remains historically immutable.
