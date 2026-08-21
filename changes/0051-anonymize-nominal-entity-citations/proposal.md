# Change Set — 0051: Anonymize nominal entity citations across the methodology repository

## Summary

Removes every real, identifiable entity/person/handle citation found in the `hipocampo` repository — a real employer name and repository-path prefix, a real colleague's first name, and Mau's real personal GitHub handle, used across several documents as an author-identity example — replacing each with a clearly-marked anonymized placeholder (`Acme`/`org-acme`, `[Colleague]`, `@personal-handle`). This proposal deliberately does not restate the original real terms it replaced — doing so here would itself be exactly the nominal citation `decisions/0050` prohibits; the anonymized diff (see `impact.yaml`) and the repository's own commit history are the record of what changed. Establishes `decisions/0050-no-nominal-entity-citation-in-methodology-repository.md` as the durable, standing rule this Change Set executes for the first time, per Mau's direct instruction (2026-08-19): "Jamais, sob hipótese nenhuma, pode haver citação nominal de entidade etc no repo da metodologia. Sempre, todas as vezes, precisa ser anonimizado."

Touches seven files: `docs/evaluation-scenarios.md`, `decisions/0026-account-vs-opinion-in-corporate-instance.md`, `decisions/0039-minimal-evaluation-scenarios.md`, `decisions/0024-upgrade-md-cumulative-checklist.md`, `skill/references/instantiation.md`, the frozen `audits/moda/2026-08-17-v1.0.0-self-audit.md`, and the accepted Change Set `changes/0038-0039-failure-recovery-and-evaluation-scenarios/impact.yaml`. Only identifying tokens changed — no example's structure, taxonomy, decision, or pedagogical point was altered.

## Class

**operational** — corrects the repository's own content for a privacy/identification concern without adding, removing, or changing any normative obligation on a content instance; `SPEC.md`'s schema, invariants, and instance-facing rules are unaffected.

## Semver

**patch** — corrective, internal to this repository's own text; no existing content instance needs to take any action.

## Triggers fired

| Trigger | Triggered? | Note |
|---|---|---|
| `regra_normativa` | No | No `SPEC.md` obligation added, removed, or changed. |
| `schema_frontmatter` | No | Doesn't touch document frontmatter (`SPEC.md` section 2). |
| `mecanismo_cross_repositorio` | No | `registry.md`/`$alias:`/Promote/Depromote/Redbutton unaffected. |
| `politica_dados_sensiveis` | No (adjacent) | `SPEC.md` section 2-A governs sensitive data *inside a content instance*, not this repository's own reference text — but the same underlying privacy principle motivates `decisions/0050` as a standing rule for this repository. |
| `release` | No | Not a release cut. |

Classified `operational` per `docs/change-management.md`'s class table — a Change Set is required regardless of which trigger row fires, since every touched path is a protected surface (`decisions/`, `docs/`, `skill/`, an `audits/moda/` evidence file, and a `changes/` artifact).

## Discarded alternatives

- **Case-by-case risk judgment**, redacting only citations that looked clearly sensitive. Discarded per Mau's explicit instruction: unconditional, not risk-scored — see `decisions/0050`.
- **Editing `changes/0038-0039-.../impact.yaml`'s accepted-evidence entry silently, with no note.** Discarded: contradicts `docs/change-management.md`'s "never edited after acceptance, only superseded" without any record of why. Instead, made the narrowest possible token substitution (one artifact path) and appended an addendum note to the same entry, dated and cross-referencing this Change Set and `decisions/0050`, preserving the traceability the immutability rule exists to protect.
- **Fully superseding `changes/0038-0039-...` with a new Change Set instead of touching it at all.** Discarded as disproportionate: only a single artifact-path token in that Change Set names the real entity; the Change Set's own decision, classification, and evidence are otherwise correct and unchanged — superseding the whole thing would misrepresent that its substance changed, when only an identifying label did.
- **Rewriting `audits/moda/2026-08-17-v1.0.0-self-audit.md` wholesale, or striking the finding that cites the real case.** Discarded: the audit's own footer already declares it frozen evidence, "nunca editada após aceitação, só superseded por uma auditoria futura." Chose a minimal in-place token redaction (the same two identifiers redacted elsewhere) plus an appended, dated redaction note documenting exactly what changed and why — rather than either leaving real entity data in frozen, public evidence indefinitely, or rewriting the audit's actual findings/severity.
- **Leaving `skill/references/instantiation.md`'s real-company worked example alone**, reasoning that a single company name in a worked example is low-risk. Discarded: Mau's instruction is unconditional ("jamais, sob hipótese nenhuma"), not risk-scored, and the fictional replacement (`Acme`) costs the example nothing — `Acme` is already this repository's own established placeholder-company convention (`skill/references/routines.md`'s `case-acme.md`).
- **Inventing a new fictional colleague first name** (e.g. a different real-sounding name) instead of a bracketed placeholder. Discarded: a real-sounding substitute risks an accidental resemblance to an actual person and reads as another (fictional) nominal citation rather than a visible redaction; `[Colleague]` is unambiguous.

## Risks

- The addendum notes added to the frozen audit and the accepted Change Set are themselves new prose appended to otherwise-frozen files — a narrow, deliberate, and logged exception to `docs/change-management.md`'s immutability rule, made only to remove identifying tokens. If this precedent is invoked again for unrelated reasons in the future, that would be scope creep beyond what this Change Set authorizes; `decisions/0050` documents the rule as prospective policy specifically so future real-entity citations are caught before merge, not after.
- Anonymization is a manual, human/agent-reviewed process, not automated — a future real-entity citation could still slip into a new contribution. No CI check for this exists yet (out of scope for this Change Set; a possible future addition to `scripts/validate_hipocampo.py` or `scripts/validate_change.py`, not attempted here since it would require a maintained list of names to match against, itself sensitive content this repository shouldn't store).

## Acceptance criteria

- None of the seven files listed in `impact.yaml` contain any of the real identifying terms this Change Set redacts (verified by repository-wide case-insensitive grep for those exact terms as part of this Change Set's validation — the search terms themselves are not reproduced in this proposal, per `decisions/0050`).
- `python3 scripts/validate_hipocampo.py --root .` passes with 0 errors.
- `python3 scripts/validate_skill_docs.py --root .` passes with 0 errors.
- `python3 scripts/validate_change.py --root .` passes with 0 errors, including this Change Set's own schema and diff-coverage check.

## Compatibility / migration

None — no existing content instance needs to take any action; this is a correction to the methodology repository's own text.

## Recovery

If a future contribution reintroduces a real entity citation, it is corrected the same way — direct edit for a live reference document, a narrow logged addendum for frozen/accepted evidence — under the same standing policy (`decisions/0050`), citing this Change Set as precedent. If the anonymization scheme chosen here (`Acme`/`[Colleague]`/`@personal-handle`) proves inadequate, a follow-up Change Set revises it; this one is marked `superseded`, never edited in place, per the same rule it documents.

## Impact

See `impact.yaml`.

## Status

`implemented` — already executed in this same Change Set.
