# Change Set 0082 — V3 processed ingress and declassification

## Problem

The repository must not become a raw inbox. Material should enter the
destination as processed, minimized and anonymized content, while REM performs
a local double check and queues remain separated by deterministic versus
semantic work.

## Proposed contract

Define processed ingress, destination-boundary minimization, redaction,
declassification with human approval, authorized external processing and
separate frontmatter, semantic and staleness queues. READ identifies findings;
CREATE/UPDATE persist them. Received material remains `new`/`pending_rem`.

## Risks and compatibility

Processing can remove useful context or create false confidence. The contract
therefore preserves provenance, approval, uncertainty and destination limits;
it does not claim to make semantic review deterministic.

## Acceptance criteria

- no raw inbox is introduced;
- deterministic frontmatter findings are separated from semantic findings;
- REM rechecks rather than silently curates;
- external processing requires an authorized environment;
- mixed-content, redaction and failed-boundary fixtures pass.

