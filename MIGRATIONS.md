# Hipocampo — Migrations

Migration guide for each MAJOR version jump (SemVer — see SPEC.md, section 9, and DISCLAIMER.md).

MINOR and PATCH migration requires no action — see DISCLAIMER.md, section "Versioning and what it means for you". This file only documents MAJOR jumps, which require active migration by definition.

## How to use this document

Each instance declares, in its own `CLAUDE.md`/README, the version or compatibility range it implements. When a new MAJOR version is released, find here the section corresponding to the jump you need to make (for example, "1.x → 2.0") before updating your instance's version declaration.

## 2.x → 3.0 (V3 candidate; not active)

V3 is sovereign over V2.2, but existing V2.x vaults remain readable until an
explicit migration is approved. This section is a planning boundary for the
unreleased V3 candidate; it is not an instruction to migrate a real vault.

### Required preconditions

Before a real migration, the operator must have:

1. a target V3 contract and compatibility tuple;
2. a vault-specific inventory and source-version declaration;
3. the completed [V2.2-to-V3 resolution matrix](docs/v3-v22-resolution-matrix.yaml);
4. a field and semantic mapping for every selected Record, Chunk, Artifact and
   Package;
5. a privacy recheck for source, destination, representations and derived
   material;
6. a tested rollback plan and a destination contract;
7. explicit human approval for that vault and migration scope.

Missing mapping, unknown privacy, unavailable destination, missing rollback or
missing approval blocks migration.

The synthetic preflight cases in
`docs/v3-migration-fixtures.yaml` and their deterministic evaluator in
`scripts/validate_v3_migration.py` are the first executable check of this
boundary. They are not evidence that any real vault is ready.

Vault-level preparation is exercised separately by
`docs/v3-synthetic-vault-inventories.yaml` and
`scripts/validate_v3_inventory.py`. The profiles are sanitized and cover
anchor, additional and inaccessible-vault cases; they do not discover or
classify real repositories.

### Migration dispositions

- V2.2 records remain readable as `legacy-unmapped` until processed.
- V2 frontmatter is preserved as source material; V3 state, maturity,
  staleness and provenance are not inferred from one another.
- V2.2 compatibility, session and access evidence is retained as provenance or
  regression evidence, not promoted to V3 authority automatically.
- The V2.2 pending-access fallback is not a V3 permission. Any provisional
  destination must pass V3 privacy, minimization, authority and acceptance
  rules.
- External artifact references remain references until the destination and
  representation are explicitly verified; a hash proves identity, not truth,
  permission or authority.
- Skill installation or recovery is a separate client-side operation and is
  not performed by vault migration.

### Execution sequence

1. Freeze the selected source inventory and capture its version and hashes.
2. Resolve compatibility and target access without writing.
3. Apply the approved mapping to synthetic fixtures first.
4. Review split, merge, privacy, provenance, authority and destination results.
5. Obtain human approval for the exact vault and Change Set.
6. Execute with rollback evidence and a migration receipt.
7. Run V3 validation and REM before any record becomes current or curated.
8. Reconcile the source and destination ledgers, then close the migration only
   when the LTE gate accepts the evidence.

No step above authorizes remote transport, publication, deletion or V3
activation by itself.

## History of MAJOR jumps

## 1.x → 2.0

The v2.0.0 jump is being assembled across several PRs (lotes), each accepted independently — this section accumulates as each one lands, rather than waiting for a single combined change. Steps below are grouped by the lote that introduced them.

### Entity model replaces `domain` (`decisions/0040`, `decisions/0041`)

**What broke:** `hipocampo.yaml`'s `instance.domain` field (`personal`/`company`) is replaced by three fields: `instance.entity`, `instance.role`, and `instance.scope_description`. An instance whose manifest still declares `instance.domain` does not satisfy the current schema.

**Why:** `decisions/0041-entity-model-and-vault-vocabulary.md` — `domain`'s fixed two-value enum doesn't express multiple entities or more than one vault per entity, both now explicit design premises (`decisions/0040-multi-vault-multi-entity-design-premises.md`).

**Step by step:**
1. Open the instance's `hipocampo.yaml`. If it has no `instance.domain` field yet (the manifest itself was never adopted, a pending item since `decisions/0033`), skip straight to generating one from `scaffold/skeleton/hipocampo.yaml` with the new fields already.
2. Replace `instance.domain: "personal"` with `instance.entity: "personal"` and `instance.role: "anchor"` — for a single-vault personal instance, this is a direct, unambiguous rename.
3. Replace `instance.domain: "company"` with `instance.entity: "<the specific company's identifier>"` (previously implicit in "company" alone) and `instance.role: "anchor"` for that entity's confidential vault, or `instance.role: "additional"` plus a `instance.scope_description` for any other vault of the same entity — this step requires a human decision (what the entity should be called), not a mechanical rename.
4. If the instance's `AGENTS.md` still declares "Instance type", it may stay as-is (recommended for retirement, not required) — see `decisions/0041`.

**How to know if your instance can migrate already:** any instance can migrate at any time — the new fields don't depend on any other pending lote of this MAJOR jump. Migration is per-instance, never automatic (`UPGRADE.md`, "How to use").
