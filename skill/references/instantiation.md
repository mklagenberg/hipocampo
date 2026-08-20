# Instantiating a new vault — the skill is the mechanism

There is no longer a "Use this template" button (`hipocampo-toolkit` was consolidated and archived, decision 0032). The agent operating this skill is itself the instantiation mechanism — it follows this procedure instead of pointing the user to GitHub.

This procedure is what the Bootstrap mechanic's **Instantiate (skeleton)** action invokes (`SPEC.md` section 12-B, `decisions/0045-bootstrap-mechanic-and-profile-md.md`) — Bootstrap wraps it with a **Select** step beforehand (which profile/entity, fixed to personal-anchor on a user's very first vault) and an **Interview** step afterward (collecting `profile.md`'s fields, then writing the plan's confirmed content — **Instantiate (content)**). Nothing in this file's own procedure changes because of that; only its place in the larger mechanic does.

## Procedure

1. **Choose the profile.** `hipocampo/scaffold/profiles/pessoal.yaml` (`personal` domain, decision 0002) or `hipocampo/scaffold/profiles/empresa.yaml` (`company` domain — the profile *filenames* stay as literal tokens the scaffold engine references programmatically, per PR #27; only the vocabulary they generate changed). If it isn't obvious from the user's request, ask.
2. **Collect the `inputs` declared in the profile** directly from the user — repository name, `curation_level` (`content` or `vault`), the owner's identity, and the vault's content language (`language` input, defaults to `en` — confirm with the user rather than silently assuming the default). Never assume a value the profile marks as required.

> **Vocabulary:** `curation_level` is `content` or `vault` and is distinct from the `confidential`/`public` exposure tier. The profile also supplies `policy_profile` (`personal` for `pessoal`, `corporate` for `empresa`); it is written only in `hipocampo.yaml`, never duplicated in `AGENTS.md`.
3. **Present the full plan before any write** — every `output` that will be created, with the values that will go into each one (invariant 5, `SPEC.md` section 8). Only proceed after explicit confirmation.
4. **Create the repository** (private — never public, invariant 1) and generate each file declared in `outputs`, reading the source content from `hipocampo/scaffold/skeleton/` and `hipocampo/scaffold/license-templates/`, filling in the placeholders with the collected `inputs`. Respect each output's ownership class (`canonical-reference`/`generated-once`/`managed-structure`/`user-authored`, declared in the profile) — there's no need to decide again what each file is.
5. **If any output already exists at the destination** (a reused, non-empty repository), stop and report — never silently overwrite (`conflicts.default: stop-and-report`, the same behavior across all profiles).
6. **After generating everything, point the user to the `POST-INSTANTIATION.md`** generated at the root of the new repository — it now works as a verification checklist (confirming each step went correctly), no longer as a manual step-by-step from scratch.

## Example

> User: "create a new corporate vault for Acme"
>
> Agent: profile `empresa.yaml`, curation level to ask about — `content` or `vault`, distinct from exposure tier. User: "vault". The agent collects the legal company name, confirms the vault's content language rather than assuming the English default — user says "pt-BR" — then presents the plan (`LICENSE-corporativo`, `AGENTS.md` with scope only, and `hipocampo.yaml` with `entity`, `role: anchor`, `policy_profile: corporate`, `curation_level: vault`, and `language: pt-BR`), waits for confirmation, creates the private repository and the files, then points to the generated `POST-INSTANTIATION.md` for final review.
