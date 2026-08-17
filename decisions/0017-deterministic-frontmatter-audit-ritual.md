# 0017 — Frontmatter audit: deterministic ritual that precedes REM consolidation

**Status:** Accepted

## Context

The staleness check (SPEC.md section 5) and the REM ritual (section 5-A) depend on knowing which documents have an expired `ttl`, a missing required field, or another violation of the frontmatter norm (section 2) — but up to v1.9.0 there is no formal mechanism that produces this list. Running this check via an AI agent, document by document, wastes tokens and is subject to the same probabilistic error risk that DISCLAIMER.md already acknowledges for any AI routine — when the check is purely mechanical (date comparison, field presence), it needs no model judgment at all.

## Decision

Frontmatter audit is a new, deterministic ritual (implemented as a script, not as AI agent judgment), with a recommended daily cadence, running **before** that same day's REM consolidation. It scans a repository's entire frontmatter (without reading document bodies — section 2-B already establishes frontmatter-first) and produces a queue file, `meta/fila-de-manutencao.md`, listing: documents with an expired `ttl` (by `temporality`), documents with a missing required field (section 2), and any other mechanically detectable violation of the frontmatter norm.

The frontmatter audit never decides disposition (archive, supersede, revalidate) — it only reports. The disposition decision is always up to the REM ritual (section 5-A, the "update old memories" function) or a human, never the audit itself.

## Rationale

Separating detection (deterministic, unambiguous, no judgment cost) from decision (which needs judgment, and is therefore always human-supervised, invariant 5) follows the same spirit as DISCLAIMER.md: use AI where judgment is needed, not where a mechanical check already solves it. Running it before REM, not after, ensures that the day's consolidation already operates with an up-to-date queue, instead of working with potentially outdated information about what needs attention.

## Discarded alternatives

- **Leave the staleness check entirely to the AI agent, without a script:** discarded due to token cost (reading every document's frontmatter via agent, every time) and the risk of error in a task that is purely mechanical.
- **Run the frontmatter audit after REM, not before:** discarded because REM needs the up-to-date queue to fulfill its second function (updating old memories) within the same daily cycle — running it after would delay handling any new pending item by a full day.
- **A single global, cross-repository queue file:** discarded because maintenance rituals always operate within the scope of one repository at a time (see DR0016) — one file per repository avoids ambiguity about where a pending item lives.
