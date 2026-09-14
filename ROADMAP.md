# Roadmap

Last revised: **2026-09-08**

This roadmap communicates direction, not a date commitment. Only an approved release plan or formal milestone creates a delivery commitment. Detailed work lives in Decision Records and PRs; completed work lives in `CHANGELOG.md`.

## Current direction — v3.0.0 / LTE

The active released contract remains `v2.2.0`. The next normative boundary is
one major `v3.0.0`/LTE release; the MRL-0003 through MRL-0006 waves are internal
execution lineages, not independent releases.

The current direction is governed by Multi Entity, Multi Vault and Privacy
First. Knowledge circulation is selective Package delivery, not promotion or
automatic authority transfer. Owner, Authority, Curator, User and Source stay
distinct. Conflicts may coexist as explicit Chunks, while current-use delivery
remains fail-closed when authority, conciliation, privacy or staleness is not
resolved. General derived projections remain deferred by the accepted V3
decision on derived layers. MRL-0005 now adds a single canonical vocabulary,
local vault extensions, English structural language, explicit offline
authority, and labelled external references.

**Status:** X3 and X4 are complete in the checkout. D5.1–D5.6 are accepted,
MRL-0005/X5, MRL-0006/X6 and F0 are implemented as unreleased V3 candidates.
No v2 instance migration, remote transport, tag, release or V3 activation has
occurred.

**Next direction:** validate the F0 closure, then prepare migration v2 → v3,
the LTE gate and the human publication gate. These remain subsequent
management stages.

MRL-0006 decisions D6.1–D6.5 and F0 decisions D0.1–D0.4 are accepted in
management. X6 and F0 candidate contracts are implemented and validated in the
checkout; the candidate remains unpublished and subject to the migration, LTE
and human publication gates.

## Historical foundation — v2.0.0, v2.1.1 and v2.2.0

### Bringing the methodology into MODA conformance — toward v2.0.0

**Outcome:** Hipocampo declares and sustains, with real evidence, a formal conformance relationship with [MODA](https://github.com/mklagenberg/moda) — today `audited_against`/`mapped`/`partial` (see `moda.yaml`, `conformance/moda.yaml`), evolving toward `conforms_to` as the `major` findings from the 2026-08-17 audit (`audits/moda/`) are addressed.

**Status:** in progress — repository type taxonomy (`decisions/0029`/`0030`), declarative foundation (`moda.yaml`, `AGENTS.md`, this `ROADMAP.md`), Change Set mechanism (`docs/change-management.md`, `decisions/0031`), consolidation of `hipocampo-toolkit` into scaffolding + the `hipocampo.yaml` manifest per vault (`scaffold/`, `decisions/0032`/`0033`), English translation of the whole repository plus the repository/vault language policy (`decisions/0034`, PR #27), the controlled-vocabulary dictionary (`decisions/0035`, PR #28/#29), deterministic validation + a minimal release-gate checklist (`decisions/0036`/`0037`, Fase G — closes MODA self-audit major finding 4 and minor finding 2), and failure/recovery behavior + minimal evaluation scenarios (`decisions/0038`/`0039`, Fase H — closes MODA self-audit major findings 6 and 7) have already been merged into `main`. With Fase H merged, all seven `major` findings from the 2026-08-17 self-audit are closed — whether `moda.yaml`'s `adoption.relationship` is ready to move from `audited_against` to `conforms_to` is a decision for Mau, not a mechanical follow-up edit; see the tracking issue below.

**Manual pending items (outside the scope of any PR):** archiving the `hipocampo-toolkit` repository on GitHub, and committing a redirect notice to its `README.md` — no tool available in this process automates the action of archiving a repository; also, declaring a GitHub branch-protection rule that requires `.github/workflows/validate.yml` to pass before merging into `main` — no tool available in this process configures repository settings. Both are Mau's action.

The remaining work to close v2.0.0 — tracked concretely in [issue #31](https://github.com/mklagenberg/hipocampo/issues/31), not duplicated here — includes `CONTRIBUTING.md`, `MIGRATIONS.md`'s first real entry ("1.x → 2.0"), the version bump, re-evaluating the `conforms_to` relationship, merging any remaining open PRs, and cutting the `v2.0.0` tag.

The release is blocked until the methodology's own release gate (`RELEASE-CHECKLIST.md`, expanding `SPEC.md` section 9 and `decisions/0014`/`0021`/`0023`) passes and is explicitly approved by Mau.

## Later

### Periodic audit of real instances

**Outcome:** Mau's 4 content repositories (and any future third-party instance) have a declared cadence for checking conformance to `hipocampo.yaml`/`UPGRADE.md`, not only on explicit request.

**Status:** hypothesis.

## Not planned

- Hosting or running a content instance — Hipocampo specifies, it doesn't run infrastructure.
- Multi-agent orchestration — Hipocampo is designed for one agent at a time, client-side (`decisions/0025`).
- Silently updating an installed skill or content already generated in an instance.
- External MODA conformance certification — MODA 1.0 doesn't offer this, and Hipocampo doesn't intend to invent its own.
