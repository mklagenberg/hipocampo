# Roadmap

Last revised: **2026-08-17**

This roadmap communicates direction, not a date commitment. Only an approved release plan or formal milestone creates a delivery commitment. Detailed work lives in Decision Records and PRs; completed work lives in `CHANGELOG.md`.

## Now

### Bringing the methodology into MODA conformance — toward v2.0.0

**Outcome:** Hipocampo declares and sustains, with real evidence, a formal conformance relationship with [MODA](https://github.com/mklagenberg/moda) — today `audited_against`/`mapped`/`partial` (see `moda.yaml`, `conformance/moda.yaml`), evolving toward `conforms_to` as the `major` findings from the 2026-08-17 audit (`audits/moda/`) are addressed.

**Status:** in progress — repository type taxonomy (`decisions/0029`/`0030`), declarative foundation (`moda.yaml`, `AGENTS.md`, this `ROADMAP.md`), Change Set mechanism (`docs/change-management.md`, `decisions/0031`), and consolidation of `hipocampo-toolkit` into scaffolding + the `hipocampo.yaml` manifest per vault (`scaffold/`, `decisions/0032`/`0033`) have already been merged; English translation of the whole repository plus the repository/vault language policy (`decisions/0034`) are done and awaiting Mau's manual merge in PR #27 — not yet in `main`; deterministic validation and the design dimensions still missing (failure/recovery, quality/evaluation) remain pending.

**Manual pending items (outside the scope of any PR):** archiving the `hipocampo-toolkit` repository on GitHub, and committing a redirect notice to its `README.md` — no tool available in this process automates the action of archiving a repository; this is Mau's action.

The remaining work includes:

- minimal deterministic validation (script + CI) of the structural integrity of the methodology repository itself;
- merge PR #27 (complete translation of the `hipocampo` repository into English, with a redirect stub at every renamed path, plus the repository/vault language policy, `decisions/0034`);
- new section on behavior under failure (insufficient evidence, contradiction, unavailable tool, interruption, unsafe request, incompatible migration);
- minimal representative evaluation scenarios;
- documented use cases;
- `CONTRIBUTING.md` (at the end, per Mau's decision);
- `MIGRATIONS.md` getting its first real entry ("1.x → 2.0") and cutting the `v2.0.0` tag.

The release is blocked until the methodology's own release gate (`SPEC.md`, section 9, and `decisions/0014`/`0021`/`0023`) passes and is explicitly approved by Mau.

## Next

### Continuous deterministic validation

**Outcome:** every PR against `main` automatically runs a check of the Decision Record template, internal links, and consistency between the declared version and `CHANGELOG.md`, without depending on manual review to catch this kind of error.

**Status:** specified as part of v2.0.0 (see "Now"); actual implementation hasn't started yet.

## Later

### Periodic audit of real instances

**Outcome:** Mau's 4 content repositories (and any future third-party instance) have a declared cadence for checking conformance to `hipocampo.yaml`/`UPGRADE.md`, not only on explicit request.

**Status:** hypothesis.

## Not planned

- Hosting or running a content instance — Hipocampo specifies, it doesn't run infrastructure.
- Multi-agent orchestration — Hipocampo is designed for one agent at a time, client-side (`decisions/0025`).
- Silently updating an installed skill or content already generated in an instance.
- External MODA conformance certification — MODA 1.0 doesn't offer this, and Hipocampo doesn't intend to invent its own.