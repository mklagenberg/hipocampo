# Change Set — 0059: verification boundaries and coverage registry

## Summary

Adds a canonical registry distinguishing deterministic checks from cognitive,
human, source-specific, and environment-specific responsibilities.

## Class and SemVer

**Normative; MINOR candidate.** The Change Set makes existing limits explicit
and adds a validation-boundary registry. It does not claim universal runtime
enforcement or change existing vault fields.

## Proposed contract

`docs/verification-boundaries.md` is the human-readable registry and
`scripts/validate_boundaries.py` checks that the declared mechanisms and limits
remain present. A missing runtime barrier, semantic extractor, or safe
nominal-citation detector remains a reported limitation.

## Acceptance criteria

- Each current deterministic validator is named with its actual boundary.
- Provenance, compatibility, authority and destructive-action limits are
  explicitly distinguished.
- The registry does not claim a universal runtime enforcement layer.
- The boundary validator and existing validators pass.

## Compatibility and migration

No existing vault migration is introduced. This is a contract clarification and
new registry capability; publication classification remains subject to review.

## Recovery

Correct an inaccurate boundary through a reviewed Change Set. Never broaden a
validator's claim merely to make an evaluation pass.

## Status

`proposed`
