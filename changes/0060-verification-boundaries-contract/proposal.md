# Change Set 0060: make verification boundaries executable

## Intent

Turn the existing verification-boundary prose into a checked registry. The
registry records what each deterministic check can prove and what remains a
semantic, human, source, or host decision.

## Scope

- add `docs/verification-boundaries.yaml`;
- add `scripts/validate_verification_boundaries.py`;
- connect the registry to the existing boundary validator;
- clarify that proof boundaries do not authorize writes or prove semantic truth.

## Non-goals

This Change Set does not create a universal runtime barrier, a semantic truth
engine, or a source-authenticity guarantee.

## Status

Implemented locally; validation and review remain required before publication.
