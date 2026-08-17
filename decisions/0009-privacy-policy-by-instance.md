# 0009 — Privacy policy and sensitive data by instance type

**Status:** Accepted

## Context

Throughout Batch 4, successive migration sub-batches ran into one-off decisions about the names of colleagues/clients, performance reviews, health data, and internal financial figures (salary, vendor, project) — handled ad hoc, with no explicit rule in the methodology. Sub-batch F, the largest one (82 work-context documents), made the pattern visible and unsustainable: without a declared policy, each instance risks applying the sensitivity criterion divergently, or reinventing the same decision repeatedly. SPEC.md defines schema, temporality, and memory layers (section 5-A, DR0008), but had never defined what can or can't be written, by data type, depending on who the instance's owner is.

## Decision

Hipocampo adopts a sensitive-data policy differentiated by instance type (SPEC.md, new section 2-A):

A corporate instance (`owner` is an organization, not an individual person) never stores, regardless of `visibility` level, even at the most restricted tier:

- Content from contracts or NDAs.
- Performance review of an identifiable individual.
- Notes about the health of any person — the instance owner or a third party.
- Personal data of any person: password, personal address, personal phone or email, name of a relative.
- Salary figures, amounts paid to a vendor, or project/contract figures — with a single exception: a figure that represents a business result delivered to a client in a `type: case` (revenue generated, cost avoided) can be kept as an absolute value, because it is the very product of the case, not internal financial exposure.
- Quantified internal learning (e.g., process savings) is recorded as a percentage variation, never as an absolute value.

Financial data about a third party that is not a direct vendor/business partner (e.g., revenue of a competitor or potential partner, extracted from a verifiable public source, used as market intelligence) doesn't count as "vendor or project figures" and can be kept — as long as the public source is explicitly cited in the document.

Full name, job title, professional email, phone, or professional address — of a colleague or a client contact — are permitted in a corporate instance, as long as accompanied by a year/date citation: the record is always a dated snapshot, never a presumed current state.

Personal matters of any individual (health, personal financial situation) never go into the corporate instance — always into the relevant person's personal instance, if one exists.

Technical detail of a vulnerability or active exploit (attack payload, query/dork that reveals the compromise, credential, exploitable endpoint) is never recorded verbatim, in any instance — even confidential/restricted. What gets recorded is the fact (existence of the flaw, category, date of the finding) and the response given, never the material that would reproduce or confirm the attack for whoever reads the document later.

When an entire document structurally depends on a banned data type (it can't be adapted by removing just the problematic passage), the agent doesn't decide alone between publishing anyway or discarding it — it flags the violation to the human responsible for the instance and waits for an explicit decision.

## Rationale

Closes a real gap, discovered operationally during the migration of work content (sub-batch F): 82 documents contained everything from sensitive HR data to vendor rates to a relative's name in a loose note, with the methodology giving no prior criterion to decide what fit. Without this policy, judgment is left entirely ad hoc per sub-batch, which doesn't scale and creates inconsistency between different instances of the same method. The "corporate vs. personal instance" distinction already exists implicitly in the multi-repository architecture (`-company`/`-company-vault` vs. `-personal-vault`); this DR just makes explicit what was already the design intent.

## Discarded alternatives

- **Leave it as an implicit criterion, decided document by document.** Discarded: this is exactly the problem that motivated this DR.
- **Ban all financial figures from the corporate instance, with no exception for case impact.** Discarded: a business case with no quantified result loses most of its value as reusable knowledge. The distinction between "what the client gained" (allowed) and "what the organization charged/paid internally" (prohibited) preserves the value without the risk.
- **Treat performance reviews as `restricted`/vault-only, instead of banned.** Discarded: even the highest confidentiality level is still an organization repository — performance data of an identifiable individual doesn't belong to any corporate tier, only to the personal instance of whoever manages that person, and even there it would require strong de-identification.
