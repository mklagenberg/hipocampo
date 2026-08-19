# hipocampo

Agentic second brain methodology: git + markdown + AI rituals. This repository is spec and tooling — it never stores real content from any instance.

- [SPEC.md](SPEC.md) — normative specification: frontmatter schema, retrieval rules, versioning.
- [GETTING-STARTED.md](GETTING-STARTED.md) — practical adoption guide.
- [DISCLAIMER.md](DISCLAIMER.md) — what the methodology is and isn't, recommended and non-recommended scenarios.
- [BEST-PRACTICES.md](BEST-PRACTICES.md) — best practices for use: day-to-day, privacy/compliance posture, and adoption by teams/new companies.
- [MIGRATIONS.md](MIGRATIONS.md) — migration guide per MAJOR version jump.
- [CHANGELOG.md](CHANGELOG.md) — methodology version history.
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to contribute to this repository: language policy, Decision Records, Change Sets, validation, releases.
- [ROADMAP.md](ROADMAP.md) — current direction, no date commitment.
- [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md) — minimal checklist run when cutting a new version of the methodology itself.
- [decisions/](decisions/) — Decision Records: why each structural rule is the way it is.
- [skill/SKILL.md](skill/SKILL.md) — the methodology's operational skill (generic canonical source; each person installs and personalizes their own copy).
- [scaffold/README.md](scaffold/) — declarative mechanism for instantiating new content repositories (profiles, file skeleton, LICENSE templates).
- [docs/FUNDAMENTALS.md](docs/FUNDAMENTALS.md) — introduction to git/GitHub for those who've never used it, with a parallel to Obsidian and a privacy checklist.
- [docs/AI-MODELS.md](docs/AI-MODELS.md) — what matters in an AI model/product to operate Hipocampo well.
- [docs/PERFORMANCE-AND-GRAPH.md](docs/PERFORMANCE-AND-GRAPH.md) — how retrieval/the graph works, and the relationship with Google's OKF.
- [docs/MULTI-TOOL-USAGE.md](docs/MULTI-TOOL-USAGE.md) — common principle and specifics of use in Claude, ChatGPT, Gemini, Copilot, Antigravity.
- [docs/FAQ-AND-COMMON-ERRORS.md](docs/FAQ-AND-COMMON-ERRORS.md) — instantiation errors actually encountered and frequently asked questions.

To instantiate a content repository from this methodology, ask the agent operating your copy of the Hipocampo skill to run the scaffold declared in [scaffold/](scaffold/) — there's no longer a separate "Use this template" button (the old `hipocampo-toolkit` was consolidated here, `decisions/0032`). Full operational procedure: [skill/references/instantiation.md](skill/references/instantiation.md).

Agents should start at [AGENTS.md](AGENTS.md).

## MODA Conformance

<!-- moda:disclosure:start -->
This repository is being evaluated and brought into conformance with [MODA](https://github.com/mklagenberg/moda) — an open framework for organizing, designing, auditing, packaging, and evolving agentic methodologies.

- Artifact profile: `methodology`
- MODA compatibility: `^1.0.0`
- Adoption relationship: `conforms_to` (retrospective) — all `major` findings from the 2026-08-17 self-audit closed as of v2.0.0; `minor` findings and `observation`s remain open, see `conformance/moda.yaml`
- Manifest: [`moda.yaml`](moda.yaml)
- Conformance profile: [`conformance/moda.yaml`](conformance/moda.yaml)
- Latest audit: [`audits/moda/2026-08-17-v1.0.0-self-audit.md`](audits/moda/2026-08-17-v1.0.0-self-audit.md)
<!-- moda:disclosure:end -->

Current version: **2.0.0** ([SemVer](https://semver.org/lang/pt-BR/)).
