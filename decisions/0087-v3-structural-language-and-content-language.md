# 0087 — V3 structural language and content language

**Status:** Accepted for the unreleased V3 contract

## Context

Structural names, frontmatter and manifests must remain interoperable across
repositories, while human content may need to follow the language of the
vault's users and purpose.

## Decision

The methodology repository and vault structure use English: structural paths,
frontmatter keys and controlled values, manifests, instructions, README and
contracts. The body language of knowledge content is selected at vault
instantiation, with English as the default. Local content translations do not
create translated normative methodology surfaces, and ES-419 structural
support is not claimed in this wave.
## Rationale

English structural vocabulary protects machine interoperability; an explicit
content-language choice preserves local usability without creating translated
schema variants.

## Discarded alternatives

- Translating frontmatter keys or structural directories per vault.
- Forcing every vault's prose to English without a declared local choice.
- Treating an unsupported structural language as an automatic migration.
