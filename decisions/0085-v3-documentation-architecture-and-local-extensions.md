# 0085 — V3 documentation architecture and local extensions

**Status:** Accepted for the unreleased V3 contract

## Context

Methodology documentation and vault documentation serve different audiences
and authority boundaries. Humans need readable entry points, while the skill
needs an explicit path to canonical norms and controlled local extensions.

## Decision

The methodology repository owns the canonical `SPEC.md` and accepted
Decision Records. A vault may add local extensions that are additive or more
restrictive, but may not weaken invariants or redefine canonical concepts.
README files exist in both methodology and vault repositories for human
explanation and presentation; they are not normative. The skill discovers the
official sources before operating.

## Consequences

One normative methodology source remains, while vaults can express their own
privacy, scope and operating constraints without creating a competing SPEC.
## Rationale

Separating human-facing explanation from normative sources prevents README
prose from becoming a competing specification while allowing a vault to add
local rules without weakening methodology invariants.

## Discarded alternatives

- Treating README as a normative source.
- Allowing vaults to replace the canonical methodology specification.
- Duplicating the full methodology specification in every vault.
