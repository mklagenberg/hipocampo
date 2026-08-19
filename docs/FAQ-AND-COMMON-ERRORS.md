# FAQ and common errors

This document brings together two things: questions that come up repeatedly, and instantiation/operation errors already encountered for real in actual repositories running the methodology (not hypothetical). If you have a question or ran into something strange, it's probably already here.

## Common instantiation errors

### "My agent says it can't create the repository itself"

Expected, for the standard Claude.ai/Claude Desktop and ChatGPT connectors — repository creation isn't something either supports, regardless of how broadly you've scoped their repository access (see `docs/getting-started-non-technical.md`, "Connecting your AI tool to GitHub"). Claude Cowork and Claude Code are different — their GitHub connection can create repositories directly. If you're on one of the connector-only tools, create the repository yourself (`docs/getting-started-non-technical.md`, "If your agent can't create the repository itself") and hand the address back to the agent — everything else about instantiation works the same from there.

### "My new repository has an Apache-2.0 license, is that right?" (historical)

No — but this specific bug is no longer possible under the current instantiation model. It described GitHub's old "Use this template" mechanism copying `hipocampo-toolkit`'s own `LICENSE` (Apache-2.0, correct for the methodology/tooling, wrong for **content**) into a newly templated repository — see `decisions/0007-content-repo-licensing.md`. That template mechanism no longer exists (`decisions/0032`): the agent explicitly selects the right `LICENSE` template (`scaffold/license-templates/`) as part of generating the repository, whether it creates the repository directly or you create it manually first (`docs/getting-started-non-technical.md`). Kept here for historical searchability only.

### "My `CLAUDE.md` still says an old version of the methodology"

This means the instance hasn't gone through the release routine (see `decisions/0014-mandatory-release-routine.md`) the last few times the methodology evolved — or nobody updated it manually after instantiating. There is no automatic synchronization between repositories (see `decisions/0002`, multi-repo architecture without replication) — it's the responsibility of whoever maintains each instance to follow the `hipocampo` `CHANGELOG.md` and update the local `CLAUDE.md`. The skill, when installed correctly, helps by warning you when there's a new release — but it doesn't apply the update on its own.

### "I can't create the repository inside my GitHub organization"

Probably a permissions issue, separate from whether your connector can create repositories at all (see the entry above). Creating any new repository inside an organization (instead of your personal account) usually requires an organization admin to enable it, or for you to ask someone with permission to create it on your behalf. It's not a limitation of the methodology — it's a GitHub configuration matter. See the corresponding note in `docs/FUNDAMENTALS.md`.

### "I migrated an old document and just copied the file, is that right?"

No. Migration is never a direct file copy (see `decisions/0011-migration-never-direct-copy.md` and `SPEC.md`, section 10). The content needs to be reinterpreted and rewritten according to the frontmatter schema in force in the current version of the methodology, with correct atomicity, naming, and privacy classification — even if that means splitting an old file into several new ones, or reclassifying `visibility`.

## Frequently asked questions

### Why is a document never physically deleted?

Because deleting destroys the history of why a decision was made or a fact changed — Hipocampo prefers `status: archived` or `status: superseded` (see invariant 3, `SPEC.md` section 8). The only formal exception is a legitimate request to erase personal data (LGPD Art. 16 / GDPR Art. 17), always with an explicit human decision and replacement by a minimal "tombstone" — see `decisions/0010-legal-deletion-exception.md`.

### What happens to my data if the AI product I use goes offline?

Nothing — your data keeps existing, readable, in plain markdown inside a git repository, regardless of whether any AI product is online or not. This has been a formal principle of the methodology since v1.5.0 (see `decisions/0013-data-always-human-readable.md`). A specific outage of a product (even a real, documented one) is never a reason to lose access to your own knowledge.

### Do I need the skill to use the methodology, or can I just use manual prompts?

The skill isn't strictly required — the `SPEC.md` and `CLAUDE.md` of your instance are already enough for any AI agent capable of reading files and using the GitHub MCP to operate correctly, even without the skill installed. The skill exists to automate recurring rituals (checking for a new release, the REM ritual, the staleness ritual, cross-repository `related` resolution) without you needing to remember to request each one manually.

### What's the difference between the methodology's license and my content's license?

They're two different entities. The methodology (`hipocampo`, `hipocampo-toolkit`) is yours, open, always Apache-2.0. Your content, once instantiated, is yours (or your company's) and should never carry the methodology's open license — always proprietary/confidential (`LicenseRef-<idstring>`, see `decisions/0007`). Instantiating the template doesn't change who owns the knowledge you place inside it.

### How do I know if a new version of the methodology has been released?

If the skill is installed and personalized, it checks `hipocampo` for new releases and notifies you. Manually, the `hipocampo` `CHANGELOG.md` is the source of truth — every new entry is a release.

### Can I use this on a git host other than GitHub?

`hipocampo-toolkit` is designed as a generic template (git + markdown), so technically there's no dependency on GitHub specifically. In practice, today, all the automation (skill, MCP, release routine) was built and tested on top of the GitHub MCP — using another host works for the content itself, but would require adapting the automation part.

### I forgot to mark my repository as private when creating it, now what?

Fix it immediately — go to the repository settings on GitHub and change the visibility to Private. It's invariant 1 of the methodology (`SPEC.md`, section 8) and has no exception. After fixing it, it's worth reviewing the commit history: if any sensitive content was ever public, even briefly, consider whether something needs to be rotated (for example, if a secret was exposed).
