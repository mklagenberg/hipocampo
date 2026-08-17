# LICENSE templates — how the agent uses this

When the agent instantiates a new content repository (see `hipocampo/skill/references/instantiation.md`), it generates the root `LICENSE` from one of these templates — it never copies the methodology's Apache-2.0 (`hipocampo/LICENSE`), which is correct for `hipocampo` but wrong for a content repository, even a private one, because the license text itself would already assert a usage permission that isn't the intent (see `hipocampo/decisions/0007-content-repo-licensing.md`).

## How the agent chooses

1. By the content owner, declared as an input in the scaffold profile:
   - **`LICENSE-pessoal.md`** — if the owner is a natural person.
   - **`LICENSE-corporativo.md`** — if the owner is a company.
2. It fills in the placeholders (`[FULL NAME]`/`[@github-username]` or `[COMPANY NAME]`) from the inputs collected from the user.
3. If the repository is at the "vault" level (only receives `visibility: confidential`/`restricted`, never `public`/`internal` — see `hipocampo/SPEC.md`, section 2), it keeps only sections (c) and (d) of the template, following the adjustment note within the template itself.
4. It saves the result as `LICENSE` at the root of the new repository.

Confirm the result in step 2 of `POST-INSTANTIATION.md` — this is neither optional nor cosmetic: without it, a private content repository would technically carry an open-source license.