# scaffold/ — vault instantiation mechanism

This directory is the scaffold of the Hipocampo methodology: the profiles, the file skeleton, and the LICENSE templates that an agent uses to instantiate a new content repository. Consolidated here from the former `hipocampo-toolkit` repository (archived, `hipocampo/decisions/0032`) — there is no longer a separate "template" GitHub repository nor a "Use this template" button.

- **`profiles/pessoal.yaml`** / **`profiles/empresa.yaml`** — declarative contract for each instantiation: inputs to collect, outputs to generate (with ownership class — `hipocampo/docs/composition-scaffolding-and-distribution.md`), conflict behavior, upgrade behavior.
- **`skeleton/`** — source content for each output declared in the profiles (`AGENTS.md`, `CLAUDE.md`, `POST-INSTANTIATION.md`, `registry.md`, `example/example-note.md`, `hipocampo.yaml`). The agent reads these files, fills in the placeholders with the collected inputs, and writes to the new repository — it never copies verbatim without filling them in.
- **`license-templates/`** — the two `LICENSE` templates (personal/corporate) and the selection logic, migrated from the toolkit without any change to the legal content.

Full operational procedure (who executes it, in what order, what to present to the user before writing): `hipocampo/skill/references/instantiation.md`.