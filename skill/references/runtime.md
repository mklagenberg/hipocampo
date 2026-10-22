# Runtime and channel procedure

The portable skill is instructions-only. Install the separate canonical CLI
runtime with its operational documentation and Python dependency. The package
target is methodology 3.1.0 / skill 2.2.0; preserve baseline 3.0.0.

Resolve the official source commit before executing its installation helper.
Stable requires the published immutable release and exact tag-resolved source.
Explicit experimental use accepts a pinned commit or RC tag with verified
inventory/hashes, emits WARNING and does not require a GitHub Release or future
stable publication. Never reject a valid engine operation just because it is RC.

Use `scripts/v3_distribution.py` for inventory and isolated installation, then
`scripts/v3_runtime.py` for canonical CRUD/Search. Full procedure and executable
examples are in `docs/v3-runtime-usage.md` in the same installed distribution or
at the selected source_repository/commit. Do not resolve these instructions
against mutable main or demand a future tag for experimental use.

An instance operator provides its local runtime policy, binding authenticated
OS principal, actor, entity, scope, allowed operations, active Collections and
exact Record paths. This local policy relies on filesystem/repository ACLs;
it is not remote IAM or evidence of Owner identity. No policy means diagnose
that missing authorization. It does not mean the adapter is unavailable.

Search uses explicit bounded Record identities. Requests cannot widen policy.
Create/update/archive use canonical CRUD with required reviews/version context.
Report the structured diagnostics without turning WARNING into a fatal error.
Final-only pending approval/documentation is a warning in experimental use;
invalid bytes, incompatible contract or unauthorized action stays blocked.

Preserve previous installs and user state. Register or load this skill through
the chosen host's supported mechanism, explicitly confirming actual loading.
Host-specific verification remains not-assessed until the real host is observed.
