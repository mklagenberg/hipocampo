# Compatibility contract

`COMPATIBILITY.yaml` is the canonical decision surface for whether a client-side
Hipocampo skill, this methodology release, and a content-vault manifest can
operate together. It does not replace `UPGRADE.md` or `MIGRATIONS.md`: the
matrix answers **whether operation may proceed**, while those guides explain
what an operator must do next.

## Decision chain

The check reads, in order: access to the required sources; the skill manifest
and package lock; the methodology version and specification; and the vault's
`hipocampo.yaml`. It produces one of five states:

| State | Operation | Meaning |
|---|---|---|
| `compatible` | allowed | All required declarations and integrity checks pass. |
| `compatible_with_upgrade` | allowed with notice | The tuple works, but a non-blocking upgrade is recommended. |
| `migration_required` | blocked | The vault's declared methodology contract is formally incompatible. |
| `unsupported_or_unknown` | blocked | A required value is missing, malformed, or outside the declared support. |
| `access_unavailable` | blocked | A required source could not be read. |

An unknown result never becomes an implicit permission. The agent explains the
chain `skill → methodology → vault conformity → local review → permitted
action`, then hands the decision back to the operator when review is required.

## Validation

Run `python scripts/validate_compatibility.py --root .`. The validator checks
the current canonical tuple and all fixtures in
`docs/compatibility-fixtures.yaml`. To evaluate a specific vault, pass its
manifest with `--vault-manifest path/to/hipocampo.yaml`. It is deterministic
validation of declared contracts, not proof that a remote vault is reachable
or that a human has accepted a migration.
