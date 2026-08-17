# 0014 — Mandatory routine for every methodology release

**Status:** Accepted

## Context

Up to this round, methodology releases (v1.0.0 through v1.5.0) always updated `SPEC.md`/`CHANGELOG.md`/`README.md`, but `hipocampo-toolkit` was never synchronized — its `CLAUDE.md` still declared "Hipocampo version followed: ^1.0.0" even five MINOR releases later. Furthermore, `MIGRATIONS.md` never received real content corresponding to any of these releases — all of them were MINOR, which does not require active migration, but there is no record that this check was consciously performed each time, only the fact that none of them was MAJOR until now. Without a formal routine, both steps remain dependent on someone remembering manually — and, in practice, this has already failed once (the toolkit's `CLAUDE.md`).

## Decision

Every time a new version of `SPEC.md` is published, before considering the release complete:

1. **Migration check.** If the version is MAJOR: `MIGRATIONS.md` gets a new entry with the migration guide from the previous version to this one. If it is MINOR or PATCH: explicitly confirm — even if the conclusion is "no action needed" — that no active migration is required, and record that conclusion in the release's own PR/commit, rather than silently skipping the check.
2. **`hipocampo-toolkit` synchronization.** Review and update `CLAUDE.md` (declared compatibility, e.g. "^1.5.0") and any other toolkit file affected by a new invariant, new section, or new default convention in `SPEC.md`.
3. **Git tag/release.** Create the tag corresponding to the new version — today a manual step performed by whoever maintains the methodology, outside the reach of the writing tools available via MCP.

## Rationale

A methodology release that does not synchronize the toolkit leaves anyone instantiating a new repository with an outdated compatibility declaration from the instance's very first commit — exactly what happened in this round. Formalizing the check, even for the "no action needed" case, prevents the habit of skipping the check from silently taking hold; it is cheaper to record a negative check than to discover, several versions later, that no one has been checking anything.

## Discarded alternatives

- **Leave it as is, ad hoc checking.** Discarded: it produced exactly the divergence that motivated this decision — the toolkit's `CLAUDE.md` stuck at "^1.0.0" for five consecutive MINOR releases.
- **Fully automate via CI/webhook.** Discarded for now: it is outside the scope of the tooling available today (the writing tools available via MCP do not create tags or CI workflows), and decisions about what needs to propagate to the toolkit with each release still require judgment — they are not purely mechanical enough to dispense with review.
