# Update and verify a Hipocampo client on each host

The methodology source, portable skill/plugin, Python runtime, GitHub MCP,
host adapter and each vault have independent versions and permissions. An
updated client does not update a vault. Use this procedure for Claude,
GitHub Copilot in VS Code and Codex/ChatGPT. The host's current supported
installation mechanism is selected and verified at execution time; no
specific UI button or account feature is assumed here.

## Common preflight

1. Identify the actual host, harness, workspace/account and existing client
   package. Record package version, selected channel and source commit.
2. Stable selects a published immutable release with matching tag commit and
   verified package hashes. Explicit experimental selection pins a source
   snapshot/optional RC tag and full inventory, with a candidate WARNING.
3. Verify the full skill and runtime payload, lock and dependencies. Preserve
   the old installation and user-local anchor pointer. Install into a new
   versioned location through the host's supported mechanism. No silent
   self-update or global overwrite occurs.
4. Start a new host session. Observe that the expected instructions actually
   loaded, that the runtime can be called if this harness supports it, and
   which GitHub MCP operations are exposed. A package present on disk is not
   an observed host capability.
5. Diagnose a selected vault separately: compatibility, per-operation
   support, MCP tools, GitHub repository permission, methodological authority
   and privacy. A V2 vault remains `migration_required` overall even when a
   bounded read adapter is validated. A V3 vault can be compatible while a
   particular operation is unavailable in the current host.

## Host checkpoints

| Host | Installation surface to confirm | New-session observation |
|---|---|---|
| Claude | Determine whether the active surface loads a plugin, a portable skill, a local CLI bridge or a combination; use its supported update path. | State the loaded package identity, callable runtime if present, and exposed GitHub MCP read/write tools. Do not transfer a Claude Code result to Claude chat or Cowork. |
| GitHub Copilot in VS Code | Confirm the workspace/user skill or agent customization actually selected by the active Copilot harness and its MCP configuration. | Inspect the active instructions and tool list in a new agent session; check read and write operations separately. |
| Codex with ChatGPT | Treat a local Codex skill/runtime and a ChatGPT plugin or app as separate installations. Update only the surface actually used. | Confirm the selected skill/plugin identity and GitHub MCP tools in that exact session; a Codex CLI test does not prove ChatGPT plugin behavior. |

For a host without executable Python, use the semantic MCP procedure only
where it can satisfy the same source, privacy, authorization and effect
requirements. If no GitHub MCP read operation exists, remote V2/V3 reading
through this method is unavailable; local cache is not an implicit fallback.
Write support requires independent GitHub write tools, repository permission,
vault eligibility and canonical CRUD. Neither read support nor client
installation confers them.

## Recovery and acceptance

If loading, hash validation, runtime or MCP capability fails, keep the prior
installation intact, report the failed layer and its evidence, and return to
the last known working package without changing vaults. Accept a host only
after its own new-session observation. Record `prepared`, `installed`,
`loaded`, `tool-observed` and `operation-observed` separately. Updating one
host or vault never implies the others were updated.
