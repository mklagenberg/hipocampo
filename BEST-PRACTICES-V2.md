# Hipocampo — Best Practices

This guide is for those who have already read [Getting Started](GETTING-STARTED.md) and want to use Hipocampo well — not just correctly, but in a way that stands the test of time. It was born from real mistakes made in a migration of hundreds of documents (not from theory) — every recommendation here has already been tested, broken, or learned the hard way by someone before you.

If you want the full normative text, it is in [SPEC.md](SPEC.md). Here it is the "and in practice, what do I do?".

## 1. Using it well day to day

**Not every decision needs a Decision Record.** If the question is "why did this client go to the vault and not to the general repository", that is a decision of your instance — it becomes a regular document with `type: decision`, on the content side. A real Decision Record (the `decisions/` folder of `hipocampo`) is reserved for a change in the methodology itself — schema, rule, agent behavior. Confusing the two leaves `hipocampo` bloated with decisions that matter to no one outside your instance.

**An empty `related` field is almost always laziness, not absence of connection.** If a document's text mentions another by name, that is a connection that deserves to go into the `related` field — it costs nothing and saves a manual search later. The most repeated lesson during the migration of real content was exactly this: dozens of documents referenced each other in the body text without any structured link.

**`category` is born afterward, never beforehand.** Do not create a `crm/` or `financeiro/` subfolder just because you imagine you'll need it one day. Wait to accumulate a few documents on the same topic and only then promote to a subfolder — the same reasoning applies to creating a new `type` value. Too much structure, too early, is just as bad as no structure at all.

**`type: framework` is for methodology of your own, not for every well-written document.** This type exists because it changes who owns the content (you, even when applied in a work context — see `DISCLAIMER.md`). If the document is just a good technical guide, without that question of ownership at stake, it is `reference`, not `framework`.

**Migrating old content? Three guaranteed pitfalls:**
- The index document of an old folder should almost never be copied literally — it usually accumulates names, links, and context that do not belong in the new place. Rewrite it as a clean `README.md`.
- A generic document that has turned into several more specific documents needs to become a "tombstone": `status: superseded`, with `superseded_by` listing all the children — never two active documents saying the same thing.
- If the old collection did not have a `date` field, do not make one up — pull the date from the file's first real commit (git history), it is more reliable than any estimate.

**Authorship of migrated content without a clear owner (whole team, no individual record) has its own mechanism** (`CONTRIBUTORS.md` + `@section-name`, see `decisions/0006`) — but that is only for the past. A new document, written today, always has a real author: the person who wrote it or directed the writing. Do not force this mechanism onto new content just because it seems more neutral.

## 2. Privacy is not a feature, it's a foundation

Hipocampo does not treat privacy as one more label in the frontmatter — it treats it as part of the design. It's worth understanding why, because this changes how you should think when writing any new document in a work instance.

**What never goes into a corporate repository, summarized:** a contract or NDA, a performance review of an identifiable person, any health note (yours or a third party's), personal data (password, address, personal phone/email, relative's name), and salary, vendor, or project figures — with a single exception: a business outcome delivered to a client in a case study (how much revenue it generated, how much cost it avoided) can remain as a real number, because it is the very product of the work, not internal financial exposure. The name, role, and professional contact of a colleague or client are allowed, always with the reference year alongside — it is a dated snapshot, never a presumed current state. Full detail is in `decisions/0009`.

**"Depersonalizing" a document is not just swapping out the name.** Before considering a document safe to publish, ask three things, in the order of a real anonymization technique (we did not invent this, it is the standard used by European regulators):

1. **Isolation** — even without the name, can this record be isolated as belonging to a specific person/company, just by looking at the rest of the document?
2. **Linkability** — can this document be cross-referenced with another one you already have to piece it together?
3. **Inference** — can you deduce who it is, with high probability, just from context (sector, size, time period, project)?

If the answer is yes to any of the three, the depersonalization did not really take — swap out more detail, not just the proper name.

**Sometimes someone has the right to ask that their own name be removed from the repository for good.** This is rare (the item above already reduces this a lot when it happens), but when it is a legitimate request for deletion of personal data, Hipocampo has a process for it (`decisions/0010`): the specific personal content is replaced with a minimal record of what happened (without repeating the data), never simply ignored.

**`visibility` is a reading convention, not a lock.** Marking a document as `confidential` does not technically prevent anyone with access to the repository from opening the file — what actually protects it is GitHub's own permission at the repository level. That is why Hipocampo's architecture separates personal, personal-confidential, corporate, and corporate-confidential into **different repositories**, not folders within the same repository: real GitHub permission is per-repository, so physical separation is the only thing that guarantees that whoever shouldn't see it, really doesn't see it.

**Never write out the "how" of a security flaw verbatim.** If you document that a vulnerability was found, record what and when — never the payload, the query, or anything that would let a later reader reproduce the attack.

## 3. Adopting Hipocampo in a new team or company

**Start by thinking about how many repositories you need, not how many folders.** The reference design is four: one personal and one personal-confidential (for those adopting solo), one for the team/company and one confidential one for the team/company (for those adopting as a group). Not everyone needs all four from day one — but think about the separation of *who has access to what* before writing the first document, because changing this later means moving content between repositories, not just reclassifying a label.

**The confidential repository ("vault") is not "the most confidential place of all" — it's the place for a specific kind of sensitivity.** After you apply the sensitive data policy (item 2 above), what remains a vault candidate is normally qualitative competitive sensitivity — a sales pipeline under negotiation, an internal partnership assessment, a negotiating stance — not financials or a person's evaluation (that is already banned before it even reaches the question "vault or not").

**Name categories as they arise, not with a folder plan ready on day 1.** Same logic as item 1, just now at the scale of an entire organization.

**Don't wire anything up for real until you're sure.** Build the new instance in parallel, without pointing any routine, skill, or colleague at it until you have confirmed yourself that it is ready. It is easier to postpone an activation than to undo the confusion of two systems running at the same time.

**Two mechanical GitHub gotchas that every adopter runs into sooner or later:**
- **"Use this template" only creates a new repository** — there is no way to apply a template retroactively to a repository you already created empty. It also copies the LICENSE from the source template, even when that doesn't make sense at the destination — remove it afterward, that's expected.
- **Installing an AI app (like the GitHub connector) on an organization repository is different from authorizing it on your personal account.** These are two separate permissions: who authorizes (your identity) and who installs (access to the repository itself). If your personal account is not an administrator of the organization, you will need a second account that is, just to do the installation — your personal account's authorization stays the same, no need to redo anything there.

---

*This document is alive — if you find a common mistake that isn't listed here, it probably deserves a new line.*