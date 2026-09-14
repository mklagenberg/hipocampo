# Change Set 0097 — V3 F0 typed outcomes and contextual blocking

## Intent

Represent incomplete proof transparently while retaining contextual fail-closed
behavior for sensitive purposes.

## Scope

Add typed F0 outcomes, hardcode review and fixtures for partial,
authorization-required and blocked results.

## Acceptance criteria

- incomplete proof is not silently treated as success;
- blocking depends on phase and purpose;
- semantic limitations remain explicit.
