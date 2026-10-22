# Codex adapter for the V3 skill

Use the portable `SKILL.md` and the target repository's V3 contracts
as sources of operational rules. Codex is a host adapter; it is not part of the
methodology/skill/vault compatibility tuple.

## Local state

Keep only the personal anchor pointer and verified installation metadata in
`hipocampo.local.yaml` client-local state, outside the packaged skill:

```yaml
anchor_repository: "owner/private-personal-anchor"
installed_skill_version: "2.2.0"
installed_package_hash: "sha256:..."
last_checked: "YYYY-MM-DDThh:mm:ssZ"
```

Do not commit this state to a vault or store a repository router, identity
table, access token, credential or permission claim in it.

## Tool boundary

Before an operation, check whether the available Codex or MCP surface can
invoke the canonical V3 read/CRUD operation with actor, reason, vault scope,
expected version and idempotency context as required. A direct filesystem,
GitHub contents or shell write is not a V3 CRUD adapter. If the canonical
operation is unavailable, block the durable operation and report the missing
capability. A repository view or UI state does not prove remote authority or
publication.

## Version and package updates

On activation, verify the selected channel and methodology/skill/vault tuple. The AI host
does not define compatibility. Reuse a successful normal source check for at
most `P7D` and a security check for at most `P1D`; when unavailable, mark it
offline and do not infer compatibility.

Stable installs verify the versioned immutable release, resolved source and
hashes. For explicit experimental use follow [runtime](runtime.md): a pinned
snapshot/RC tag needs no GitHub Release. Emit WARNING for candidate/final-review
state and let valid canonical calls execute. Retain operation-specific checks
and do not silently update, overwrite state or activate globally.

Never self-update; a package-lock.yaml verifies the exact package bytes, not authorization.
