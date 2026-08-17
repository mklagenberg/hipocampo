# 0002 — Multi-repository architecture, no replication

**Status:** Accepted

## Context

The original design considered a replicated "Global Context" model across repositories — each instance would have a synchronized copy of certain shared information.

## Decision

Adopt an independent-repository architecture, with no content replication between them. Two layers: methodology and tooling (`hipocampo`, `hipocampo-toolkit`, public) and knowledge base (content repositories instantiated from the template, always private). References between content repositories are resolved by link/alias (`related` with a `$alias:` prefix, see SPEC.md section 6), never by copying data.

## Rationale

Replication without an automatic synchronization mechanism creates silent divergence — the copy in one repository becomes outdated relative to the source without anyone noticing, because there's no automatic consistency check between the two. A document that physically exists in only one place (with other repositories pointing to it by reference) doesn't have this failure mode: either the link resolves to the right document, or the link is broken — there's no intermediate state of "outdated but present copy."

## Discarded alternatives

- **Replicated Global Context** — discarded due to the risk of divergence without a sync mechanism, described above.
- **A single repository for everything** — discarded because it contradicts the requirement that knowledge repositories always be private while `hipocampo`/`hipocampo-toolkit` are always public — actual GitHub permissioning is per-repository, not per-folder within a shared repository (same principle as the `visibility` invariant, SPEC.md section 2).
