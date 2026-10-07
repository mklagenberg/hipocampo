# Local personalization for V3

The portable skill contains no user-specific identity, vault router or
repository list. Its only local bootstrap value is the operator's personal
anchor pointer, stored beside the installed skill and outside any vault.

```yaml
anchor_repository: "owner/private-personal-anchor"
```

This pointer identifies where discovery starts; it does not grant access or
replace the target vault's manifest. Do not add other vault addresses,
entities, roles, scopes, credentials or authorization claims to local state.

## Session discovery

1. Read the local `anchor_repository` pointer.
2. Establish actor authorization and a non-empty allowed vault scope for the
   anchor before a governed Read.
3. Read the anchor manifest through a separately authorized metadata-read capability; verify
   entity, role, scope, V3 compatibility declaration and provenance.
4. Read discovery.registered_repositories and only registered target manifests needed for the requested operation,
   each under its own explicit authorization and scope.
5. Keep discovered addresses in session context only. Never infer authority,
   identity or registration from account access or matching repository names.

If the pointer is absent, use the Bootstrap procedure in the main skill and
the target scaffold profile. If the pointer resolves to an unavailable or
invalid source, report that exact condition. Do not replace it by guessing,
create a new anchor automatically, or treat unavailability as absence.

## Registering an invited repository

An invitation is not trusted discovery. Review the target manifest and scope
through the separately authorized metadata-read path, present them to the operator and wait for
explicit confirmation. Registration is an operational manifest/registry change in the personal anchor. Use the separately authorized structure capability with exact target, current manifest fingerprint, privacy checks, validation and review. RecordCrud persists Records, not operational manifests. If a supported metadata capability is absent, stop registration with a concrete plan; never bypass Record CRUD for knowledge or infer write permission. Add only the confirmed repository address;
never copy identity, entity, role, scope or permissions into the anchor.
