# Contributing to Hipocampo

This file is for anyone — human or agent — about to touch the `hipocampo` repository itself (the methodology: `SPEC.md`, Decision Records, `docs/`, `skill/`, `scaffold/`). It is not for content instances (vaults) built from this methodology — those follow their own `AGENTS.md`.

## Start here

- **[AGENTS.md](AGENTS.md)** — the agent entry point for this repository. Read it first; it states the working rules an agent operating on `hipocampo` itself must follow, distinct from the `AGENTS.md` a content instance carries for its own operators (`SPEC.md`, section 11).
- **[SPEC.md](SPEC.md)** — the normative specification. Any change to what an instance must do to be compatible starts here.
- **[README.md](README.md)** — orientation for a human reading this repository for the first time.

## Language

**This repository is maintained in English.** `SPEC.md`, `decisions/`, `docs/`, `skill/`, and `scaffold/` are all written in English, and new contributions follow the same rule — see `decisions/0034-repository-and-vault-language-policy.md` for why. This is a policy about what gets committed *here*, not about what language you converse with an agent in while working on it: that stays whatever's natural for the conversation. It also doesn't apply to vaults (content instances) built from this methodology — a vault's own content language is a separate, per-instance declaration (`hipocampo.yaml`'s `instance.language`, same Decision Record).

## Decision Records

Any change to a normative rule, a schema field, an invariant, or an established convention needs a Decision Record (a DR) before or alongside the change — not written after the fact to justify something already done. The template (Context / Decision / Rationale / Discarded alternatives, plus a `**Status:** Accepted` line) and the criteria for when a DR is warranted versus when a change is small enough not to need one are in `SPEC.md`, section 7 ("Decision Record vs. `type: decision`") — read that section before opening one. Number a new DR sequentially from the highest existing file under `decisions/`; check `decisions/` directly rather than trusting a number cited in an older issue or conversation, since it drifts as work lands.

## Change Sets

Every `operational` or `normative` change (per `docs/change-management.md`'s own class definitions — `editorial` changes are exempt) needs a Change Set: a `changes/<change-id>/` folder with `proposal.md` (summary, class, semver, triggers fired, known gaps) and `impact.yaml` (a file-by-file accounting of what changed and why, plus the validation commands run). See `docs/change-management.md` for the full mechanism, the trigger table, and what each class actually requires.

## Validation

Before opening a PR, run the repository's own structural validator from its root:

```
python3 scripts/validate_hipocampo.py --root .
```

It checks Decision Record template compliance, internal markdown link resolution, and `README.md`/`CHANGELOG.md` version consistency — deterministically, no AI judgment involved (`decisions/0036-deterministic-validation-of-repository-structure.md`). It also runs automatically in CI on every PR against `main` (`.github/workflows/validate.yml`). A clean run is necessary, not sufficient — it catches structural defects, not whether the change is a good idea or complete; that remains human review. Run every declared validator, including `validate_skill_docs.py`, `validate_contracts.py`, `validate_skill_package.py`, and `validate_change.py` when they apply; verify the actual remote branch after publication rather than treating a local result as proof.

## Terms and names

Before introducing a new canonical term, alias, enum value, schema field, routine, mechanic, action, or other named concept, search for an existing term and classify the proposal. In the same Change Set, record every accepted canonical term in `docs/taxonomy.md`, every controlled value or alias in `docs/vocabulary-dictionary.md`, and the authoritative Decision Record or SPEC section that owns it. If no registry change is applicable, say why in the Change Set's terminology-review note; do not silently invent competing vocabulary.

## Privacy and learned safeguards

Never put a real entity, person, or personal handle into this public methodology repository; use the placeholders required by `decisions/0050`. Never paste a credential, secret, non-public financial value, or sensitive finding into a proposal, audit, example, CI output, or issue. For a public financial value, cite its public URL and date. Do not claim a GitHub write, CI result, release, or package installation happened until it has been independently checked. A package provenance field cannot self-reference its own commit: use the release tag and package lock for update integrity instead.

## Pull requests and releases

One PR per unit of work, reviewed and merged by Mau — this repository does not use `mcp__GitHub__merge_pull_request`-style automated merging; a human always merges. If you're cutting an actual release (not just landing a change), **[RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md)** is the concrete, operationalized run-through of `decisions/0014`/`0021`/`0023` — apply every item before tagging.

## What never changes without an explicit decision

The six invariants (`SPEC.md`, section 8) are never overridden by any instance, under any request, from any tool. If a contribution appears to require bending one of them, that's a signal to open a Decision Record and discuss it explicitly — never to route around it silently.
