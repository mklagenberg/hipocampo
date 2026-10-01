# Change Set 0123 — V3 skill candidate package

## Problem

The gate from Change Set 0122 could evaluate the current package, but that
package is V2-compatible and cannot demonstrate V3 operating guidance. V3
remains unreleased, while the active skill and compatibility contract must
continue to describe V2.2 truthfully.

## Proposed contract

Add a complete, integrity-locked V3 skill candidate at
`candidates/skill-v3/`. Keep the released package under `skill/` and the active
`COMPATIBILITY.yaml` tuple unchanged. The candidate declares skill package
`2.0.0-rc.1`, methodology range `^3.0.0`, and unreleased status. Extend the
conformance validator to bind AI evidence to this candidate's full package
lock, evaluate six semantic scenarios, and enforce the AI review → separate AI
challenge → human decision sequence. Record the primary AI semantic review;
leave the independent challenge and human decision pending for their proper
gates.

This Change Set implements candidate guidance from existing V3 contracts. It
does not change V3 methodology contracts, install or publish the candidate,
activate V3, or read/write real vault content.

## Alternatives considered

1. Replace `skill/` now — rejected because it is the released V2 package while
   V3 is still a candidate.
2. Mark the current package as V2/V3 compatible — rejected because current
   compatibility validation and skill instructions do not substantiate that
   claim.
3. Review only a delta or overlay — rejected because the gate must identify and
   validate the complete package that would eventually be installed.

## Risks and recovery

Candidate guidance may still contain omissions, and text review does not prove
host runtime enforcement. The separate AI challenge and human review remain
blocking. The candidate lives outside the release package, so it can be
revised or removed without changing V2 behavior. A package change invalidates
the review lock and requires a new semantic assessment.

## Acceptance criteria

- the V2 released skill and active compatibility tuple remain unchanged;
- the V3 candidate package is complete, explicitly unreleased, and locked by
  SHA-256;
- the candidate covers all six semantic cases and refers to the governing V3
  contracts;
- primary AI review dispositions include rationale, evidence and uncertainty
  for all cases and bind to the exact package-lock fingerprint;
- the gate reports the candidate as compatible with the V3.0 baseline while
  keeping release blocked until independent AI challenge and human approval;
- skill documentation, repository and Change Set validators pass;
- no real vault is accessed or changed.

## Compatibility and migration

No released V2.2 behavior changes. The candidate is not an available skill
update and does not change the methodology/vault compatibility tuple. A later
promotion requires the V3 release gates and a separate release procedure.
