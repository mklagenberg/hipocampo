# V3 — Semantic Revalidation Report Under the Constitution

**Run:** `RUN-20260914-semantic-revalidation-constitution`
**Normative basis:** `management/CONSTITUTION.md` v1.0.0, `FF-DEC-0060`, and `v3-constitutional-test-basis.yaml`
**Prior round:** `v3-semantic-review.yaml`
**Scope:** 28 semantic cases across 11 logical engines, with two judgment passes and one adversarial pass.

## Result

The suite was rerun as a versioned round. The current round confronted each case with the Constitution and the Decision Record basis while preserving the prior round as history. The immediate prior review contains 28 cases; its four constitutional edge cases were already added by the preceding revalidation. The committed historical baseline contains 24 cases. All 28 cases in the immediate prior review retained their disposition: 12 `blocked`, 11 `needs_review`, 4 `provisional`, and 1 `rework_required`.

The constitutional judgment found 25 directly compatible cases and 3 conditionally compatible cases. No case was conflicting, obsolete, or without a normative basis. The conditions concern constitutional exceptions and re-judgment after a constitutional amendment; they do not authorize promotion, direct writing, or publication.

| Check | Result |
|---|---:|
| Cases rerun | 28 |
| Cases compared with prior round | 28 |
| Cases in committed historical baseline | 24 |
| Prior constitutional edge cases retained | 4 |
| Dispositions preserved | 28 |
| Dispositions changed | 0 |
| Semantic passes | 2 |
| Record mutations | 0 |
| Engines covered | 11 |

## Conclusion boundaries

This round confirms coherence among cases, dispositions, the Constitution, and Decision Records. It does not turn semantic judgment into factual truth or replace the human review required by pending cases. The result remains a validated deliverable with residual human gates, not authorization for publication, migration, or merge.

No cache vault, remote vault, or knowledge Record was changed. The run used only sanitized fixtures and local deliverable artifacts.

## Reproducibility

The deterministic comparator is `scripts/validate_v3_semantic_constitutional_revalidation.py`. The engine suite now executes this comparator through the `semantic_revalidation_command` policy in `docs/engines/test-matrix.yaml`, in addition to the existing deterministic commands.
