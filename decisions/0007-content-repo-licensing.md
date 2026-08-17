# 0007 — Licensing of content repositories

**Status:** Accepted

## Context

`decisions/0001` covers the Apache-2.0 license for `hipocampo`/`hipocampo-toolkit` — the methodology itself, public. The content repositories (`hipocampo-concepts`, `hipocampo-personal-vault`, `hipocampo-company`, `hipocampo-company-vault`) had no license treatment at all — the original plan specified "License: None." This leaves a gap: without a license file, content falls under restricted copyright by default, with no explicit ownership clause and no effect differentiated by `visibility` level. An instance predating Hipocampo (the owner's Personal Second Brain) had already solved this same problem in an equivalent way.

## Decision

Every Hipocampo content repository gets a `LICENSE` file at the root, a proprietary/confidential model — never an open license —, with an explicit owner: the individual person, in `hipocampo-concepts`/`hipocampo-personal-vault`; the company, in `hipocampo-company`/`hipocampo-company-vault`. New frontmatter field, `license` (SPEC.md, section 2), **always mechanically derived from `visibility`, never set by hand**, using the SPDX `LicenseRef-<idstring>` pattern — a short identifier embedded in the document, with the full legal text only in the `LICENSE` file. Four possible values, one per `visibility` level: `LicenseRef-<Instance>-Public`, `-Internal`, `-Confidential`, `-Restricted`.

## Rationale

Private knowledge bases call for a confidential proprietary model, not an open license — an open license would introduce leak risk and a disclosure obligation that doesn't apply to content repositories that, by invariant (SPEC.md, section 8), are never public. Deriving `license` mechanically from `visibility` avoids divergence between the two layers without duplicating the operational granularity of the confidentiality layer into the legal layer. Embedding the identifier in the frontmatter ensures the document carries its own legal effect even if copied in isolation, outside the context of the source repository.

## Discarded alternatives

- **Keep "License: None" in content repositories**, the original plan. Discarded: without a license file, the legal default is restricted copyright, with no explicit ownership clause and no treatment differentiated by `visibility` — exactly the gap that motivated this decision.
- **`license` as a free-value field, filled in by hand.** Discarded for the same reason that prevents filling `visibility`→legal effect by hand: risk of divergence between the two fields with no real gain in expressiveness.
- **A single license for all content repositories, regardless of owner.** Discarded — `hipocampo-company`/`hipocampo-company-vault` have a different owner (the company) than `hipocampo-concepts`/`hipocampo-personal-vault` (the individual person), so each repository's `LICENSE` needs to state this explicitly; it can't be a single shared text.
