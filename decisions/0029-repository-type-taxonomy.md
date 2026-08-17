# 0029 — Repository type taxonomy: domain × exposure tier

**Status:** Proposed

## Context

Hipocampo already operates, in practice, with content repositories organized by two informal criteria — ownership (`decisions/0002`, personal vs. corporate) and access-restriction level (confidential vault vs. more open repository) — without either of these two criteria ever having been formally named. This became evident when starting to bring the methodology into conformance with MODA: MODA's scaffolding contract requires every scaffold profile to declare the legitimate instance variant it generates, and the audit (section 4.14) points out that poorly defined instance profiles tend to turn into loose templates without a shared contract. We need formal vocabulary for the content-repository variants Hipocampo already produces — not a new structure.

The starting point was a proposal with five named tiers: pessoal-confidencial, pessoal-público, empresa-confidencial, empresa-estruturante, empresa-público — "estruturante" described as "knowledge to be curated by leadership," alongside "confidencial" described as "knowledge only leadership can access." The two descriptions share the same access audience (leadership); the difference is one of intent (remain confidential vs. be a candidate for future publication), not of who can read it.

## Decision

Two orthogonal axes, both already existing in practice, now formally named (`SPEC.md`, section 2-C):

1. **Ownership domain** (`decisions/0002`, unchanged): `pessoal` or `empresa`.
2. **Exposure tier**, within each domain: `confidencial` or `público` — two values in both domains, no third tier.

The four pairs map, without any new repository, to the four real content repositories Mau already operates:

| Domain | Tier | Repository |
|---|---|---|
| pessoal | confidencial | hipocampo-personal-vault |
| pessoal | público | hipocampo-concepts |
| empresa | confidencial | hipocampo-company-vault |
| empresa | público | hipocampo-company |

"Estruturante" doesn't become a fifth physical repository. It becomes a new, optional frontmatter field, relevant only within the `empresa-confidencial` repository: `curation_status: staged | permanent` (`SPEC.md`, section 2). `staged` marks a document as a candidate to eventually be promoted to `empresa-público`, after leadership curation; `permanent` (default) marks content that is confidential by nature, with no expectation of future publication. Promote's behavior regarding this field is handled separately, in `decisions/0030`.

The formal declaration of which domain+tier a specific repository implements remains, for now, in the `AGENTS.md` "instance type" field that already exists (`decisions/0022`) combined with the tier known informally by the operator — and will be formalized by an instance manifesto when the methodology's MODA conformance work incorporates scaffolding (a separate phase, not yet executed).

## Rationale

Reusing the four real repositories instead of proposing a new theoretical model follows the same principle that motivated `decisions/0002` (don't design structure before the real need appears) and the `BEST-PRACTICES.md` item ("`category` is born later, never before" — the same reasoning applied here to a repository instead of a folder). "Estruturante" and "confidencial" describe the same access audience — per invariant 4 (`SPEC.md`, section 8: access separation is always by repository), a new repository is only justified when *access* changes, not when only *intent* changes. Treating this as a frontmatter field instead of a repository avoids generating an empty, low-volume repository just to represent a lifecycle stage.

The absence of a third personal tier reflects a real asymmetry: "estruturante" only makes sense when whoever decides to publish (leadership) is structurally different from whoever wrote it (the employee) — a situation exclusive to the `empresa` domain. In the `pessoal` domain, author and curator are the same person; there is no "awaiting third-party curation" stage to mark.

## Discarded alternatives

- **A fifth physical repository for "estruturante."** Discarded — same access audience as `empresa-confidencial` today, with no real GitHub enforcement difference that justifies separation (invariant 4); contrary to the principle of not structuring before the real need.
- **A symmetric third tier in the personal domain ("pessoal-estruturante").** Discarded — there is currently no curator structurally different from the author in the personal domain that would justify a curation stage before release; without a real use case, it would be premature structure.
- **Fold the tiers into the existing `visibility` field.** Discarded — `visibility` already solves a different, well-defined problem (what, once you already have access to the repository, can be used without additional restriction); mixing the two concepts (repository tier vs. intra-repository reading convention) would reduce the clarity of both fields.
