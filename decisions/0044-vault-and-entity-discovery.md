# 0044 — Vault and entity discovery, without a stored router

**Status:** Accepted

## Context

`SPEC.md` section 2-C (`decisions/0041`) introduced the entity model but deliberately left one question open: "the procedure an agent uses to discover this at runtime is specified separately (a distinct Decision Record, not this one)." This Decision Record is that separate specification.

Independently of that forward reference, the generic skill's `skill/references/personalization.md` already asks every adopter to hand-fill two static tables before first real use: a "repository router" (which repository plays which role) and a multi-account identity table (which git account is personal vs. professional). Both are a second source of truth for information that, after `decisions/0041`, is already declared repo-side — `entity`/`role`/`scope_description` in each vault's own `hipocampo.yaml`, and multi-account identity in `AGENTS.md` per `SPEC.md` section 12. A hand-filled local table can drift from what the repositories themselves declare, with no mechanism to catch the divergence — the same second-source-of-truth risk this methodology has already rejected elsewhere (`decisions/0004`'s rationale against `router.md` as a second alias table).

An earlier proposal, reviewed and rejected before this Decision Record was drafted, suggested closing the gap with a hub-and-spoke graph: every additional vault of an entity carries a pointer back to that entity's mandatory anchor vault. This breaks on a real, not hypothetical, case: user A has access only to Vault A of an entity, user B only to Vault B — neither is guaranteed access to the anchor vault to register the reciprocal pointer hub-spoke requires. Swapping to full-mesh (every vault points to every sibling) has the identical problem in the opposite direction — it still assumes reciprocal access no participant is actually guaranteed.

## Decision

**Discovery, not storage.** The skill does not persist a repository router. Instead, at the start of a session, it reads the manifest of the user's own anchor vault, discovers from there every entity and vault address (and identity metadata) that manifest declares, and caches the result in sensory memory — ephemeral, never versioned in git, rediscovered fresh each new session, without needing to ask again within the same one.

**No graph between sibling vaults.** Each vault self-declares only its own `entity`/`role`/`scope_description` (`SPEC.md` section 2-C) — no vault carries a pointer to any sibling, anchor or otherwise. Enumerating "every vault of entity X" is never something an entity's own vault does about itself; it is only ever computed from a specific user's own root manifest, for whichever vaults that user happens to have access to. This is not a second mechanism next to cross-entity discovery — it is the same pattern, applied recursively within one entity.

**Known limitation, not a blocker.** Access granted outside the agent's own instantiation flow (for example, a direct GitHub collaborator invite that never went through the Bootstrap mechanic, `decisions/0045`) is not auto-discovered — it requires manual registration in that case, the same posture section 14's "insufficient evidence" behavior already takes toward any gap the agent cannot close by itself.

**Consistency checking is simpler without back-pointers.** There is no "does every vault point back correctly" check to run, because no vault points anywhere. What remains to verify is only that each vault's own self-declaration (`entity`/`role`/`scope_description`) is still internally valid and its address is still reachable — folded into the existing weekly structural audit (`SPEC.md` section 5-C), not a new ritual.

**Step classification (section 8/14).** Reading and caching the root manifest is deterministic-or-discretionary, ungated — no durable write happens. Registering a new vault (the Instantiate action of the Bootstrap mechanic, `decisions/0045`) is gated, per invariant 5, same as any other durable write.

**`skill/references/personalization.md`'s router table is retired.** Both tables — the repository router and the multi-account identity table — stop being something an adopter hand-fills once; identity (which GitHub handle applies to which entity) is discovered from each vault's manifest the same way an address is, not tracked in a second local file. What remains genuinely, irreducibly local is a single pointer: which repository is the user's own anchor vault, needed before any manifest can be read at all. That pointer is not a router — it is one line, not a table — but this Decision Record does not name where it lives; that is an explicitly open item (see `decisions/0045` and the lote's tracking).

## Rationale

Discovery-from-source removes an entire class of drift bug (local table says one thing, repository manifests say another) at the cost of a small, bounded re-read at the start of each session — a trade this methodology has already made the same way elsewhere (frontmatter-first reading, section 2-B; light validation at every read, `decisions/0018`). Rejecting both hub-spoke and full-mesh in favor of no sibling graph at all is the only option of the three that does not assume symmetric access between users of the same entity, which is the actual, observed failure mode of the discarded alternatives.

## Discarded alternatives

- **Hub-spoke (every additional vault points back to its entity's anchor).** Discarded — assumes every vault-holder has access to register a pointer on the anchor, which is not guaranteed (the two-user, disjoint-access scenario in Context).
- **Full-mesh (every vault points to every sibling).** Discarded — same access-symmetry assumption as hub-spoke, in the opposite direction; also grows the write surface with every additional vault instead of shrinking it.
- **Keep `personalization.md`'s router and identity tables, scoped only to identity mapping.** Considered as a narrower fix (keep the table, but only for "which GitHub handle per entity," not full repository addresses) — discarded because the same discovery mechanism that resolves an address already resolves identity metadata from the same manifest; a second table for a subset of the same information reintroduces the drift risk this Decision Record exists to remove, for no remaining benefit.
