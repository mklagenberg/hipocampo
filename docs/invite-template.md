# Invitation and executable installation prompt

Choose the actual host mode: Claude Code, GitHub Copilot agent mode with a
terminal, or Codex local CLI. A chat-only surface needs its own implemented
transport; do not claim a local CLI is callable there. Host observations remain
separate from distribution tests.

## Prompt to paste into the receiving AI

> Help me install and use Hipocampo from the canonical repository
> https://github.com/mklagenberg/hipocampo. Use stable by default. If I explicitly
> select experimental, use my chosen commit or RC tag and show the resolved SHA;
> do not demand a GitHub Release or future stable publication for that channel.
> Read SKILL.md and docs/v3-runtime-usage.md at that pinned source. Create an
> isolated Python environment and a new version directory, install the declared
> runtime dependencies, verify the source and full distribution inventory, and
> run scripts/v3_distribution.py. Preserve my existing install and settings.
> Load the installed skill using this host's supported local mechanism and
> confirm which mode/tools you actually have. Invoke scripts/v3_runtime.py;
> do not stop at telling me that an undefined CRUD adapter is missing.
> Show candidate warnings and continue valid canonical operations. Do not turn
> WARNING into failure or bypass integrity, authorization or CRUD controls.
> If I supplied an existing instance, read its authorized metadata and use its
> operator-provided policy; request only missing credentials/authority. Do not
> create a personal vault, edit instance metadata or widen access implicitly.
> Run the first authorized query and return its source, then verify a new
> session can use the same pinned install. If no instance is configured, run
> the synthetic reference self-test and report that limit explicitly.
> Speak in my language. Never publish private content, overwrite a prior install
> or claim an unobserved host test passed.

## Host execution

- Claude Code: use the supported local skill-loading mechanism, then invoke the
  installed Python runtime through its terminal. Confirm actual loading.
- Copilot: use agent mode with permitted terminal execution and its supported
  local skill mechanism. Plain chat without execution is not this integration.
- Codex local CLI: explicitly load the installed SKILL.md and invoke the runtime
  through available execution tools. Do not change the global skill automatically.

## Invitation details

Fill recipient, entity, repository address and permitted initial operation only
from authorized context. An invitation does not grant repository access or
create an instance policy. Have the inviter provide access through the proper
repository/organization controls. Discovery/registration and any personal-anchor
setup follow the accepted bootstrap procedure under their own authorization.
The host-local installation itself does not create a knowledge Record.
