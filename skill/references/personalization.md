# Local personalization for V3

The portable skill contains no user-specific identity, vault router or
repository list. An optional personal anchor pointer may be stored beside
the installed skill and outside any vault.

```yaml
anchor_repository: "owner/private-personal-anchor"
```

When present, this pointer identifies where discovery starts; it does not grant access or
replace the target vault's manifest. Do not add other vault addresses,
entities, roles, scopes, credentials or authorization claims to local state.

## Session discovery

1. Read the optional local `anchor_repository` pointer.
2. Establish actor authorization and a non-empty allowed vault scope for the
   anchor before a governed Read.
3. Read the anchor manifest through a separately authorized metadata-read capability; verify
   entity, role, scope, V3 compatibility declaration and provenance.
4. Read discovery.registered_repositories and only registered target manifests needed for the requested operation,
   each under its own explicit authorization and scope.
5. Keep discovered addresses in session context only. Never infer authority,
   identity or registration from account access or matching repository names.

If the pointer is absent, use an invitation, exact requested address, bounded
MCP enumeration or temporary private project hints as candidate discovery.
Revalidate the selected target on its current authenticated remote HEAD and
check access independently. This is not a complete canonical inventory and
does not require creating a personal Vault for an authorized entity read.
If the pointer resolves to an unavailable or invalid source, report that exact
condition. Do not replace it by guessing, create a new anchor automatically,
or treat unavailability as absence. Offer optional personal-Vault creation
only when personal knowledge needs a lawful persistence destination.

## Registering an invited repository

An invitation is candidate discovery, not authorization. Review the target manifest and scope
through the separately authorized metadata-read path, present them to the operator and wait for
explicit confirmation. Registration is an operational manifest/registry change in the personal anchor. Use the separately authorized structure capability with exact target, current manifest fingerprint, privacy checks, validation and review. RecordCrud persists Records, not operational manifests. If a supported metadata capability is absent, stop registration with a concrete plan; never bypass Record CRUD for knowledge or infer write permission. Add only the confirmed repository address;
never copy identity, entity, role, scope or permissions into the anchor.
