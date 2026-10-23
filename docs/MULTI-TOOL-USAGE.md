# Using Hipocampo across different AI tools

Central reference — see `hipocampo/decisions/0002` for why this content lives here and new instances receive only the link, not a copy.

## The common principle

Hipocampo isn't coupled to any specific AI tool. For a remote vault, daily
operations use the **GitHub MCP** as transport inside the governed method.
Diagnose available operations and repository permission per host and target;
connector presence alone proves neither. A local cache is for separately
authorized substantial work, and a proto-vault has no remote yet. Follow the
verified Hipocampo skill and the target vault's instructions.

What changes between tools is only **how** each one connects to GitHub — not what to do once connected.

## Homologation status

The contract is platform-independent, but each host/connector combination is
supported only to the extent its observed GitHub MCP functions and target
permission allow. The examples below are orientation, not current capability
or permission evidence. Run the skill's diagnostic on first use, each new
vault/entity and after changing account, connector or package. Python is an
optional deterministic route; a host without Python may operate through the
semantic procedure only when all required structural proofs remain available.

## Specifics by tool

**Claude (Cowork, Claude Code, Claude via API/Desktop)** — connects to GitHub via Settings → Connectors (add/connect the GitHub connector, authorize through GitHub); like ChatGPT, a connected connector must still be turned on per conversation. Once connected, the Hipocampo skill can be saved persistently via Claude's native Skills feature (or `save_skill` in Cowork specifically) and applies automatically across future sessions from then on. Repository creation specifically depends on which Claude surface is in use — Cowork and Claude Code can create repositories directly; the standard Claude.ai/Desktop connector currently cannot. See `docs/getting-started-non-technical.md` for the manual fallback.

**ChatGPT** — check the GitHub connector or MCP available in the active chat.
Its exposed operations and permissions can differ by surface and change over
time. Run the operation-level diagnostic before promising repository creation,
read or write. Keep skill installation/loading separate from connector access;
neither proves the other.

**Gemini** — connects via Gemini extensions/tools with GitHub access, or via Gemini CLI/API when the GitHub MCP is available in the environment.

**GitHub Copilot** — determine whether the active host exposes the GitHub MCP
operations required for the exact remote vault action. Repository or IDE
presence by itself is not a governed read/write receipt. The skill's
instruction may be kept in a supported host instruction file, but must not
bypass the MCP and CRUD gates.

**Codex** — use the packaged adapter (`skill/agents/openai.yaml`). A private
`anchor_repository` pointer is optional; when absent, start from an explicit
invitation/address and confirm it remotely. The adapter maps GitHub MCP
operations to the governed path and treats repository declarations as
authoritative over local hints.

**Antigravity** (and other IDEs/agents with configurable MCP) — same principle as the tools above: connect the GitHub MCP, load the personalized Hipocampo skill instruction, operate normally.

**Recommended check, with any new tool:** before connecting to a repository with sensitive content, revisit the privacy checklist in `docs/FUNDAMENTALS.md` ("Privacy of AI engines in general") — model training policy varies by tool and by plan, and changes over time.

## What never changes, in any tool

The six invariants (SPEC.md, section 8), the CRUD/frontmatter-first mechanic (section 2-B), and the principle of always human-readable data (`DISCLAIMER.md`) — none of them is tool-specific. A well-configured Hipocampo instance behaves consistently regardless of which AI tool is used to operate it at any given moment.
