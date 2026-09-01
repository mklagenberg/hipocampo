# Change Set — 0058: canonical compatibility contract

## Summary

Introduces a single, versioned compatibility decision surface for the
client-side skill, the Hipocampo methodology, and a content-vault manifest.

## Class and SemVer

**Normative; MINOR.** Existing v2.1.x vaults remain valid without action. The
new contract adds a capability and blocks only when an operator asks for a
compatibility decision that is unknown, inaccessible, or formally incompatible.

## Proposed contract

`COMPATIBILITY.yaml` defines the supported tuple, required declarations, five
explicit states, and precedence. `scripts/validate_compatibility.py` checks the
canonical self-declared tuple and deterministic fixtures. Unknown never means
compatible; migration guidance remains in `UPGRADE.md` and `MIGRATIONS.md`.

The new pre-operation gate changes the skill's behavior and therefore is
prepared as skill package version `1.3.0`; the methodology remains on its
current release line. The package version bump is independent and must be
published through the skill's own release process.

## Acceptance criteria

- The current skill/methodology tuple validates as `compatible`.
- Unknown, inaccessible, unverified, and incompatible cases have explicit
  non-permissive outcomes.
- The methodology explains the decision chain in `docs/compatibility.md`.
- The new validator and existing repository validators pass.

## Compatibility and migration

No existing vault field becomes mandatory in this Change Set. Adoption of the
matrix is recommended for future operations; a future release may add a
manifest-level compatibility check only through a separately reviewed change.

## Recovery

If the matrix or validator rejects a valid tuple, correct the contract through
a new reviewed Change Set. Never bypass an unknown result by treating it as
compatible.

## Semantic review

Reviewed against the committed diff `9fdb2cb` and the current repository
contracts. The declared updated surfaces match the implementation. `README.md`
and `MIGRATIONS.md` were intentionally left unchanged because no methodology
release was cut and no migration was introduced. The skill behavior change
warrants independent candidate version `1.3.0`; publication remains a separate
human release gate.

## Status

`implemented locally`
