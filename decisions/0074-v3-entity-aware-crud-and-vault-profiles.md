# 0074 — V3 entity-aware CRUD and vault profiles

**Status:** Accepted for the unreleased V3 contract

## Context

V3 knowledge may originate in one Source and require governed representations
for different entities, scopes, or vault contracts. A vault path alone cannot
decide where knowledge belongs. CRUD therefore needs to resolve the actor's
role, Source, entity, scope, vault profile, visibility, maturity, authority,
staleness, and destination contract before it creates, reads, updates, splits,
or sends a governed object.

The methodology already distinguishes an entity from a vault, and an anchor
from an additional vault (`decisions/0040` and `0041`). The new profiles must
not recreate hub-spoke access, make a profile authoritative, or make maturity
an exposure hierarchy.

## Decision

The unreleased V3 contract recognizes three vault policy profiles:

- **`entity`** — broad entity-scoped knowledge with stricter intake, curation,
  visibility, and delivery gates;
- **`team`** — collaborative knowledge for one entity, team, project, or
  initiative, including material that is new, provisional, conflicting, or
  ephemeral;
- **`personal`** — user-private knowledge, normally associated with the
  personal entity, with no automatic export or fallback of another entity's
  content.

The profile is independent from `instance.entity`, `instance.role` (`anchor`
or `additional`), Owner, Authority, Curator, User, maturity, epistemic nature,
visibility, and staleness. A profile does not grant authority, write access, or
automatic access to an entity anchor. The existing private-anchor and
non-reciprocal-access premises remain in force.

V3 distinguishes these roles:

- **Owner:** accountable for the vault/entity boundary, policy, authorization,
  and lifecycle;
- **Authority:** responsible for current knowledge within one entity and scope,
  subject to the single-active-authority and hereditary-succession rules;
- **Curator:** processes, classifies, normalizes, splits, reconciles, and
  assembles Packages without gaining authority by performing the work;
- **User:** reads, consumes, or operates under granted permissions.

`Source` is provenance, not a governance role. It may be a person, conversation,
observation, Artifact, Record, vault, external system, or another identifiable
origin. A Source may lead to more than one entity-bound representation, but one
mutable governed Chunk must not span incompatible entity contracts.

When a capture contains both personal and project-relevant material, CRUD may
perform an explicit governed split into separate Records or Chunks. Each split
preserves Source lineage, parent context, entity, scope, visibility, maturity,
and revalidation relations. Splits are not silent copies, general projections,
or automatic synchronization.

Every relevant CRUD operation must resolve:

1. actor and role;
2. Source and provenance;
3. entity and scope;
4. source vault and profile;
5. visibility, maturity, staleness, and authority;
6. whether a split is required;
7. destination-vault contract;
8. local, intra-entity, or inter-entity transfer mode.

Intra-entity sending uses the entity's shared contract but still validates
visibility, staleness, integrity, and authority. Inter-entity sending requires
destination compatibility, authorization, minimization, and destination
acceptance; it never inherits source authority.

## Rationale

The profile boundary makes the three vault policies explicit without collapsing
them into authority, maturity, visibility, or access inheritance. Entity-aware
CRUD is required before delivery because the same Source may legitimately
produce distinct personal and project Records, while a mutable Chunk must not
cross incompatible entity contracts. A split that crosses entities is subject
to the same destination acceptance, Owner approval, and minimization gates as
other inter-entity delivery.

## Consequences

- V3 CRUD becomes entity-aware before Package assembly rather than only at
  delivery time;
- a common Source can produce personal and project representations without
  mixing private and shared content;
- Record remains the persistence and governance unit, and Chunk remains a
  contextual child rather than an autonomous CRUD object;
- profile, Owner, Authority, Curator, User, Source, and Package generation stay
  distinct dimensions;
- deterministic checks validate declarations and mechanical restrictions,
  while semantic ownership, applicability, and split decisions remain gated;
- V2 remains readable and is not migrated or activated by this candidate.

## Discarded alternatives

- treating the physical vault as the sole entity classifier;
- inheriting anchor access from any vault of the same entity;
- using the profile as a universal authority or maturity hierarchy;
- allowing one mutable Chunk to span incompatible entity contracts;
- duplicating or synchronizing split content without Source lineage;
- using a Personal Vault as an automatic fallback for another entity.

## Evidence and validation

The candidate is exercised by `scripts/validate_v3_crud.py` and
`docs/v3-crud-fixtures.yaml`. The validator proves in-memory contract behavior;
it does not prove remote authorization, real transport, semantic truth,
migration, or publication.
