# Change Set 0133 — V3 publication boundary cleanup

## Problem

The final pre-publication audit found a real third-party identifier in accepted
Decision 0117, contrary to accepted Decision 0050; consumed operator-specific
PR/publication/readiness drafts are in the public source; local private and
temporary working roots are not ignored. The previous approved release commit
is already on main. A later correction does not erase its Git history.

## Proposed change and acceptance criteria

- Apply the narrow anonymization and dated annotation expressly authorized by
  Decision 0050, preserving the scope and original authority of Decision 0117.
- Ignore local/private workspace roots, secret environment files and disposable
  output. Existing versioned paths are still audited independently of ignore rules.
- Remove the three consumed handoff drafts; preserve their exact bytes and
  retain traceability in the originating operator's local governance evidence.
- Keep the final human/AI package evidence, all review iterations, accepted
  Change Sets, synthetic tests and deliberately archived public V2 package.
- Repair affected references, with a dated note when a frozen audit link changes.
- Date the new preparation revision 2026-10-08; retain the prior preparation
  in Git and original evidence, without backdating actual publication.
- Preserve the exact approved skill lock and package file bytes; run structure,
  contracts, package, conformance, regressions, ignore and differential checks.
- Obtain human acceptance before remote submission/integration and before
  replacing the release target. Tag/publication remain manual.

## Alternatives and risks

Deleting all review iterations or legacy packages would discard useful,
explicitly referenced evidence; they were inspected and retained. Blindly
trusting ignore rules does not inspect tracked files or Git history. Rewriting
remote history or replacing a published tag is excluded. Historical,
anonymized cases are explicitly retained under Decision 0050; no raw vault
document is transported or edited by this correction.

## Compatibility, migration and recovery

Operational packaging/privacy correction under existing rules; no changed
knowledge obligation or skill tuple. Patch-class if released independently;
included within the unpublished 3.0.0 target. Original public files
are recoverable from the exact pre-correction commit and verified local
preimages. No vault migration, global installation or ACL change.

## Status

Accepted by the operator on 2026-10-08 after review of local proposal
`9d2b1168b5d335e9cddfe24ba3132f783bfb03f2`. Remote submission, CI/main
verification and integration remain independently verifiable. Publication is manual.


## Actual acceptance and integration scope

Recorded at 2026-10-08T16:02:11Z, the operator answered:
"Pode aplicar as correções e ações, fazer uma nova PR, e preparar a release pra mim."
This directly follows the presented proposal, including conditional integration
of only `review/v3-publication-boundary-2026-10-08`. The operator authorizes the
correction, branch submission, PR and integration after CI/source verification;
the tag and GitHub Release remain manual. No history rewrite, vault write,
installation or ACL change is included. Approved skill package bytes and its
existing fingerprint-bound semantic reviews remain unchanged.
