# Hipocampo — Disclaimer

This document exists separately from the [LICENSE](LICENSE) because it solves a different problem: the LICENSE says what you can legally do with the code/spec; this document says what the methodology **is and is not**, in practice, before you rely on it for something that matters.

## Purpose

Hipocampo is a methodology for organizing personal or corporate knowledge using git, markdown, and rituals conducted by AI agents. The goal is better retrieval and living (not static) knowledge over time — it is not, and never had the ambition of being, a substitute for systems with stronger formal guarantees.

## What Hipocampo is not

- **It is not a transactional database.** There is no guarantee of atomicity, consistency under concurrency, or automatic rollback beyond what git itself offers (which is versioning, not transactions).
- **`visibility` is not technical enforcement.** The `visibility` field in the frontmatter (SPEC.md, section 2) is a reading convention for humans and agents — it does not technically prevent someone with access to the repository from reading a file marked `confidential`. Real technical enforcement, when needed, is done through GitHub repository permissions (see invariant 4 of SPEC.md), not by a label inside a shared repository.
- **It does not replace legal compliance.** Nothing in this repository constitutes legal advice. If your instance stores sensitive personal data, trade secrets, or information subject to specific regulation (LGPD, contractual, sectoral), legal adequacy is the responsibility of whoever operates the instance — not something Hipocampo solves by design.
- **AI routines are probabilistic.** Any ritual conducted by an agent (consolidation, staleness, classification of `type`/`temporality`) can be wrong. Hipocampo assumes human supervision in the loop — the invariant "the agent never writes without an explicit request" (SPEC.md, section 8) exists exactly for this reason, it is not boilerplate.

## Data always human-readable, regardless of AI product

All data in a Hipocampo instance must remain readable and navigable by a human using only the repository's native tools — GitHub's own markdown viewer, any text editor, `git log`/`git show` — without depending on any specific AI product being online. This is not a limitation of the methodology — it is the same characteristic that already guarantees, above, that access permission is always resolved at the GitHub level, never by a third-party product layered on top of it.

Vendor lock-in is a real and growing risk as more functionality is built on top of specific AI products (skills, MCPs, agents). An outage, a product discontinuation, or a pricing change should never put access to the knowledge itself at risk — only the convenience of operating it with AI. See `decisions/0013-data-always-human-readable.md`.

## Recommended scenarios

- Personal or small-team knowledge, where the person/team can review what the agent proposes.
- Content where "probably correct, reviewable later" is an acceptable trade-off in exchange for better retrieval.
- Organizations that already trust GitHub as a permissioning platform (Hipocampo's privacy model structurally depends on this — see `docs/FUNDAMENTALS.md`).

## Scenarios not recommended

- Records that need a formal audit trail with legal guarantees (that is the role of a dedicated compliance system, not a second brain).
- Data that cannot, under any circumstances, be processed by a third-party AI model — even with training opt-out, the content still passes through the provider's inference at the moment of use.
- Replacement of a system with a formal SLA for availability/integrity (git + markdown does not have that kind of guarantee).

## Technical assumptions

Hipocampo assumes: a git host with real per-repository permissioning (the model was designed around GitHub, but the principle generalizes to any equivalent host); an AI agent capable of reading/writing markdown and following structured instruction; willingness on the part of the instance operator to review what the agent proposes, not just accept it automatically.

## Versioning and what it means for you

The methodology follows SemVer (full detail in SPEC.md, section 9, and in `MIGRATIONS.md`). In practice, for those who just use it:

- **PATCH** (1.0.x) — nothing changes for you. Text clarification or spec error correction.
- **MINOR** (1.x.0) — new optional capability. Your instance remains valid without adopting anything; ignoring it is a legitimate option.
- **MAJOR** (x.0.0) — something changed in an incompatible way. Your instance keeps working with the version it declares it follows, but migrating to the new version requires following the corresponding guide in `MIGRATIONS.md`. Migration is never automatic or silent.

## Bridge to LICENSE

This disclaimer does not alter or replace anything in the [LICENSE](LICENSE) (Apache-2.0) or the [NOTICE](NOTICE). In case of a conflict of interpretation between this document and the LICENSE, the LICENSE prevails as the legally binding document — this file is practical guidance, not a legal instrument.