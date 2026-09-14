# V3 candidate — documentation architecture and local extensions

**Status:** unreleased V3 candidate. This document does not duplicate or
replace the released `SPEC.md`.

## Authority layers

| Surface | Scope | Authority |
|---|---|---|
| `SPEC.md` in the methodology repository | canonical methodology contract | normative |
| accepted Decision Records | durable choices within their scope | normative |
| `hipocampo.yaml` in a vault | identity, entity, role, version and policy declarations | normative for that declaration |
| local vault contract and `AGENTS.md` extensions | vault-specific restrictions and procedures | additive or more restrictive |
| skill | discovery and procedural adaptation | operational, not a substitute source |
| `README.md` | human explanation, orientation and presentation | non-normative |
| research and evidence | reasoning and verification support | non-normative |
| knowledge content | governed data | not a methodology rule source |

## Local extension rule

A vault may extend the methodology for its own entity, scope, privacy,
retention, circulation or operational cadence. A local extension may add a
requirement or make a rule more restrictive. It may not weaken an invariant,
silently redefine a canonical term, or create a competing source of truth.

## Discovery

Before a normative operation, the skill locates the methodology contract,
accepted decisions, target manifest, local instructions and applicable local
extension. A missing or conflicting source is reported; the agent does not
resolve the conflict by choosing the newest README or skill copy.

Both the methodology repository and each vault have a README. The README is
written for humans: it explains and presents what the repository contains. It
does not become normative merely because it is easy to read.
