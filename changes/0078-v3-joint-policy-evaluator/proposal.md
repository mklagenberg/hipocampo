# Change Set 0078 — V3 joint policy evaluator

## Problem

The V3 candidate needs an explicit, explainable boundary where source and
destination policies are evaluated independently before a Package crosses a
vault or entity boundary.

## Proposed contract

Add a bounded evaluator that combines origin authorization and destination
acceptance without allowing either side to erase the other side's restriction.
It returns `permitido`, `redigido`, `provisório` or `bloqueado`, preserves the
reason and purpose, and fails closed on objective identity, boundary or
privacy non-evaluation. Semantic uncertainty remains visible rather than being
forced into a deterministic truth decision.

## Risks and compatibility

This is preparation for the unreleased V3 candidate. It does not implement
remote authorization, transport, migration, host enforcement or publication.
The main risk is confusing an explainable policy result with semantic truth.

## Acceptance criteria

- source and destination gates are independently represented;
- same-entity and cross-entity fixtures pass;
- redaction, provisional and blocked outcomes are distinguishable;
- inaccessible sources are not disclosed through diagnostics;
- deterministic and semantic verification boundaries are documented.
