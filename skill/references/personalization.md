# Local anchor configuration

The portable skill has no repository router, identity table, or user-specific repository name. The only client-local fact it needs is the address of the operator's personal anchor vault, because that address is the first manifest discovery must read.

## Required field

Each host adapter stores this value in private local state, outside both the packaged skill source and every Hipocampo vault:

```yaml
anchor_repository: "owner/private-personal-anchor"
```

This field is a bootstrap pointer, not a repository registry. Do not add other vault addresses, identities, entities, or scopes to it.

## Session start

1. Read `anchor_repository` from local state.
2. Read that repository's `hipocampo.yaml` and verify that it is an anchor vault.
3. Read each address in `discovery.registered_repositories` and obtain every target's declaration from its own manifest.
4. Cache the result only for the current session.

If the local pointer is absent, run Bootstrap. If the pointer exists but the repository is unavailable or invalid, report that condition and wait for the operator; never replace it by guessing from account access.

## Registering a repository received by invitation

Read the invited repository's manifest, present its address and declared scope, and add only the address to the personal anchor's `discovery.registered_repositories` after explicit confirmation. This is a durable, gated write. It never creates sibling pointers or restores a local router.
