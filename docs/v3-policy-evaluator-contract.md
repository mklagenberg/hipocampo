# V3 joint policy evaluator

The X4.1 evaluator applies the origin and destination contracts independently.
It never treats authority as access, and it never treats access as authority.

The deterministic result is one of `permitido`, `redigido`, `provisório` or
`bloqueado`. Objective inability to evaluate identity, boundary, purpose or
visibility fails closed. Semantic uncertainty can remain `provisório` when the
destination contract accepts it; the evaluator does not choose semantic truth.

The explanation contains only the minimum entity, vault, purpose and rule
context needed for audit. It never copies protected content or inaccessible
source metadata.
