# V3 candidate — canonical vocabulary and conversational aliases

**Status:** unreleased V3 candidate. It does not change the active v2.1.1
contract or migrate existing vaults.

## Canonical terms

The V3 contract uses one persisted vocabulary for `Record`, `Chunk`,
`Collection`, `Artifact`, `Package`, `Entity`, `Vault`, `Owner`, `Authority`,
`Curator`, `User`, and `Source`. `Source` is provenance, not a governance
role. An alias is a routing convenience, not a persisted type.

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
