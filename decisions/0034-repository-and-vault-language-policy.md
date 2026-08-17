# Repository and vault language policy

**Status:** Accepted

## Context

Fase E (this same release cycle, toward v2.0.0, PR #27) translated the entire `hipocampo` methodology repository — `SPEC.md`, all Decision Records, `docs/`, `changes/`, `skill/` (including `references/`), and `scaffold/` (including `skeleton/`) — from Brazilian Portuguese to English. That was executed as a one-time migration, not yet codified as an ongoing rule: nothing in `SPEC.md` or `AGENTS.md` stated that future contributions to this repository must be written in English, and `moda.yaml`'s `artifact.language` field was left at `"pt-BR"`, now stale relative to the repository's actual content.

Separately, the vault manifest (`hipocampo.yaml`, `decisions/0033`) declares `instance.domain`/`instance.tier` but had no field for the language of the content a specific vault actually stores. `hipocampo` changing its own language doesn't imply anything about the language of content repositories (vaults) — Mau's own four real vaults are, and remain, in Portuguese. A newly scaffolded vault, however, now inherits an English-language toolchain (scaffold skeleton, skill copy, this very spec) by default, and that default was implicit rather than declared anywhere a human or agent could check it.

## Decision

1. **`hipocampo` (this repository) is maintained in English, going forward.** `SPEC.md`, `decisions/`, `docs/`, `skill/`, and `scaffold/` are written in English; new contributions follow the same rule (see `AGENTS.md`, "Working rules"). `moda.yaml`'s `artifact.language` is corrected from `"pt-BR"` to `"en"` to reflect this, and the stale Portuguese `SPEC.md#...` anchor fragments left over from before the section headers themselves were translated are corrected across `moda.yaml` and `conformance/moda.yaml`.
2. **Every vault manifest (`hipocampo.yaml`) declares its own content language**, via a new `instance.language` field (BCP-47 tag, e.g. `"en"`, `"pt-BR"`) — independent of `hipocampo`'s own language. The scaffold skeleton pre-fills this field with `"en"` (the scaffold's own default), not a blank placeholder like `domain`/`tier` — the instantiating agent still confirms the actual language with the operator before finalizing, since most of Mau's real vaults are Portuguese and the default should never be assumed silently. The two scaffold profiles (`scaffold/profiles/pessoal.yaml`, `scaffold/profiles/empresa.yaml`) gain a matching optional `language` input, and `skill/references/instantiation.md` is updated so the instantiation procedure explicitly asks about it rather than assuming.
3. This does not retroactively change any existing vault's content language or trigger a translation of any vault — it only formalizes a declaration going forward. The four existing real vaults will declare `instance.language: "pt-BR"` when they retroactively adopt `hipocampo.yaml` (already a pending `UPGRADE.md` item since `decisions/0033`; this decision adds one more field to that same pending adoption step).
4. This decision governs what is written *in a repository* (`hipocampo` itself, or a vault's stored content) — it says nothing about, and does not change, the language any operator converses in with an agent. Mau's own working conversations continue in Brazilian Portuguese; that is an independent choice from what language ends up committed to a repository.

## Rationale

`hipocampo` is a single canonical spec everyone reads, including non-Portuguese speakers evaluating or adopting the methodology (MODA conformance work, in particular) — one language avoids the two-of-everything problem a bilingual spec would create, and English is the language MODA itself and its conformance artifacts are already written in. A vault, by contrast, is personal or corporate content whose language is a property of its owner's actual working language, not of the methodology — conflating the two would either force real vaults to translate for no operational reason, or leave the scaffold's own default language undeclared and only discoverable by reading the generated files one at a time.

## Discarded alternatives

- **Leave vault content language undeclared, inferred from file content.** Discarded — inference is unreliable at the frontmatter-first reading layer (`SPEC.md` section 2-B) the methodology already depends on for cheap triage; a declared field costs nothing and removes the guesswork.
- **Default the vault manifest's language to match the operator's most common vault.** Discarded — no such default exists generically across adopters; `"en"`, matching the scaffold's own language, is the only default that doesn't require the profile to already know something specific about the operator.
- **Also govern the language an operator converses in with an agent.** Out of scope — this decision governs what's written *in a repository*, not the language Mau or any operator uses when talking to an agent; those are independent and this decision does not touch the second one.
