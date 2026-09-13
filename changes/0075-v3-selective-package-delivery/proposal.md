# Change Set 0075 — V3 selective Package delivery

## Problem

The V3 candidate now resolves entity, vault profile, Source, roles and governed
splits, but it still needs an executable boundary for selective delivery,
authority succession, conciliation, conflict-bearing Packages and
revalidation.

## Current contract

`DEC-0029` and `DEC-0030` require one active authority per entity/scope,
hereditary succession, explicit conciliation, coexistence of conflicting
perspectives in Chunks, and purpose-sensitive Package gates. Delivery is not
promotion and cannot silently transfer authority.

## Proposed contract

Add bounded in-memory primitives that:

1. resolve the first accessible active authority in an ordered chain;
2. classify conciliation without merging sources;
3. distinguish source authority from the Package-generating vault;
4. allow conflict-bearing Packages for discussion/review/analysis;
5. block current-use delivery when authority, conflict or staleness is
   unresolved, subject to explicit destination acceptance of multiple
   perspectives;
6. record sent/received Package ledger context.

## Discarded alternatives

- treating Package generation as promotion or authority transfer;
- selecting the newest or most accessible source as authority;
- forcing a single synthesis from conflicting perspectives;
- retaining only the source authority and omitting the generating vault;
- allowing current-use delivery to bypass conciliation or revalidation.

## Risks and compatibility

This is an unreleased V3 candidate and has no effect on v2 instances. The
implementation is in-memory and does not claim remote authorization,
transport, migration or runtime enforcement. If rolled back, source IDs,
Records, Chunks and prior evidence remain intact; only the candidate delivery
implementation and its fixtures are removed.

## Acceptance criteria

- ordered authority succession is deterministic and fail-closed;
- source and Package authorities are both present and distinct;
- conciliation preserves source IDs and conflict state;
- Package purpose controls current-use delivery;
- stale material and missing authority block current-use delivery;
- sent/received ledger context is explicit;
- fixtures and validators pass.
