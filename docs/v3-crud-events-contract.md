# V3 candidate — CRUD operational events

**Status:** unreleased V3 candidate; derived from D6.3.

Only governed CRUD and exceptional actions emit operational events. Every
durable Record mutation is a governed CRUD action; no engine or transport may
emit a Record write outside that boundary. The event
contains target identity, actor roles, entity, scope, operation, result,
approval linkage, rule revision, retention and redaction state. It does not contain a Record,
Chunk, Artifact or Package body.

When such an event is durably persisted by a vault, it belongs under
`meta/events/`, according to the layered operational-event contract.

Reads are not automatically durable knowledge events. A read is logged only
when the contract defines an auditable operational action, such as a governed
export, validation, retraction or privacy-sensitive access.
