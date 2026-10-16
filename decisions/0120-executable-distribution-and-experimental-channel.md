# 0120 — Executable distribution and explicit experimental execution

**Status:** Accepted direction, implementation authorized on 2026-10-16; final package approval remains separate

## Context

The published 3.0.1 instructions require a canonical runtime without delivering
an executable installation path. Preparation markers and final-review gates
also prevent meaningful candidate evaluation. Publishing another immutable
snapshot before reconciling these surfaces would repeat the defect.

## Decision

Add an explicit experimental channel alongside the default stable channel.
Experimental execution accepts a verified pinned source snapshot or RC tag;
no GitHub Release or future stable tag is required. Candidate/final-readiness
findings produce structured warnings, not execution failures. Byte integrity,
actual contract compatibility, authorization and canonical CRUD remain enforced.
Resolve channel policy before dispatch, without per-engine version exceptions.

Provide a local CLI composition of canonical CRUD/Search and an isolated,
recoverable installation. The skill remains instructions-only. An instance
operator supplies an explicit policy binding an authenticated OS principal,
entity, vault, scope, allowed operations and bounded Record paths. A caller's
request cannot widen that policy. Local filesystem ACLs protect this policy;
this is not a remote identity service or a GitHub MCP server.

RC support is tested without requiring a public RC. An actual RC needs a
specific additional test and may be a tag only. Tags are human-created and
never moved/reused. Tag rules are not GitHub immutable-release attestation.
Stable publication still requires a complete draft and immutable GitHub Release.

Separate source identity, pre-publication readiness and publication evidence.
The final receipt binds the entire operational payload and remains outside it.
No pre-tag check waits for that same tag or embeds its own hash. Publish only
after documentation, manifests, runtime and declared-host evidence are complete.

For the explicit experimental channel only, this supersedes the stable-only
installation wording in Decision 0119 and the tag-plus-GitHub-Release routine
as applied to RCs. Final stable review, human publishing control and the raw
3.0.0 invariant contract remain in force. Update their operational projections
in the same Change Set; do not silently extend this exception to stable.

## Rationale

This permits usable candidates without weakening operation-specific controls,
and makes the final publication a confirmation of an already tested package.
Private-vault rollout is outside methodology release acceptance.

## Discarded alternatives

- Require a GitHub Release for every RC: unnecessary publication dependency.
- Ignore all validation errors in experimental mode: breaks access and integrity.
- Treat a logical test adapter as an installed transport: repeats onboarding failure.
- Put final approval inside its own payload hash: creates a cyclic dependency.

## Impact and compatibility

Change Set 0135. Methodology 3.1.0 and skill 2.1.0 are independent compatible
MINOR additions; raw 3.0.0 Record/CRUD contracts and ^3.0.0 instances remain valid.
Scaffold engine/profile versions do not change without a corresponding change.
No migration, global installation or private-vault mutation is authorized here.

## Validation

Actual CLI installation and engine dispatch in isolated fixtures, warning and
negative-control regressions, package integrity, repository and differential
Change Set checks, plus review of the exact final payload. Host observations
and human approval are recorded truthfully and never inferred from tests.
