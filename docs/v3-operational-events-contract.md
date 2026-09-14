# V3 candidate — operational event envelope

**Status:** unreleased V3 candidate; derived from D6.1 and D6.2.

Operational events are deterministic transparency and traceability records.
They are not Records, Packages, ledgers, authority declarations or a second
source of knowledge. The event proves the occurrence that was recorded and its
limits; it does not prove semantic truth and is **not a content mirror**.

When a durable event must be persisted in a vault, its canonical namespace is
`meta/events/`. Transient session context and sensory capture do not become
durable event files merely because they existed during an operation.

## Layers

- `transient_session`: temporary context or cache; not durable knowledge;
- `sensory_capture`: captured only after explicit authorization;
- `durable_operational`: bounded audit metadata, never a content mirror.

## Envelope

An event declares `event_id`, `event_type`, `layer`, actor roles, target,
payload, `rule_revision`, `proof_scope`, `limits`, `retention` and, when
available, correlation and host-capability references.

The actor roles `author`, `approver`, `executor` and `delegator` are separate.
Package identity remains in the Package, including `package_authority` and
`source_authority`; an event references the Package but does not copy it.

## Redaction and rollback

Credentials, secrets and source or knowledge bodies are redacted before an
event is persisted. A correction is an additive compensating event; the
original event is not silently erased.

## Example

```yaml
event_type: package_delivered
layer: durable_operational
target: {package_id: PKG-001, vault_id: gauge-vault}
payload: {result: completed, fingerprint: sha256:example}
rule_revision: v3.0.0-x6.1
proof_scope: local-checkout
limits: ["does not prove semantic truth", "does not revoke external backups"]
retention: operational-policy
```
