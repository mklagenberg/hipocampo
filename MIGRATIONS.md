# Hipocampo — Migrations

Migration guide for each MAJOR version jump (SemVer — see SPEC.md, section 9, and DISCLAIMER.md).

MINOR and PATCH migration requires no action — see DISCLAIMER.md, section "Versioning and what it means for you". This file only documents MAJOR jumps, which require active migration by definition.

## How to use this document

Each instance declares, in its own `CLAUDE.md`/README, the version or compatibility range it implements. When a new MAJOR version is released, find here the section corresponding to the jump you need to make (for example, "1.x → 2.0") before updating your instance's version declaration.

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
