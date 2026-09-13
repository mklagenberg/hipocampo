# V3 candidate — operational correlation

**Status:** unreleased V3 candidate; derived from D6.3 and D6.2.

The correlation envelope uses `correlation_id`, `causation_id`, object IDs,
fingerprints, evidence references, rule revision and state. It may relate CRUD,
Package assembly, receipt, validation, evaluation, publication preparation and
retraction without becoming an authority or content mirror.

Entity and vault boundaries remain active. If a vault is inaccessible, the
correlation records an `inaccessible_frontier`; it does not infer or reveal the
missing source body.
