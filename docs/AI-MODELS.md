# AI models and Hipocampo

Central reference, not specific to any instance — see `hipocampo/decisions/0002` (replication produces silent divergence) for why this content lives here and new instances receive only the link, not a copy.

Hipocampo is designed to work with any AI agent capable of reading/writing markdown via git — it doesn't depend on any specific model or product (see `DISCLAIMER.md`, "Data always human-readable"). Even so, some characteristics of a model/product matter for operating the methodology well.

## What matters, in practice

**Following structured instruction without drifting.** The methodology depends on invariants that have no automatic technical enforcement (SPEC.md, section 8) — the model needs to actually follow the rule "never write without an explicit request," not just when convenient. This is more a matter of instruction (a well-written skill) than of a specific model, but models more capable of following long, contextual instruction sustain this with less friction.

**Context window and the reason for frontmatter-first.** No model has an infinite context window, and even those with large windows pay a cost (in latency and in tokens) to use the whole thing. The CRUD/frontmatter-first mechanic (SPEC.md, section 2-B) exists exactly for this: in an instance with many documents, reading only the frontmatter of each candidate before deciding to read the full body is what makes the methodology viable on any model, regardless of its context window size.

**AI routines are probabilistic, not deterministic.** No model — however capable — guarantees 0% error in a `type`/`temporality` classification, in staleness triage, or in a REM ritual consolidation decision. That's why every ritual in the methodology always presents the plan before executing (SPEC.md, section 8) — human oversight in the loop isn't a safety layer against a bad model, it's a safety layer against the probabilistic nature of any model, including the best ones available.

**GitHub MCP as the common denominator.** The way Hipocampo is operated — reading/writing the repository via tools — depends on the AI environment in use having access to a GitHub MCP (or equivalent mechanism). This is what makes the methodology usable from different tools (Claude Cowork, ChatGPT, Gemini, GitHub Copilot, Antigravity, among others) without rewriting anything about the methodology itself — the operating principle is the same across all of them; only the mechanics of each tool for connecting that MCP change, and, in some cases, how much of read/write/create that particular connection actually grants — a standard chat product's own built-in connector is often more limited than a coding-agent product's (`docs/MULTI-TOOL-USAGE.md`, "Homologation status"; `docs/getting-started-non-technical.md` for the concrete Claude/ChatGPT case). Practical detail per tool: see `BEST-PRACTICES.md` and the multi-tool guide for whichever instance you're following.

## What doesn't matter

There's no "officially supported" model for Hipocampo, nor a certified minimum capability. The methodology doesn't benchmark any model — it assumes, as a technical premise (`DISCLAIMER.md`), only that the agent in use is capable of operating structured markdown and following instruction. Which model/product to use is a decision for whoever operates the instance, not something the methodology prescribes. This is a claim about capability, not about validation: whether this repository's own onboarding walkthrough has actually been written and checked for a given tool ("homologation") is a separate, narrower, currently-tracked thing — see `docs/MULTI-TOOL-USAGE.md`.
