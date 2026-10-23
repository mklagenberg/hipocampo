# Codex adapter for the V3 skill

Use the portable `SKILL.md` and the target repository's V3 contracts
as sources of operational rules. Codex is a host adapter; it is not part of the
methodology/skill/vault compatibility tuple.

## Local state

Keep an optional personal anchor pointer and verified installation metadata in
`hipocampo.local.yaml` client-local state, outside the packaged skill:

```yaml
anchor_repository: "owner/private-personal-anchor" # omit when none exists
installed_skill_version: "2.4.0"
installed_package_hash: "sha256:..."
last_checked: "YYYY-MM-DDThh:mm:ssZ"
```

Do not commit this state to a vault or store a repository router, identity
table, access token, credential or permission claim in it. Without an anchor,
start from an explicit address or invitation and revalidate the candidate via
GitHub MCP. Project-local private hints are optional and never canonical.
Do not require a personal Vault for an authorized entity read or infer a
complete Vault inventory from local hints.

## Tool boundary

Before an operation, diagnose the available GitHub MCP functions, authenticated
account, target permission and methodological eligibility separately. For a
remote vault, use GitHub MCP transport inside canonical V3 read/CRUD, with
actor, reason, vault scope, expected version, idempotency and confirmed
readback as required. With Python, the compatible engine can enforce
deterministic checks. Without Python, follow the same CRUD sequence with
reproducible MCP evidence; a raw GitHub contents or shell write outside that
gateway is not governed CRUD. Missing capability blocks the dependent action,
not independent read or orientation. A repository view or UI state does not
prove remote write authority or publication.

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
