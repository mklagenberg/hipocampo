# Validation and revalidation loop

This procedure governs deterministic correction work. It does not authorize a
scope change, a write, or a semantic decision by itself.

## Sequence

1. Capture the failing check, exact input, rule revision, and affected path.
2. Classify the failure as structural, contract, compatibility, package,
   provenance, or semantic/human-boundary.
3. Consult the authoritative contract and identify the smallest in-scope
   correction.
4. Apply only that correction, preserving provenance and unrelated work.
5. Re-run the failing check, then the relevant regression set.
6. Record the result, remaining limitations, and evidence link.

## Stop conditions

Stop and escalate when the requested correction changes policy or intent, the
authoritative source is unavailable, the same failure repeats without new
evidence, the proposed fix would broaden scope, or a human/host decision is
required. A stopped loop is not a passing validation.

The structured scenarios in `docs/validation-loop-fixtures.yaml` and
`scripts/validate_validation_loop.py` check the decision shape, not the truth
of repository content.
