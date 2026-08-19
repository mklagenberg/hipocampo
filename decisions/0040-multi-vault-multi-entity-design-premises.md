# 0040 — Multi-vault and multi-entity design premises

**Status:** Accepted

## Context

A taxonomy review toward v2.0.0 (whiteboard redesign session, 2026-08) surfaced three assumptions that were true in practice but never stated as explicit design premises, and one real design bug caused by their absence.

`domain` (`decisions/0002`/`0029`) is a fixed two-value enum (`personal`/`company`). In real use, a single person already operates more than one company-scoped instance (e.g., an employer relationship distinct from other future entities — family, a side project), and the same physical entity commonly needs more than the canonical two repositories (a confidential/public pair). Nothing in the existing model said whether this was the normal case or an edge case, and an earlier version of this same review round treated N-vaults-per-entity as rare, schema-only headroom — later corrected (see `decisions/0041`) once it became clear the premise, not just the schema, needed to change.

Separately, an earlier draft of this review proposed a hub-spoke discovery model: every additional vault of an entity points back to that entity's confidential anchor. This breaks under a real access pattern already true today — a user with access only to one vault of an entity has no way to read or write the anchor's reciprocal pointer that hub-spoke requires, and a second user in the same position, with access to a different vault of the same entity, is in the same bind. Chasing this bug down to its root exposed that the anchor vault had been implicitly treated as a universal funnel for capture (a stated "the `inbox/` only lives in the anchor" assumption), which is the same error in a different place: it presumes access nothing here actually guarantees.

## Decision

Three explicit design premises, going forward:

1. **Multi-vault and multi-entity by design.** The methodology is designed for multiple repositories and multiple entities; it works with a single vault, but that is a degraded case, not the target the schema and rituals are designed around. A single-vault instance gives up the per-repository access separation invariant 4 (`SPEC.md` section 8) provides — an operator choosing mono-vault is trading that away, not getting it for free.
2. **Confidential-first, always.** Information is confidential by default and promoted to public only as a later, explicit step (see the Promote action, `SPEC.md` section 13) — with no exception for content that looks "obviously public." There is never a direct write path to a public vault. This is a blanket rule specifically because it removes a judgment call ("is this ambiguous or not?") that is itself a point of failure — an agent guessing wrong about "obviousness" is a worse failure mode than an extra promotion step for content whose destination was never actually in doubt.
3. **Every entity has exactly one mandatory anchor vault (private), and may have any number of additional vaults (public, or additional private vaults with a narrower scope).** The anchor is a guarantee of existence — every entity, including each user's own "personal" entity, always has at least one private place for its content to land. It is **not** a universal funnel: after the hub-spoke bug above, no vault of an entity is assumed reachable by every user who has access to some other vault of that same entity. The guarantee premise 3 provides is narrower and more useful than that: every user always has *some* private landing place available to them — at minimum, their own personal anchor — even when the "correct" destination for a specific entity is out of their reach.

Two direct consequences of premise 3, both corrections to an earlier, narrower assumption in this same review:

- **Short-term memory is per-vault, not per-entity.** Every vault — anchor or additional — has its own `inbox/` (`SPEC.md` section 5-A). There is no single, entity-wide capture point.
- **Fallback with tag, for a known-but-unreachable destination.** When the correct destination for a captured item is a specific entity's vault, but the user doing the capturing does not have access to it, the item is not discarded and not force-written where it doesn't belong — it lands in that user's own personal vault's `inbox/`, marked with a tag indicating it does not permanently belong there. This is a distinct failure category from `decisions/0038`'s "insufficient evidence" mode: there, the agent does not know the correct destination; here, it knows exactly which vault is correct and only lacks access to it. The exact tag field format, and who is responsible for later resolving a tagged item, are open items — not resolved by this Decision Record.

A consequence of the fallback mechanism needing somewhere to land: **a user's own personal anchor vault is always the first vault instantiated for that user**, before access to any third-party entity is exercised — even when an invitation to a third-party entity's vault already exists at that point. Without this ordering, the fallback mechanism in the paragraph above has no vault to fall back to for that user. The full bootstrap procedure that enforces this ordering is specified separately, as its own mechanism; this Decision Record only establishes the premise it depends on.

## Rationale

Multi-user, multi-entity access is not a hypothetical this Decision Record is preparing for — it is already how Hipocampo is used today, across more than one real entity and more than one real collaborator with partial access. A model (hub-spoke) that only works when every participant has full reciprocal access to every vault of an entity does not describe that reality; it describes a simpler case that happens not to hold.

Confidential-first as a blanket rule, rather than "only for ambiguous cases," was a position this review changed mid-conversation: the narrower version was the initial proposal, revised once premise 3 (a private landing place always exists) made the blanket rule cost nothing beyond an extra step for the minority of content whose destination was never ambiguous.

## Discarded alternatives

- **Hub-spoke discovery** (every additional vault points back to its entity's anchor). Discarded — breaks for a user without access to the anchor, which is a real, already-existing access pattern, not a hypothetical.
- **Full-mesh discovery** (every vault of an entity points to every other). Discarded for the same underlying reason as hub-spoke, in the opposite direction — it still presumes reciprocal access no participant is guaranteed to have.
- **Confidential-first restricted to ambiguous cases only.** Discarded after premise 3 made the blanket rule free of the cost that motivated the narrower version — see Rationale.
- **Folding the fallback-with-tag case into `decisions/0038`'s "insufficient evidence" mode.** Discarded — the two situations are epistemically different (destination unknown vs. destination known but unreachable), and collapsing them would make `decisions/0038`'s mode name inaccurate for half of what it covered.
