# Change Set — 0046: Repository content always overrides local skill state (Invariant 6)

## Summary

Adds a sixth invariant to `SPEC.md` section 8: content declared in the repository always overrides locally-cached or customized skill state. Closes a gap none of the existing lotes addressed directly — the personal skill copy that operates an instance can hold state (a hand-filled pointer, an ephemeral session cache, or simply a stale local copy) that disagrees with what the repository's own structured files (`AGENTS.md`, `hipocampo.yaml`, and now `profile.md` from Lote C) actually declare, and nothing in `SPEC.md` previously said which one wins.

The invariant is worded generically — "content declared in the repository," not a closed list of file names — so it covers `profile.md` today and any future structured repository file without needing amendment. It resolves unambiguously only on the condition that no two repository-side files declare the same field, which is the underlying reason `AGENTS.md`'s "instance type" field is already recommended for retirement (`decisions/0041`) rather than kept as a duplicate echo of the manifest.

This is a different axis from the existing agent precedence hierarchy (section 8): that hierarchy governs which *rule* applies once the instance's documented state is known; this invariant governs whether the *local skill copy's view* of that state can be trusted, or whether the repository must be re-read. See `decisions/0046-repository-content-overrides-skill-local-state.md` for the full Context/Decision/Rationale.

This is Lote D of the v2.0.0 taxonomy revision sequencing — standalone by design (a different category from Lotes A–C's content/discovery taxonomy work: this is skill-versus-repository governance). It textually cites `profile.md` as an example, so it is sequenced after Lote C, whose merge introduced that file.

## Class

**normative** — adds a new invariant to `SPEC.md` section 8, the strongest category of rule this methodology has ("no instance overrides these, under any circumstance").

## Semver

**minor** — no existing instance becomes formally incompatible with no action. The invariant governs the personal skill's own behavior (which source it trusts when local state and repository content disagree), not a schema or frontmatter field any content repository must newly satisfy. It does not remove `AGENTS.md`'s "instance type" field — that stays "recommended for retirement," exactly as Lote A left it (`decisions/0041`); no instance is forced to change anything as a result of this Change Set. Per `decisions/0023`'s operational test, this is MINOR — consistent with the independent classification already applied to Lotes B and C, and a deliberate divergence from the original planning document's rougher "lotes A–D are probably all MAJOR" framing, which was driven primarily by Lote A's `domain` → `entity` schema break and does not hold for this lote considered on its own.

## Triggers fired

| Trigger | Triggered? | Note |
|---|---|---|
| `regra_normativa` | Yes | A new invariant in `SPEC.md` section 8 — the strongest category of normative rule the methodology has. |
| `schema_frontmatter` | No | No document frontmatter field, `hipocampo.yaml` field, or `profile.md` field is added or changed — the invariant is a precedence rule referencing existing structured files, not a schema change to any of them. |
| `mecanismo_cross_repositorio` | No | Sections 6 and 13 (Registry, Promote/Depromote/Redbutton) are unchanged. |
| `politica_dados_sensiveis` | No | Section 2-A is unchanged. |
| `release` | Reserved | Evaluated at the v2.0.0 release closing, not in this isolated Change Set. |

## Impact

See `impact.yaml`.

## Known, not addressed here

- **No automated drift detection.** The invariant states the resolution rule (repository wins) but does not introduce any mechanism that automatically detects when local skill state and repository content actually disagree — that remains agent-executed judgment at read time (the same posture `decisions/0018`'s frontmatter validation already takes toward other classes of inconsistency), not a deterministic check `scripts/validate_hipocampo.py` or an equivalent tool runs. Flagged in `conformance/moda.yaml`'s `packaging_and_synchronization` control as a real, acknowledged gap.
- **`AGENTS.md`'s "instance type" field is not removed.** This Change Set reinforces the existing rationale for its retirement (`decisions/0041`) but does not itself retire it from any real instance — that remains each instance operator's own opportunistic migration, per `UPGRADE.md`'s standing posture toward every other optional capability.
