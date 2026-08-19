# Using Hipocampo across different AI tools

Central reference — see `hipocampo/decisions/0002` for why this content lives here and new instances receive only the link, not a copy.

## The common principle

Hipocampo isn't coupled to any specific AI tool. What any tool needs, to operate an instance, is read/write access to the repository via the **GitHub MCP** (or an equivalent git integration mechanism). Once that connection exists, the same principles apply across any tool: read the frontmatter first (SPEC.md section 2-B), respect the invariants (section 8), never write without an explicit request, and follow the personalized Hipocampo skill (`hipocampo/skill/SKILL.md`) as the source of operational instruction.

What changes between tools is only **how** each one connects to GitHub — not what to do once connected.

## Specifics by tool

**Claude (Cowork, Claude Code, Claude via API/Desktop)** — connects to GitHub via Settings → Connectors (add/connect the GitHub connector, authorize through GitHub); like ChatGPT, a connected connector must still be turned on per conversation. Once connected, the Hipocampo skill can be saved persistently via Claude's native Skills feature (or `save_skill` in Cowork specifically) and applies automatically across future sessions from then on.

**ChatGPT** — connects to GitHub via Settings → Connectors (Connect, then authorize through GitHub); the connector must still be turned on per chat from the connectors dropdown near the message box. Since ChatGPT has no native "skill" concept and Custom Instructions has a character limit too small for the full skill content, the practical approach is a short Custom Instruction pointing at the live `skill/SKILL.md`/`AGENTS.md` URLs rather than an embedded copy — see `docs/getting-started-non-technical.md` for the exact wording. A dedicated "GPT" is a workable alternative but scopes the setup to that one GPT rather than every chat.

**Gemini** — connects via Gemini extensions/tools with GitHub access, or via Gemini CLI/API when the GitHub MCP is available in the environment.

**GitHub Copilot** — already runs inside GitHub/the IDE itself, with native access to the repository it's operating on — it doesn't need an external MCP to reach the host it already lives on. The skill's instruction can be kept as a Copilot custom instruction file (e.g., `.github/copilot-instructions.md`) in addition to the `CLAUDE.md` already used by other tools.

**Antigravity** (and other IDEs/agents with configurable MCP) — same principle as the tools above: connect the GitHub MCP, load the personalized Hipocampo skill instruction, operate normally.

**Recommended check, with any new tool:** before connecting to a repository with sensitive content, revisit the privacy checklist in `docs/FUNDAMENTALS.md` ("Privacy of AI engines in general") — model training policy varies by tool and by plan, and changes over time.

## What never changes, in any tool

The six invariants (SPEC.md, section 8), the CRUD/frontmatter-first mechanic (section 2-B), and the principle of always human-readable data (`DISCLAIMER.md`) — none of them is tool-specific. A well-configured Hipocampo instance behaves consistently regardless of which AI tool is used to operate it at any given moment.
