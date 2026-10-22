# hipocampo

Agentic second brain methodology: git + markdown + AI rituals. This repository is spec and tooling — it never stores real content from any instance.

Each governed knowledge repository is a **Vault**. V3 classifies its policy
profile as `entity`, `team` or `personal`; a repository named "concepts" is
still a vault. See [the taxonomy](docs/taxonomy.md) and
[the V3 vocabulary](docs/v3-vocabulary-and-aliases.md).

- [SPEC.md](SPEC.md) — normative specification: frontmatter schema, retrieval rules, versioning.
- [GETTING-STARTED.md](GETTING-STARTED.md) — practical adoption guide.
- [DISCLAIMER.md](DISCLAIMER.md) — what the methodology is and isn't, recommended and non-recommended scenarios.
- [BEST-PRACTICES.md](BEST-PRACTICES.md) — best practices for use: day-to-day, privacy/compliance posture, and adoption by teams/new companies.
- [docs/privacy-and-licensing-boundaries.md](docs/privacy-and-licensing-boundaries.md) — boundaries between methodology licensing, content-vault licensing, privacy, and progressive remediation.
- [MIGRATIONS.md](MIGRATIONS.md) — migration guide per MAJOR version jump.
- [docs/legacy-read-support.md](docs/legacy-read-support.md) — bounded V2 read adaptation and its limits; general V2/V3 compatibility is unchanged.
- [docs/host-installation.md](docs/host-installation.md) — host-specific skill/plugin update and verification gates.
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

Current version: **3.1.0** ([SemVer](https://semver.org/lang/pt-BR/)).

## Published V3 baseline and adoption boundary

V3.0.0 was published on 2026-10-08. Version 3.0.1 corrects the publication
markers and install guidance that remained stale in that released source; it
preserves the V3.0.0 contract and vault compatibility range. See the
[release record](docs/v3-release-preparation.md) and [changelog](CHANGELOG.md).
Publication does not mean that existing vaults have migrated, that restoration
or LTE is complete, or that every AI host exposes a verified V3 runtime.

The V3 contract includes MRL-0006's operational-trace rules for layered events,
session/cache boundaries, CRUD audit metadata, structured correlation,
host-capability disclosure and revocation reach. This release does not claim a
durable host log, remote invalidation, migration or V3 activation for existing
vaults.

F0 defines script-level classification, phase-specific verification, layered
evidence boundaries, hardcode review and typed outcomes for incomplete proof.
Semantic evaluation remains distinct from deterministic validation.

## Installation and publication channels

Version 3.1.0 adds a callable local runtime and an explicit experimental channel,
with independent skill 2.2.0, preserving the 3.0.0 data contract. Follow
[runtime installation](docs/v3-runtime-usage.md) and
[distribution/channel rules](docs/v3-distribution-and-channels.md).
Stable installation verifies the official immutable published release and hashes.
Experimental installation fixes a source commit or RC tag, needs no GitHub Release,
and emits WARNING while valid canonical operations continue. Operation-specific
authorization and integrity checks remain mandatory. A version heading is an
identity declaration; query the provider to establish actual publication.
