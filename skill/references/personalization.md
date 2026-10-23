# Local personalization and vault discovery for V3

The portable skill contains no user-specific identity, repository router or
permission list. A personal anchor is optional. An existing host-local
`anchor_repository` pointer remains a useful discovery path, but is not a
prerequisite for joining or reading an entity vault. Store it beside the
installed skill and outside any vault.

```yaml
anchor_repository: "owner/private-personal-anchor" # optional
```

## Session discovery

1. If the anchor is configured and readable, use its
   `discovery.registered_repositories` addresses as candidates. If it is
   configured but unavailable, report that
   state rather than pretending that it does not exist.
2. An explicit invitation or repository address can start discovery directly.
   If the GitHub MCP offers repository listing, use it only to suggest
   candidates; absence from a partial list proves nothing.
3. A project may hold a private, Git-ignored temporary file of minimum
   candidate addresses and verification dates. A versioned project instruction
   may explain how to resume discovery but must not contain private addresses
   or rights by default. The file is a hint for the current session, not a
   canonical or synchronized inventory; revalidate every candidate remotely.
   If no private storage is available, keep the address in session only.
4. Confirm the authenticated account, exact remote manifest, entity, role,
   profile, compatibility and operation-specific GitHub MCP access before a
   governed read. Neither a candidate address nor a remembered permission
   constitutes authorization.

A person with verified read access may consult an entity anchor up to
`internal` without a personal vault. They remain unable to write an `entity`
vault through Hipocampo without a current scoped grant. When a personal
Record needs a destination, offer an optional personal vault. If the person
declines, do not persist the content in the entity vault, local hint, inbox or
log; explain that it was disregarded for recording. Do not claim that the
conversation itself was erased.

## Registering an invited repository

Registration in an existing personal anchor is optional, not a gate to reading
the invited vault. If requested, verify the target through the GitHub MCP,
present its scope and use the separately authorized operational metadata path
for the exact anchor change. RecordCrud persists Records, not manifests. If
that metadata capability is absent, leave registration pending while the
independently authorized read can proceed. Never store identity, roles or
permission claims in a local router.
