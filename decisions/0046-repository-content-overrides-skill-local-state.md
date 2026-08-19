# 0046 — Repository content always overrides local skill state (Invariant 6)

**Status:** Accepted

## Context

The personal skill copy that operates a Hipocampo instance carries state outside the repository itself: `skill/references/personalization.md`'s hand-filled bootstrap-seed pointer (`decisions/0044`), and the ephemeral sensory-memory cache vault discovery populates fresh each session (`decisions/0044`, `SPEC.md` section 12-A). The repository declares the same category of information authoritatively, in its own structured files: `AGENTS.md`'s local extensions and instance-type declaration (section 11), the `hipocampo.yaml` manifest (`decisions/0033`/`0041`), and now `profile.md` (section 12-B, `decisions/0045`).

Nothing in `SPEC.md` states which one wins when the two disagree. This is a real, not hypothetical, drift risk: a user's local skill copy can go stale relative to the repository (the repository was updated by another session, or by hand, and the local copy never re-read it), or can be hand-edited by the user in a way that no longer matches what the repository actually declares. Without an explicit rule, an agent has no principled way to resolve the disagreement — it would have to guess, silently pick one, or ask every time, none of which is acceptable given section 14's "insufficient evidence" posture already rejects silent guessing for exactly this class of problem.

This gap is structurally the same kind of trust-boundary question the existing invariants already resolve — never physically delete content, always separate access per repository, never write without an explicit request — not a feature-specific implementation detail scoped to one artifact.

## Decision

**New Invariant 6:** content declared in the repository always overrides locally-cached or customized skill state.

**Scope: generic, not a closed list.** The invariant applies to any content the repository declares — `AGENTS.md`, the `hipocampo.yaml` manifest, `profile.md`, and any future structured repository file — not a fixed list of file names. A closed list would need amending every time the methodology gains a new structured file; `profile.md` itself is a concrete example of exactly that gap, since it did not exist when this need was first identified and would have been missing from an earlier, narrower list.

**Condition for the invariant to resolve without ambiguity.** No two repository-side files may declare the same field. If two repository files ever disagreed with each other, "which one overrides which" would have no clear answer even with this invariant in force — the invariant only resolves skill-versus-repository conflicts, not repository-versus-repository ones. This is the reason `AGENTS.md`'s "instance type" field is recommended for retirement (`SPEC.md` section 2-C, `decisions/0041`) rather than kept as a duplicate echo of the manifest's `instance.entity`/`instance.role` — not a stylistic preference, but a precondition this invariant depends on.

**A different axis from the agent precedence hierarchy.** `SPEC.md` section 8 already defines an agent precedence hierarchy (explicit conversation request → documented local instance extension → base `SPEC.md` rule → default convention). That hierarchy governs which *rule* applies once the instance's own documented state is known. Invariant 6 governs a prior, separate question: whether the *local skill copy's* view of that state can be trusted at all, or whether the repository itself must be re-read. The two are not in tension — the precedence hierarchy's second tier already assumes accurate knowledge of the instance's own documented extensions; Invariant 6 is what keeps that assumption honest when the skill's local copy might be stale.

## Rationale

Formalizing this as an invariant, rather than as an implementation note buried inside the `hipocampo.yaml` manifest DR (`decisions/0033`) or the discovery DR (`decisions/0044`), follows the same reasoning that elevated never-physically-delete, per-repository access separation, and no-write-without-request to invariant status: each is a trust boundary the whole methodology depends on holding in every instance, not a detail specific to one feature. A user's local skill copy is, by construction, outside version control and outside any instance's own review cycle — the one place in the whole methodology where "what the agent currently believes" can silently diverge from "what is actually declared" without any of the existing rituals (frontmatter audit, structural audit, REM) ever seeing it, because none of them operate on the skill copy at all. An invariant closes that blind spot generically, rather than leaving it to be rediscovered and patched file by file as each new structured artifact is added.

## Discarded alternatives

- **Leave it as an informal note inside `decisions/0033-hipocampo-yaml-per-vault-manifest.md` (or `decisions/0044-vault-and-entity-discovery.md`), rather than a formal invariant.** Discarded — this would bury a trust boundary the whole methodology depends on inside a DR scoped to one specific artifact, and would not obviously apply to `profile.md` or to any future structured file without a separate note being added each time.
- **A closed list naming the specific files this rule covers (`AGENTS.md`, `hipocampo.yaml`).** Discarded — `profile.md` needed the identical rule and was not on an earlier draft of this list; a closed list requires amendment every time a future structured file is introduced. The generic wording adopted here covers `profile.md` today and any future structured file without further amendment.
- **Resolve drift only by removing `AGENTS.md`'s "instance type" field outright, instead of adding a generic invariant.** Discarded — removing one specific duplicate field addresses one instance of the problem (already recommended for retirement by `decisions/0041`) but does not establish the general principle a future duplicate-field situation would need. The invariant and the retirement recommendation are complementary, not substitutes for each other: the invariant is the general rule, the retirement recommendation is its concrete first application.
