# 0006 — Contribution credits for historical content

**Status:** Accepted

## Context

Work content migrated from systems that predate Hipocampo originated from collective authorship never tracked by individual — entire teams (leadership, sales, pre-sales) produced documents without anyone recording "who wrote this sentence." Forcing a single personal `author` per document in these cases would be arbitrary. The invariant "`author` is always a person" (SPEC.md, section 8) doesn't change — what's missing is a mechanism for when the actual person can't be recovered from the source.

## Decision

A `CONTRIBUTORS.md` file (per instance, where teams make sense) defines named, already-dated sections — for example `## comercial-empresa-q1-2026` — each with a short description of context/history and the list of people with their position. `author` and `contributors` in the frontmatter can reference that section directly via `@section-name` (e.g., `author: "@comercial-empresa-q1-2026"`), in addition to continuing to accept the existing person format (`"Real Name - @github-username"`). Temporal resolution (a "snapshot in time") is embedded in the section name itself — whoever drafts the document chooses the already-dated name, with no dynamic resolution algorithm.

**Scope: historical/migrated content only.** A new document, created already within a Hipocampo instance, always has a real-person `author` (whoever actually wrote or is refining that knowledge) and `contributors` determined by commit or explicit citation — the team mechanism doesn't apply to new content.

## Rationale

Reuses the `@mention` pattern, already familiar from GitHub itself, instead of inventing new syntax. Eliminates the need for a dynamic date-resolution pipeline — the date is already in the section name, not in a range field that needs to be computed. There is real precedent outside the Git ecosystem: the Writers Guild of America credit system formally distinguishes a team that worked together ("&") from authorship separated in time ("and"); the `<collab>`/`<collab-wrap>` tag from JATS/Crossref resolves collective authorship in scientific publishing; Schema.org accepts `Organization` as a value for `author`. The most documented risk of this kind of mechanism — dilution of accountability when `author` is just a generic group, a concern converging in both RACI literature and scientific hyperauthorship literature — is mitigated by the scope: restricted to the stock of migrated content, finite and shrinking as documents are revised, never recurring in new content.

## Discarded alternatives

- **A single credit unit with a list of periods nested in YAML, resolved by a date algorithm at build time.** Discarded due to complexity disproportionate to the project's stage — plain Markdown, with no established CI/CD pipeline.
- **`$alias:` syntax** (already used for cross-repository `related`/`context_anchor`). Discarded for this case: `@name` is more readable for a reference within the same repository to a section of a file, a different use than what `$alias:` resolves (an entire document in another repository).
- **Use CRediT (Contributor Roles Taxonomy) as a direct precedent.** Discarded as the basis for the mechanism — CRediT describes what each author did (contribution role), not who counts as an author (identity), a different axis than what this mechanism resolves.
