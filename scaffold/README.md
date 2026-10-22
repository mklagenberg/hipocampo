# scaffold/ — vault instantiation mechanism


## V3.1 executable distribution and experimental channel

Use [runtime installation](../docs/v3-runtime-usage.md) and the
[channel contract](../docs/v3-distribution-and-channels.md). Stable requires the
verified immutable published release. Explicit experimental use pins a source
commit/optional RC tag and hashes; it emits WARNING and allows valid canonical
engine operations without a GitHub Release or future stable publication.
No Record-schema migration is required from compatible V3.0.x; V2 adoption
retains its separate governed migration. Preserve previous installs and user
state. Do not activate globally or change an instance without authorization.


This directory is the scaffold of the Hipocampo methodology: the profiles, the file skeleton, and the LICENSE templates that an agent uses to instantiate a new content repository. Consolidated here from the former `hipocampo-toolkit` repository (archived, `hipocampo/decisions/0032`) — there is no longer a separate "template" GitHub repository nor a "Use this template" button.

- **`profiles/pessoal.yaml`** / **`profiles/empresa.yaml`** — declarative contract for each instantiation: inputs to collect, outputs to generate (with ownership class — `hipocampo/docs/composition-scaffolding-and-distribution.md`), conflict behavior, upgrade behavior.
- **`skeleton/`** — source content for each output declared in the profiles (`.gitattributes`, `AGENTS.md`, `CLAUDE.md`, `POST-INSTANTIATION.md`, `registry.md`, `example/example-note.md`, `hipocampo.yaml`). The agent fills placeholders where present and writes the reviewed files to the new repository. The `.gitattributes` skeleton is fixed LF guidance; see [line-ending guidance](../docs/line-endings.md) for existing-vault exceptions.
- **`license-templates/`** — the two `LICENSE` templates (personal/corporate) and the selection logic, migrated from the toolkit without any change to the legal content.

Full operational procedure (who executes it, in what order, what to present to the user before writing): `hipocampo/skill/references/instantiation.md`.
## V3 source and object boundary

Profiles version 2.0.0 target ^3.0.0. For stable use the verified immutable methodology release and resolved commit; explicit experimental use pins its selected source commit/RC tag and hashes without waiting for a future release. Never use a moving HEAD as provenance. Structure generation creates authorized metadata and proposal documentation; it never directly persists a Record. Confirm initial active Collections, actor/scope and canonical CRUD before first knowledge admission. Existing content and conflicting files are never overwritten automatically.
