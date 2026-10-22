# Getting started with Hipocampo V3

Hipocampo is a methodology and a client-side skill with a separately installed
canonical runtime. Installing the public methodology does not create a vault,
register an entity, grant access or migrate content.

## 1. Select the source and execution channel

Stable is the default: verify the official published immutable release and its
exact tag-resolved commit. For an explicitly requested experiment, select a
commit or RC tag and verify its source/inventory; no GitHub Release or future
stable tag is needed. Experimental emits WARNING and allows valid operations.
Never silently use mutable main as the installed contract.

Methodology 3.1.0, skill 2.2.0 and runtime 1.0.0 have independent identities;
compatible V3.0.0 data remains supported. See [channel contract](docs/v3-distribution-and-channels.md).

## 2. Install the full distribution

Follow [executable runtime installation](docs/v3-runtime-usage.md): isolated
Python environment, pinned dependencies, verified source/inventory and a new
installation directory. The installer supplies the callable Python runtime and
isolated Claude Code/Copilot workspaces containing the exact skill bytes.
Preserve previous installs. Do not globally activate or edit existing host
configuration without the operator's explicit request.

A chat-only environment cannot call a local CLI. Use a host with execution
capability or an implemented transport; do not pretend a logical MCP adapter
is a deployed server. Actual loading/operation must be observed in each host.

## 3. Use the reference test before real knowledge

Run the installed synthetic self-test. It installs a candidate, invokes real
canonical engines, exercises new-session persistence and preserves negative
controls. A reference test is evidence about the implementation, not permission
to access a real company/personal vault. The experiment does not require creating
a personal vault or publishing an RC merely to test the public methodology.

## 4. Configure an authorized instance

Read its AGENTS.md and hipocampo.yaml through an authorized metadata capability.
Confirm entity, scope, compatibility and actual repository permissions.
The instance operator supplies the scoped runtime policy documented in the
[runtime procedure](docs/v3-runtime-usage.md#instance-authorization), binding
the authenticated OS principal and actor to allowed operations and Record paths.
Do not infer Owner identity from OS/GitHub/repository ownership. This adapter
uses local filesystem/repository ACLs; it is not a remote authorization service.

Discovery, personal-anchor setup, profile.md and any new repository creation
follow [bootstrap](skill/references/instantiation.md) and their explicit
confirmation/authority gates. They are separate from installing the methodology.

## 5. Execute and resume

Use a bounded read or Search request and the installed runtime with its pinned
fingerprint. Return result, source and structured diagnostics. A candidate
WARNING does not interrupt the engine or turn successful exit 0 into failure.
Invalid bytes, incompatible contracts or unauthorized actions remain blocked.
A missing instance policy is a concrete authorization requirement, not a missing
undefined CRUD adapter. Start a new session and repeat with the same install.

Writes require the canonical CRUD review, reason and version context, and an
explicit policy grant. Delete archives; no direct Record filesystem write is
permitted. Maintenance uses the same boundaries; no retrospective body sweep.

## Invitations and updating

Use the [copyable installation/invitation prompt](docs/invite-template.md).
Read [UPGRADE.md](UPGRADE.md) for compatible updates and [MIGRATIONS.md](MIGRATIONS.md)
for V2 adoption. Preserve [privacy and licensing boundaries](docs/privacy-and-licensing-boundaries.md).
For nontechnical Git concepts see [FUNDAMENTALS](docs/FUNDAMENTALS.md).
