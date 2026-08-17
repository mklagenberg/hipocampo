# 0032 — Consolidation of hipocampo-toolkit into declarative scaffolding

**Status:** Accepted

## Context

The `hipocampo-toolkit` repository existed as a separate GitHub template ("Use this template"), carrying the skeleton of files a new content repository needs (`AGENTS.md`, `CLAUDE.md`, `POS-INSTANCIACAO.md`, `LICENSE`, `registry.md`, `example/`, and a copy of the skill inside `skill/`) in addition to the `LICENSE` templates. This topology — normative methodology (`hipocampo`) and distribution/scaffold mechanism (`hipocampo-toolkit`) in separate repositories — had never been evaluated against MODA.

MODA normatizes scaffold and distribution in `docs/composition-scaffolding-and-distribution.md`, requiring any scaffold mechanism to declare, per profile: engine version, inputs, outputs with an ownership class (`canonical-reference`/`generated-once`/`managed-structure`/`user-authored`), conflict behavior, and upgrade behavior. This is exactly what `hipocampo-toolkit` lacked — it worked, but through a fully implicit mechanism (GitHub's native button), with none of these declarations.

Additionally, `hipocampo-toolkit` itself contained a known structural problem: the `skill/` folder copied by "Use this template" into every new content repository never had any effect (the skill runs client-side, per person — `decisions/0025`) — and the toolkit's own `POS-INSTANCIACAO.md` already instructed the user to delete it manually. It was structural noise that the process itself recognized as an error, but never fixed at the source.

## Decision

Consolidate the content of `hipocampo-toolkit` into the `hipocampo` repository itself, under `scaffold/`, as a declarative scaffold per MODA:

- **Two profiles per domain** (`scaffold/profiles/pessoal.yaml`, `scaffold/profiles/empresa.yaml`), not per tier — the generated skeleton doesn't differ by tier (`conteudo`/`vault`), only the `LICENSE` receives a documented adjustment (sections kept). `tier` is an input declared in the profile, not a separate profile.
- **`scaffold/skeleton/`** holds the source content for each declared output, migrated from the toolkit with two adjustments: (a) the `skill/` folder is no longer generated — that residue no longer exists; (b) `POS-INSTANCIACAO.md` is reworked from a manual step-by-step into a post-generation verification checklist (see rationale).
- **The skill (`skill/`, previously only in the toolkit) migrates into `hipocampo` itself**, as a methodology component — it stops having `independent` lifecycle in `moda.yaml` (it was a component hosted in a separate GitHub repository) and becomes `embedded`.
- **Without the "Use this template" button** (a consequence of archiving the toolkit), instantiating a new vault is now **executed by the agent**: the skill reads the profile, collects the user's inputs, presents the complete plan before writing (invariant 5), creates the new repository, and generates each declared output — with no native GitHub templating mechanism involved. Full procedure: `skill/references/instanciacao.md`.
- **`hipocampo-toolkit` is archived** on GitHub (a real repository, a manual action — no tool available in this environment automates this step) and receives, before archiving, a redirect `README.md` pointing to `hipocampo/scaffold/`.
- All existing reference points that cited `hipocampo-toolkit` (`README.md`, `GETTING-STARTED.md`, `UPGRADE.md`, `AGENTS.md`, `moda.yaml`) are updated to point to the new `scaffold/`.

## Rationale

Consolidating solves two problems at once: (1) it aligns the scaffold mechanism with MODA's declarative contract, making explicit what today was implicit in the click of a button; (2) it removes the structural noise of the residual `skill/` folder, which never worked and whose own manual checklist already recognized as an error.

Losing the "Use this template" button is a real operational consequence, not a cosmetic one — but the alternative of keeping a separate, minimal template repository just to preserve the click would reintroduce the same underlying problem (an implicit mechanism, without declaration of inputs/outputs/conflicts) this DR seeks to eliminate. Choosing to have the agent execute the scaffold, instead of keeping a native click or requiring a full manual checklist, was an explicit decision by Mau (not the agent) given this trade-off.

`POS-INSTANCIACAO.md` stops being a step-by-step because the agent already executes the steps that used to be manual (mark private, swap the LICENSE, fill in AGENTS.md) as part of the generation itself — the file remains as a human verification checklist of what the agent generated, not as execution instructions.

## Discarded alternatives

- **Keep `hipocampo-toolkit` as is, only documenting it in `moda.yaml`.** Discarded: it doesn't solve the underlying problem (implicit scaffold mechanism, residual `skill/` folder) — it only formally declares a gap that MODA asks to be closed.
- **Create a new, minimal template repository, without the `skill/` folder, keeping two repositories.** Discarded this round: it would preserve GitHub's native click, but would still leave the scaffold without declaration of inputs/outputs/conflicts — the normative problem would persist, only the visible surface (the `skill/` folder) would be fixed.
- **A full manual checklist, with the agent executing nothing.** Discarded by Mau's explicit decision — the agent already has access to the GitHub MCP and already executes this kind of operation in other contexts (creating branches, pushing files, PRs); requiring a manual checklist throws away that capability unnecessarily.
