# Change Set 0139 — LF line-ending guidance and scaffold default

## Problem and current contract

Decision 0113 and the methodology `.gitattributes` already select LF for
recognized text. Existing vaults have divergent attribute coverage; the
scaffold does not generate attributes. Windows CRLF materialization has
previously altered local parser and package-hash observations.

## Proposed change

Publish a cross-platform line-ending guide, explain the contribution checks,
and add a `.gitattributes` output to both scaffold profiles. Recommend LF for
authored text, with binary, Windows command-script and exact-byte source
exceptions. This is operational guidance, not a new Record contract or a
retroactive requirement to rewrite compatible vaults.

Decision 0123 records the durable choice. Review of the Constitution found
FF-CON-0001:2.2 and 2.10 already sufficient. Taxonomy review found no new
structural term or controlled value; neither document requires amendment.
The skill's bundled instructions do not change, so its version remains 2.2.0.

## Acceptance and recovery

- Scaffold profiles declare the new output and its skeleton file exists.
- Guidance distinguishes Git blob bytes, worktree bytes and binary or
  byte-preserved exceptions; no blanket renormalization is performed.
- CONTRIBUTING links the procedure; the existing methodology attributes stay
  byte-identical; repository and Change Set validators pass.
- Each vault adopts through its own branch/PR and preserves its local policy.
- Revert this Change Set if rejected; no Record or historical blob rollback is
  required from this documentation/scaffold change.
