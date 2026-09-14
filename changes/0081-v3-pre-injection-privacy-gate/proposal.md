# Change Set 0081 — V3 pre-injection privacy gate

## Problem

Checking privacy only at the final response is too late. Retrieval,
compilation, injection, cache, export, embedding and telemetry can each cross
a boundary before a response exists.

## Proposed contract

Add a distributed, explainable gate before each relevant passage of
information. It evaluates identity, destination, purpose, sources, scope and
minimization, fails closed on objective non-evaluation, and does not pretend
to resolve semantic truth deterministically.

## Risks and compatibility

The gate is a methodology and candidate-runtime boundary, not a universal
security guarantee. External providers and hosts remain separate enforcement
surfaces.

## Acceptance criteria

- every declared passage has a gate;
- direct and derived secrets, titles, links, cache, embedding, export and
  telemetry are covered;
- bypass attempts are detected;
- inaccessible-source existence is not disclosed;
- semantic interpretation remains explicitly bounded.
