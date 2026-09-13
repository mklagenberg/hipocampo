# Change Set 0089 — V3 operational event envelope

## Intent

Implement X6.1 as a bounded candidate event envelope with redaction and proof
limits.

## Scope

Add the event engine, operational-event contract, fixture integration and the
candidate Decision Record. No durable host log is enabled.

## Acceptance criteria

- layers are distinct;
- sensitive keys are redacted;
- proof scope and limits are explicit;
- event output is not a content mirror;
- deterministic validation passes.
