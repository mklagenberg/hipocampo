# Instantiating a new vault — the skill is the mechanism

There is no longer a "Use this template" button (`hipocampo-toolkit` was consolidated and archived, decision 0032). The agent operating this skill is itself the instantiation mechanism — it follows this procedure instead of pointing the user to GitHub.

## Procedure

1. **Choose the profile.** `hipocampo/scaffold/profiles/pessoal.yaml` (`pessoal` domain, decision 0002) or `hipocampo/scaffold/profiles/empresa.yaml` (`empresa` domain). If it isn't obvious from the user's request, ask.
2. **Collect the `inputs` declared in the profile** directly from the user — repository name, `tier` (`confidencial` or `público`, decision 0029), and the owner's identity (full name + `@github-handle` in the `pessoal` domain; legal company name in the `empresa` domain). Never assume a value the profile marks as required.
3. **Present the full plan before any write** — every `output` that will be created, with the values that will go into each one (invariant 5, `SPEC.md` section 8). Only proceed after explicit confirmation.
4. **Create the repository** (private — never public, invariant 1) and generate each file declared in `outputs`, reading the source content from `hipocampo/scaffold/skeleton/` and `hipocampo/scaffold/license-templates/`, filling in the placeholders with the collected `inputs`. Respect each output's ownership class (`canonical-reference`/`generated-once`/`managed-structure`/`user-authored`, declared in the profile) — there's no need to decide again what each file is.
5. **If any output already exists at the destination** (a reused, non-empty repository), stop and report — never silently overwrite (`conflicts.default: stop-and-report`, the same behavior across all profiles).
6. **After generating everything, point the user to the `POST-INSTANTIATION.md`** generated at the root of the new repository — it now works as a verification checklist (confirming each step went correctly), no longer as a manual step-by-step from scratch.

## Example

> User: "create a new corporate vault for Gauge"
>
> Agent: profile `empresa.yaml`, tier to ask about ("confidencial or público?"). User: "confidencial". The agent collects the legal company name, presents the plan (repo name, filled-in `LICENSE-corporativo`, `AGENTS.md` with "Instance type: corporativa", `hipocampo.yaml` with `domain: empresa`/`tier: confidencial`), waits for confirmation, creates the private repository and the files, then points to the generated `POST-INSTANTIATION.md` for final review.