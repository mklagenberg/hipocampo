# Roadmap

Last revised: **2026-10-15**

This roadmap communicates direction, not a date commitment. Only an approved release plan or formal milestone creates a delivery commitment. Detailed work lives in Decision Records and PRs; completed work lives in `CHANGELOG.md`.

## Current direction — published v3.0.0 / LTE and adoption

The active released contract is `v3.0.0`, published on 2026-10-08. The
v3.0.1 PATCH follow-up corrects publication markers and skill install guidance;
it preserves the V3.0.0 contract and `^3.0.0` vault compatibility range. The
MRL-0003 through MRL-0006 waves are internal execution lineages, not separate
releases.

The current direction is governed by Multi Entity, Multi Vault and Privacy
First. Knowledge circulation is selective Package delivery, not promotion or
automatic authority transfer. Owner, Authority, Curator, User and Source stay
distinct. Conflicts may coexist as explicit Chunks, while current-use delivery
remains fail-closed when authority, conciliation, privacy or staleness is not
resolved. General derived projections remain deferred by the accepted V3
decision on derived layers. MRL-0005 now adds a single canonical vocabulary,
local vault extensions, English structural language, explicit offline
authority, and labelled external references. Change Set 0108 adds the logical
Search & Progressive Disclosure boundary: relevance does not grant authority
or disclosure, and the default presentation remains didactic prose.

**Status:** V3.0.0 publication is complete. X3 and X4 are complete in the
checkout. D5.1–D5.6 are accepted; MRL-0005/X5, MRL-0006/X6 and F0 are included
in the published methodology with bounded implementation/runtime evidence.
Publication did not migrate v2 instances or establish universal host runtime,
remote transport, restoration or LTE completion.

**Next direction:** continue per-vault v2 → v3 migration preparation, then pass
the integrated LTE readiness gate. Semantic Search and current local changes
must complete their human review and normal integration path. No additional
real-vault migration or V3 activation is inferred from methodology publication.

MRL-0006 decisions D6.1–D6.5 and F0 decisions D0.1–D0.4 are accepted in
management. X6 and F0 contracts were included in the published V3 baseline;
remaining migration, LTE and host-runtime gates are independent of publication.

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

## V3 release closure

Prepare the V3.0.0 contract and stable 2.0.0 portable skill, complete exact-package AI/human review and manual publication before resuming separately accepted vault migration. Local preparation is not release or universal runtime proof.
