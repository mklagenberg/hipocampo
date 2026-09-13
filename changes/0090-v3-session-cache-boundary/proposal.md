# Change Set 0090 — V3 session and cache boundary

## Intent

Implement X6.2's explicit boundary between transient context, cache, sensory
capture and durable operational events.

## Scope

Add session disposition primitives, contract documentation and fixtures.

## Acceptance criteria

- unauthorized context is discarded;
- authorized capture is explicit;
- interruption and restart do not create knowledge;
- host retention limits remain visible.
