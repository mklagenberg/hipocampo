# Verification boundaries

This registry separates what the repository can prove mechanically from what
still requires agent reasoning, human review, or an environment-specific
barrier. A green validator never proves truth of content or authorizes a write
on its own.

The structured companion registry is `docs/verification-boundaries.yaml`.
Each entry is required to declare inputs, outputs, deterministic coverage, rule
revision, legacy treatment, limits, and the human or environmental boundary.
`scripts/validate_verification_boundaries.py` checks that contract.

| Concern | Deterministic coverage | Outside the validator | Current mechanism |
|---|---|---|---|
| Repository structure | Decision templates, links, README/CHANGELOG version and schema coverage | Semantic completeness and truth | `validate_hipocampo.py` |
| Declared contracts | Required cross-surface snippets and named consistency rules | Whether prose is semantically sufficient | `validate_contracts.py` |
| Skill package | File set and raw SHA-256 hashes against the package lock | Whether instructions are safe or semantically adequate | `validate_skill_package.py` |
| Compatibility | Declared methodology/skill/vault tuple, required fixture fields, package hashes and explicit states | Reachability of a remote vault and operator acceptance | `validate_compatibility.py` |
| Change Set | Change Set schema and heuristic protected-path coverage | Whether impact claims are semantically accurate | `validate_change.py` plus human review |
| Skill/scaffold documentation | Declared output paths and superseded-field references | Runtime behavior of a host adapter | `validate_skill_docs.py` |
| Provenance | Presence of declared source and release references | Authenticity of an external source unless independently fetched | Human/source-specific verification |
| Precedence cycles | No general universal detector is claimed here | Authority decision in an unusual multi-vault context | Agent reasoning plus review |
| Destructive-action enforcement | No repository-wide runtime barrier is claimed | Blocking a delete or external side effect before execution | Host-specific capability, when available |
| Nominal citations | Placeholder/handle heuristic on explicitly supplied changed files | Legacy corpus, aliases, and identity truth | `validate_nominal_citations.py`; human review and source-specific verification |
| Validation/revalidation loop | Failure classification and stop/revalidate scenarios | Semantic correction and policy intent | `validate_validation_loop.py`; human review and authoritative-source access |
| Bounded enforcement policy | Non-mutating allow/deny/blocked simulations | Real host interception | `validate_enforcement_policy.py`; host-specific adapter |

## Classification rule

Every new verification declares its input boundary, output, rule revision,
legacy treatment, false-positive/false-negative limits, and the human or
environmental decision it cannot replace. A missing barrier is reported as a
limitation and never converted into a passing result by configuration alone.

## Current conclusion

The repository has deterministic validators for its own declared contracts and
package surfaces, a bounded validation-loop decision check, a non-mutating
enforcement simulation, and an opt-in nominal-citation heuristic. It still does
not have a universal runtime enforcement layer or a full semantic vocabulary
extractor. The structured registry makes these limits explicit; it does not
convert a declared boundary into runtime enforcement.
