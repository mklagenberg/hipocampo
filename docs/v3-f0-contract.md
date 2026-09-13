# V3 F0 — deterministic review and proof boundaries

F0 is the final integrated review of deterministic scripts after the V3
contracts are assembled. It does not make semantic judgment deterministic. It
classifies each script at script level, applies verification by lifecycle
phase, uses a layered operational envelope, and reports typed outcomes when
proof is incomplete.

## Script classification

The current candidate classifies each relevant script as `deterministic`,
`cognitive`, `human`, or `hybrid`. Script-level classification is intentional
for this wave; operation-level classification is a future evolution.

## Phase matrix

Execution, review, publication, migration and retraction/revocation have
different required checks and blocking results. A check that is sufficient for
local execution is not automatically sufficient for publication or migration.

## Layered evidence

Events use a common envelope with operation-specific extensions. The envelope
records rule revision, proof scope, result, coverage, limits, correlation,
evidence, redaction and retention. It never becomes a content mirror.

## Typed outcomes

The candidate distinguishes `completed`, `partial`, `observational`,
`authorization_required`, `unavailable` and `blocked`. A missing proof blocks
only when the applicable phase and purpose require it. Semantic uncertainty is
transparent and traceable; it is not silently converted into deterministic
truth.

## Candidate boundary

F0 does not migrate vaults, transport Packages remotely, publish a release,
activate V3 or prove enforcement on external hosts. It prepares the candidate
for the later migration, LTE and human publication gates.
