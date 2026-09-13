# V3 candidate — session and cache boundary

**Status:** unreleased V3 candidate; derived from D6.1 and D6.5.

Session context and cache are transient surfaces. They do not become durable
Hipocampo knowledge by being visible to an agent. A sensory capture requires
explicit authorization and remains distinct from an operational log.

When capture is not explicitly authorized, the disposition is
`discard_transient_context`. Interruption and restart must not silently turn
the previous context into a Record. Host limitations around cache retention are
reported as `observational` or `unavailable`.
