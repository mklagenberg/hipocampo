# Executable distribution and execution channels

This is the operational publication contract for methodology 3.1.0, preserving
the raw 3.0.0 data/CRUD baseline. Skill 2.2.0 is versioned independently.

## Channel decision

Stable is the default. Installation verifies the official immutable published
release, resolves its tag to the pinned source commit and verifies package bytes.
Experimental requires explicit selection and a pinned source commit; an RC may
be a tag without a GitHub Release. A source `release-target` declaration states
intended identity, not that a publication has occurred.

Candidate identity and incomplete final approval/documentation emit a WARNING.
They never reject engine execution, raise an exception or change a successful
operation's exit code. Structured diagnostics are separate from the domain
result; wrappers must not infer failure from stderr being non-empty.
Invalid integrity, source identity, actual compatibility or authorization still
blocks the affected operation. Experimental does not turn needs_review into accepted.

## Installation and authority

Use the executable installation procedure in [runtime usage](v3-runtime-usage.md).
The runtime is separate from the portable instructions. It binds requests to
the current OS principal and an instance-operator-managed policy. The policy
specifies entity, vault, scope, operations, active Collections and exact Record
paths; it is protected by the instance's filesystem/repository access controls.
It is a local authorization boundary, not remote IAM or a claim of Owner identity.
Requests cannot supply their own authorized-vault set to enlarge access.
Only selected, authorized paths are loaded, after header and path validation;
no repository-wide body scan is an onboarding substitute. Writes cross RecordCrud.

## Preflight and immutable publication

Use one distribution inventory covering skill, runtime and operational docs.
Do not hash the inventory/receipt into itself. Freeze and test the payload,
review that fingerprint, then record final human acceptance outside the payload.
The pre-tag validator consumes available local evidence; it never waits for
the final tag. Source integration must preserve the reviewed payload.

The final preflight requires completed AI review, independent challenge, human
approval and declared-host observations. Missing evidence stays blocked for final
handoff, while experimental operations remain available with warnings.
Only a justified additional test creates a need for an actual RC tag. Its
policy/preflight differs from final readiness; RC publication is not mandatory.

The human creates tags and final GitHub Releases. Complete every operational
document, manifest, prompt and asset before publishing the final draft. After
publication verify tag, source, hashes, channel and immutable:true. Never reuse
or move a published identity. Existing vault deployment is not a release gate.
