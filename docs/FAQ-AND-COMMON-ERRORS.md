# FAQ and common errors

This document brings together two things: questions that come up repeatedly, and instantiation/operation errors already encountered for real in actual repositories running the methodology (not hypothetical). If you have a question or ran into something strange, it's probably already here.

## Common instantiation errors

### "I clicked 'Use this template', but the skill doesn't seem to work"

Expected. **"Use this template" copies the repository's skeleton, not the skill installation.** `skill/SKILL.md` arrives in your new repository as a file — but for an AI agent to actually use it, it needs to be personalized (the repository router for your instance filled in) and actually installed (in Cowork, that's `save_skill`; other tools have their own mechanism, see `docs/MULTI-TOOL-USAGE.md`). This step is in `hipocampo-toolkit`'s `POST-INSTANTIATION.md` — if you skipped it, go back there.

### "My new repository has an Apache-2.0 license, is that right?"

No, it's a known bug in GitHub's template mechanism: it copies the `LICENSE` from `hipocampo-toolkit` (Apache-2.0, correct for the methodology/tooling) into your new repository — but your new repository holds **content**, not methodology, and content should never be Apache-2.0 (see `decisions/0007-content-repo-licensing.md`). Manually swap the `LICENSE` for the right template in `hipocampo-toolkit/license-templates/` (personal or corporate) as soon as you instantiate. This is also in `POST-INSTANTIATION.md`.

### "My `CLAUDE.md` still says an old version of the methodology"

This means the instance hasn't gone through the release routine (see `decisions/0014-mandatory-release-routine.md`) the last few times the methodology evolved — or nobody updated it manually after instantiating. There is no automatic synchronization between repositories (see `decisions/0002`, multi-repo architecture without replication) — it's the responsibility of whoever maintains each instance to follow the `hipocampo` `CHANGELOG.md` and update the local `CLAUDE.md`. The skill, when installed correctly, helps by warning you when there's a new release — but it doesn't apply the update on its own.

### "I can't create the repository from the template inside my GitHub organization"

Probably a permissions issue. Creating a repository from a template inside an organization (instead of your personal account) usually requires an organization admin to enable it, or for you to ask someone with permission to create it on your behalf. It's not a limitation of the methodology — it's a GitHub configuration matter. See the corresponding note in `docs/FUNDAMENTALS.md`.

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
