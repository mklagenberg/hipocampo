# V3.0.0 contract — canonical vocabulary and conversational aliases

**Status:** published in V3.0.0. Existing vaults are not migrated by this
contract's publication.

## Canonical terms

The V3 contract uses one persisted vocabulary for `Record`, `Chunk`,
`Collection`, `Artifact`, `Package`, `Entity`, `Vault`, `Owner`, `Authority`,
`Curator`, `User`, and `Source`. `Source` is provenance, not a governance
role. An alias is a routing convenience, not a persisted type.

`Vault` names every Hipocampo knowledge repository. `entity`, `team`, and
`personal` are its three V3 policy profiles, not three repository kinds.
`concepts` is a possible subject, scope or historical repository name, never
a fourth profile. The V2-era `curation_level: content | vault` is a separate
field and cannot establish a V3 profile.

An Artifact-linked Record also declares its material representation as
`format: prose`. This describes the persisted Record content, not a promise
that the referenced Artifact can be fetched. Structured metadata can support
provenance and audit, but it is not a substitute for the prose body.

## Alias rules

An alias maps to one canonical term within a declared scope. It may be used
for conversational routing and search, but it must never create a competing
frontmatter type, manifest value, or contract name. Alias mappings are
versioned and validated for drift.

When an utterance has more than one plausible canonical interpretation, the
agent asks a didactic clarification question. It presents the relevant
interpretations and their practical consequences instead of choosing silently.

Examples:

| User expression | Canonical target | Persistence |
|---|---|---|
| note / nota | `Record` | only `Record` is persisted |
| source / fonte | `Source` | only `Source` is persisted |
| second brain / Hipocampo | methodology or target vault, according to context | never a new type |
| personal vault / vault pessoal | `Vault` with a personal profile | profile is resolved from manifest |

## Validation boundary

The resolver only normalizes vocabulary. It does not infer authority,
privacy, maturity, epistemic truth, or destination ownership. Those decisions
remain governed by the relevant V3 contracts and human clarification when
needed.

## Release-preparation projection

This adjacency is included by the published V3 SPEC. Existing vault adoption remains separately governed.
