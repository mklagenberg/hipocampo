# Change Set 0074 — V3 entity-aware CRUD and vault profiles

## Intent

Implement and exercise the unreleased V3 boundary in which CRUD resolves
Source, entity, scope, vault profile, governance role, and destination contract
before it creates, reads, updates, splits, or sends knowledge.

## Problem

The existing candidate CRUD contract validates Record–Chunk integrity and
Package restrictions, but does not yet model the difference between a personal,
team, and entity vault or distinguish Owner, Authority, Curator, User, and
Source. It therefore cannot safely express a single capture split between a
Personal Vault and a project Team Vault.

## Proposed contract

- add candidate profiles `entity`, `team`, and `personal`;
- keep `instance.entity` and `instance.role` (`anchor`/`additional`) separate
  from the profile;
- preserve the private-anchor and non-reciprocal-access rules;
- add entity-aware operation validation for actors, roles, Source, scope,
  visibility, maturity, staleness, authority, and destination contract;
- support explicit Source-preserving splits into entity-bound Records/Chunks;
- distinguish intra-entity and inter-entity sending;
- block missing authorization, destination compatibility, or required authority;
- exercise positive and negative in-memory fixtures.

## Out of scope

This Change Set does not activate V3 for existing instances, migrate vaults,
perform remote transport, enforce real permissions, create a general derived
projection layer, synchronize split representations, or publish a release.

## Compatibility and rollback

The active released contract remains v2.1.1. V2 instances remain readable.
Reverting this Change Set removes the unreleased candidate additions without
deleting historical decisions or changing a vault. A future V3 release still
requires migration planning, skill review, release validation, and human
publication approval.

## Acceptance

- entity, profile, role, Source, and actor-role context are validated;
- Owner, Authority, Curator, and User remain distinct;
- split records preserve parent context and Source lineage;
- incompatible entity-boundary sharing is blocked;
- intra-entity and inter-entity transfer gates differ;
- personal, team, and entity profile fixtures cover allowed and blocked paths;
- existing Record–Chunk–Package fixtures remain green.
