# 0015 — AGENTS.md as the canonical instruction file, CLAUDE.md as a thin pointer

**Status:** Accepted

## Context

Hipocampo has advocated multi-tool operation from the start (Claude, ChatGPT, Gemini, GitHub Copilot, Antigravity — see `docs/MULTI-TOOL-USAGE.md`), but every instance up to v1.9.0 uses `CLAUDE.md` as the primary operational instruction file — a tool-specific name, not the standard's. In the meantime, `AGENTS.md` established itself as a real, widely adopted open standard: formalized as a specification in August 2025 with participation from OpenAI, Google, Cursor, and Factory; donated to the Linux Foundation's Agentic AI Foundation in December 2025; more than 60 thousand repositories and 20+ AI tools support it. Keeping only `CLAUDE.md` as the source of instruction contradicts the very tool-neutrality principle that Hipocampo already advocates.

## Decision

`AGENTS.md` becomes the canonical operational instruction file of any Hipocampo instance — the same role `CLAUDE.md` held until v1.9.0 (invariants, local extensions, frontmatter reference, repository scope). `CLAUDE.md` continues to exist, but becomes a thin pointer: a few lines, directing the agent to `AGENTS.md` as the source of truth. This follows the same progressive-disclosure principle already used elsewhere in the methodology (e.g., skill vs. reference document) — the essential in a small, always-loaded file, the rest on demand, without duplicating content in two places that could diverge.

Every content repository (instantiated from `hipocampo-toolkit`) now has `AGENTS.md` as a mandatory file; `CLAUDE.md` remains mandatory too, but only as a pointer. Retroactive migration of already-existing instances is the responsibility of whoever operates each one — it is not automatic (the same principle as any MINOR change, see DISCLAIMER.md).

## Rationale

Duplicating operational instruction in both `CLAUDE.md` and `AGENTS.md` would recreate the same risk already identified in the Personal Second Brain precedent (the decision to separate skill from framework, before Hipocampo existed): two sources of the same truth silently diverge as soon as one is edited and the other is not. Electing one of them as canonical and the other as a pointer eliminates this risk by construction. `AGENTS.md` is the right choice as canonical because it is the standard that does not presuppose any specific tool — exactly what Hipocampo already asks of itself.

## Discarded alternatives

- **Keep only `CLAUDE.md`, without `AGENTS.md`:** discarded for contradicting the already-established multi-tool principle — instances operated by tools that natively recognize `AGENTS.md` (more than 20, including several outside the Claude ecosystem) would be left with no instruction at all if the agent did not know to open `CLAUDE.md` by its own convention.
- **Have both files with complete, independent content:** discarded due to the risk of silent divergence already described.
- **`CLAUDE.md` as canonical, `AGENTS.md` as pointer:** discarded — it would invert the tool-neutrality logic; the tool-specific file should be the thinner of the two, not the opposite.
