# Change Set 0100 — V3 synthetic vault inventory gate

## Intent

Classify sanitized vault-shaped migration inventories before any real-vault
inventory is prepared.

## Scope

Add synthetic profiles for personal and corporate anchors, an additional vault
with a bounded inaccessible artifact frontier, and an inaccessible invited
vault. Add a deterministic evaluator and validator.

This Change Set does not read or modify real vaults, discover repositories,
fetch artifacts, transport packages, install a skill, publish a release or
activate V3.

## Acceptance criteria

- each profile declares entity, role, versions, access and migration gates;
- profiles cover ready, authorization-required, partial and blocked outcomes;
- an inaccessible artifact reference remains explicit and bounded;
- an inaccessible vault cannot expose or infer its content or identity;
- the validator checks uniqueness, required fields and expected outcomes;
- the validator is included in the F0 script inventory.
