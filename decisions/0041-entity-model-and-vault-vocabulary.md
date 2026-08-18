# 0041 — Entity model replaces domain; vault vocabulary generalized

**Status:** Accepted

## Context

`domain` (`personal`/`company`, `decisions/0002`/`0029`) is a fixed two-value enum. `decisions/0040` establishes that Hipocampo is designed for multiple entities, not just the two `domain` currently distinguishes — a person may operate more than one company-scoped instance, a family entity, or any other future grouping, and a single entity may legitimately have more than the canonical confidential/public pair of vaults (also `decisions/0040`, premise 3).

Separately, "vault" today carries an implicit narrow sense — only the confidential member of a domain's pair has historically taken the `-vault` suffix, which is also why the four real repositories (`hipocampo-concepts`, `hipocampo-personal-vault`, `hipocampo-company`, `hipocampo-company-vault`) are asymmetrically named: two carry the suffix, two don't, for no reason beyond which member of the pair they are.

`AGENTS.md`'s "Instance type" field (`corporate`/`personal`) already runs in parallel to `domain`, unharmonized by design (`decisions/0033`, "this divergence is known and deliberately **not** resolved by this DR"). Replacing `domain` with a new, extensible concept is the point at which that divergence becomes worth resolving, since "Instance type" would otherwise be left pointing at a retired field.

## Decision

**1. `entity` replaces `domain` as the concept a repository (vault) belongs to.** An entity is an extensible identifier — `personal`, a specific company, a family, or anything else an operator introduces — not a fixed enum. The existing `personal`/`company` values remain valid entity identifiers (the smallest possible entity set: one personal entity, one company entity); nothing about existing content requires renaming, only the field's meaning widens from "one of two categories" to "any entity the operator declares."

**2. `hipocampo.yaml` (`decisions/0033`) is extended: `instance.domain` is replaced by three fields:**

```yaml
instance:
  entity: "<fill in: entity identifier, e.g. personal, or a specific company/family name>"
  role: "<fill in: anchor | additional>"
  scope_description: "<fill in only when role: additional — what belongs in this vault>"
```

`role: anchor` marks the entity's one mandatory, guaranteed-private vault (`decisions/0040`, premise 3); `role: additional` marks any further vault of the same entity (public, or private with a narrower purpose), which must also declare `scope_description` — a short, free-text statement of what belongs there. No vault lists its siblings: which other vaults belong to the same entity is never something one vault's manifest declares about another — it is only ever knowable from the root manifest of a specific user with access to more than one of them. This is a direct consequence of `decisions/0040` retiring the hub-spoke model; a discovery procedure that actually reads this information at runtime is specified separately, as a Decision Record of its own.

When an additional vault's `scope_description` isn't enough, on its own, to decide where a specific item belongs among more than one candidate vault of the same entity, that is not a new failure mode — it is already covered by `decisions/0038`'s "insufficient evidence" behavior: the agent surfaces the ambiguity to the human rather than guessing.

`instance.tier` (curation-level, `content`/`vault`, `decisions/0033`) is unchanged by this decision — it remains a distinct, unresolved-by-design concept from exposure tier (see `SPEC.md` section 2-C's "Known, separate inconsistency" note, unchanged).

**3. "Vault" is redefined as a generic noun.** It now means any knowledge repository this methodology generates or governs — confidential or public — not only the confidential member of a domain's pair. Exposure tier is carried by the repository's own name going forward (a `restricted`/`open` suffix convention, e.g. `<entity>-restricted-vault`, `<entity>-open-vault`), not implied by whether the word "vault" appears at all. Renaming Mau's four real repositories to this convention is a real, separate migration action, out of scope for this repository (`hipocampo` never stores a real repository's name) — tracked as a pending operator action, not as content of this Decision Record.

**4. `AGENTS.md`'s "Instance type" field (`corporate`/`personal`) is recommended for retirement**, not immediately removed. With `entity`+`role` now carrying the equivalent information (any `role: anchor` vault whose `entity` isn't `personal` is, in effect, corporate; a `personal`-entity vault is personal), keeping "Instance type" as a manually-filled, no-longer-authoritative echo of the manifest recreates exactly the kind of divergence risk this schema change is meant to reduce. This does not retroactively edit any real instance's `AGENTS.md` — that is a per-instance `UPGRADE.md`/`MIGRATIONS.md` action, not something this repository does on an operator's behalf.

**5. `docs/vocabulary-dictionary.md` is updated**: a new "Change history" entry records that `instance.domain` is superseded by `instance.entity`/`instance.role`, and that "vault" no longer implies exposure tier. The "Known, unresolved inconsistencies" note about `domain` vs. "Instance type" is updated to reflect that `domain` is now superseded (not merely a parallel vocabulary) and that "Instance type" is recommended for retirement rather than indefinitely unharmonized.

## Rationale

Extending the manifest instead of introducing a new router file follows the same reasoning `decisions/0030` already used to reject a fourth cross-repository action: don't build a second mechanism for something the first one (the manifest, `decisions/0033`) already has room for. Self-declaration without sibling pointers is the direct fix for the hub-spoke bug `decisions/0040` documents — the manifest only ever needs to describe the vault it lives in, never any other vault, which is exactly what breaks the reciprocal-access assumption hub-spoke depended on.

Recommending "Instance type" for retirement, rather than leaving it as a second, permanently unharmonized vocabulary the way `decisions/0033` originally chose to, is a direct consequence of `entity`/`role` now being expressive enough to derive it — the condition that made harmonization out of scope in `decisions/0033` (a smaller, narrower schema that couldn't yet express the distinction cleanly) no longer holds once this decision lands.

## Discarded alternatives

- **A new `router.md` file per vault**, listing every other vault reachable from it. Discarded — duplicates the manifest `decisions/0033` already introduced, for the same reason `decisions/0030` rejected a fourth lifecycle action instead of reusing existing mechanics.
- **Keep `domain` and add `entity` alongside it, rather than replacing.** Discarded — running two fields for the same underlying concept recreates the exact `domain`/"Instance type" divergence this decision otherwise resolves, just at one more layer.
- **Harmonize `entity`/`role` into `AGENTS.md`'s "Instance type" field immediately, editing every real instance now.** Discarded — out of scope for a normative-repository change; real vault edits are a per-instance `UPGRADE.md` action, and `decisions/0033` already established the precedent of naming a divergence without forcing a same-PR fix across real repositories.
- **Reintroduce a symmetric "structuring" third exposure tier while extending the schema.** Not revisited here — `decisions/0029`'s reasoning against a third tier is orthogonal to the entity/vault changes in this decision and still holds.
