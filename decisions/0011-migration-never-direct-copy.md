# 0011 — Migration of pre-existing content never copies a file directly

**Status:** Accepted

## Context

Throughout Batch 4 (real migration of hundreds of documents from the legacy Personal Second Brain to the Hipocampo repositories), the practice consistently followed was to never copy an original file verbatim into a Hipocampo instance — always rewrite the frontmatter from scratch according to the current schema, and frequently also adjust the document body (atomicity rule, removal of data banned by the privacy policy, naming updates). This practice was never formalized as a normative rule — it remained only an ad hoc convention. This means a future migration, done by another person, another company adopting Hipocampo, or an AI agent without this session's history, could legitimately copy files directly, believing it was migrating correctly.

## Decision

Migration of pre-existing content — from a legacy system, from an earlier version of the same instance, or from any external source — never copies the original file directly into the destination repository. The agent (or human) always:

1. Interprets the original content.
2. Rewrites the frontmatter from scratch, according to the current version of the schema (SPEC.md, section 2).
3. Applies the current atomicity, naming, and privacy-policy rules to the document body (SPEC.md, section 2-A), splitting, purging, or reformatting as needed.
4. Documents the migration in `revision_note`, citing the source and the changes applied — what was preserved verbatim and what was changed, and why.

This applies both to migrating content from outside Hipocampo and to republishing content from an earlier version of the methodology within the same instance.

## Rationale

Copying a file directly propagates schema inconsistency (outdated frontmatter, fields that no longer exist, old conventions) and also propagates a violation of the current privacy policy that perhaps didn't exist when the original document was written — for example, personal data that was acceptable to record before `decisions/0009` existed. Rewriting forces a conformance check at every migration, instead of assuming the old content is already correct. The additional cost (more work per migrated document) is acceptable because migration is a rare event per document — it happens once —, while the cost of propagating inconsistency is paid repeatedly, on every future read of the poorly migrated document.

## Discarded alternatives

- **Copy the file directly and fix it later, on demand.** Discarded: without a mandatory check at migration time, "on-demand" correction tends to never happen — nobody revisits a document that's already migrated and apparently working.
- **Automated migration with no human or agent review.** Discarded: same principle as invariant 5 (SPEC.md, section 8) and the process already used in Batch 4 — classification decisions (`type`, `category`, what to preserve vs. discard) require judgment, they can't be mechanized blindly.
- **Migrate only the frontmatter, always preserving the body verbatim.** Discarded: the body can also violate current rules (atomicity, privacy) that didn't exist at the source; restricting the rewrite to the frontmatter only would let those violations slip through.
