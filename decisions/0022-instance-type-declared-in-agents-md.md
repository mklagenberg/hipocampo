# 0022 — Instance type (corporate/personal) explicitly declared in AGENTS.md

**Status:** Accepted

## Context

The sensitive-data policy by instance type (section 2-A, DR0009) differentiates what a *corporate* instance can store from what a *personal* instance can. The weekly structural audit (section 5-C, DR0019) has, among its three functions, checking for sensitive-data leakage "against the policy by instance type" — but never specifies where this instance type is declared.

In that same section 5-C, the placement function resolves this correctly: it is explicitly anchored in the scope declared in `AGENTS.md` (section 11, DR0015). The sensitive-data-leakage function does not have the same anchoring — it works today only because the agent contextually infers which repository is which, which is exactly the kind of decision that SPEC.md section 8 says should never remain implicit ("always documented, never implicit"). Raised by Mau while reviewing the structural audit design ahead of the skill rewrite (G2).

## Decision

The `AGENTS.md` of every instance explicitly declares, within the "Repository scope" block (section 11), the **instance type**: `corporativa` or `pessoal`. This field is the criterion that the structural audit (section 5-C, function 3) and any new document read/write use to know which variant of the sensitive-data policy (section 2-A) applies to that repository — never implicitly inferred by the agent from the repository name or conversation context.

SPEC.md, section 2-A, gains a closing sentence pointing to this field. SPEC.md, section 5-C, has function 3 rewritten to cite the same field, in the same pattern already used by function 2 (placement).

## Rationale

This closes a real asymmetry within section 5-C itself: two of the three functions (placement and, now, sensitive-data leakage) become anchored in the same declared artifact (`AGENTS.md`), instead of one of them depending on agent inference. It reuses a field that is already required to fill in (section 11) instead of creating a new mechanism — the instance type was already, in practice, an implicit decision baked into which repository exists (`-company`/`-vault` vs. `-personal-vault`); this DR only turns that decision into a read field, not an assumed one.

## Discarded alternatives

- **Infer the instance type from the repository name (suffix `-company`, `-personal-vault`, etc.).** Discarded: it depends on a naming convention never formalized as a rule, and breaks silently if a repository is ever renamed or a user chooses a name different from the standard pattern.
- **Create a new frontmatter field instead of using `AGENTS.md`.** Discarded: instance type is a property of the entire repository, not of an individual document — frontmatter already has `owner` fulfilling part of that role per document; duplicating the information in every file would be redundant and prone to divergence.
