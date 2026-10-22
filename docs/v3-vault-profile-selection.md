# V3 Vault profile selection and absent-profile recovery

**Status:** 3.1.0 release-target contract. Source: `SPEC.md` section 2-C,
Decisions 0074 and 0124, and `docs/v3-to-v3.1-vault-upgrade.md`.

## Creation interview

Before creating a new V3 Vault, read the selected, version-matched scaffold
profile and perform the first-use capability/permission diagnosis. Ask:

> Which Vault profile should this repository use? **Team (suggested)** is a
> collaborative Vault for one entity, team or project. People with proven
> repository access are methodologically eligible to write through canonical
> CRUD, subject to technical permission, available MCP operations and privacy
> gates. **Personal** is a private Vault for one person's knowledge, opinions
> and hypotheses; it never receives another entity's material automatically.
> **Entity** is an institution-wide Vault with stricter intake and curation;
> access alone allows governed reading, while writing requires a current,
> scoped representative grant. Which do you choose?

This is a suggestion, not consent. No reply, an ambiguous answer or a value
outside `team | personal | entity` leaves creation at `needs_selection`.
After selection, ask which entity owns the Vault, its anchor/additional role,
scope, owner, intended audience, content language and privacy constraints.
The scaffold profile `pessoal | empresa` chooses the owner/license template;
`instance.policy_profile` chooses the older sensitive-data policy;
`instance.curation_level` describes curation. None supplies a V3 profile.
Review the selected profile and all consequences in the exact creation plan.
Only explicit confirmation of that plan permits a repository or manifest write.

For a new Vault, bind the authenticated creator as its initial operational
representative with a durable, scoped event. This neither makes the creator an
Authority for Record content nor a representative of any existing Vault or
entity. A repository owner/admin account is not sufficient evidence of a
representative grant in an existing Vault. The creator and declared entity
must be confirmed independently. If the connector cannot provide the needed
creation, metadata and representative-recording operations, return a blocked
plan identifying the missing capability; never claim a completed Vault.

The manifest contains the confirmed `instance.vault_profile`. The profile in
Record operation context must match the current authenticated remote manifest
and registry identity; mismatches block the profile-dependent operation.
Record writes still pass canonical CRUD. Operational manifests and grants use
their separately authorized structure path with expected-head and receipt.
No GitHub ACL or repository setting is changed by declaring a profile.

## When the field is absent

| Source state | Result |
|---|---|
| Compatible existing V3 manifest | Preserve previously governed read/write route; emit `PROFILE_UNDECLARED` WARNING. New profile-dependent eligibility is unavailable until confirmed adoption. |
| New or interrupted V3 creation | Report `INCOMPLETE_CREATION`; reconcile the partial repository against the approved plan and current remote HEAD. Never silently fill `team` or overwrite a file. |
| V2/V2.1 Vault | Use bounded legacy read support with its version-age WARNING if its separate gates pass. No V3 profile is required or inferred. |
| Explicit V3 profile outside the three values, or conflicting declarations | Block the affected V3 operation and request correction; do not replace the value with the suggested default. |

On legacy adoption, confirm the selected Vault and profile with its responsible
operator, stable Vault ID, entity and scope; inspect local extensions without
promoting them automatically to the canonical manifest. For direct-target
reads needing an ID absent from the manifest, verify the registry at the same
authenticated remote HEAD under the upgrade guide. Keep historical
`verified_against` and Record data intact. Use a reviewed, scoped metadata
change; no repository-wide backfill follows from a methodology update.

## Operation and failure gates

Keep profile choice, methodological eligibility, GitHub permission, MCP
capability, local policy, privacy clearance and actual CRUD success separate.
An authorized person may read through the proven route up to the permitted
visibility even if not locally registered; confidential/restricted still need
their own clearance. `personal`/`team` do not bypass technical or CRUD gates.
An `entity` write needs a valid scoped grant recorded by a representative.
Without a personal anchor, an authorized entity read may proceed; no personal
Record is parked in that entity Vault. Offer optional personal-Vault creation
when a personal write needs a destination. If declined, discard the attempted
personal persistence and notify the user.

The semantic procedure and `scripts/vault_profile_selection.py` must agree on
these outcomes. The script tests declaration and selection state only; it
does not prove human understanding, GitHub permission, MCP capability or a
remote write. Read-only metadata diagnosis is not Record content access.

## Retroactive use-case cross-check

| Existing case | Preserved result under this change |
|---|---|
| UC-CRUD-01/02, 19–21 | Authorized read still needs proved actor, target and scope; absence of a personal anchor or local registration is not an independent denial. Missing authorization context or wrong vault still blocks. |
| UC-CRUD-03–05, 17–18 | A Record Create/retry still uses canonical CRUD and complete review; a selected profile supplies no MCP bypass or technical permission. |
| Bootstrap capable-create/no-write-before-confirmation | Creation additionally needs explicit profile selection, entity and creator-representative event in the approved plan. |
| Bootstrap invitation-accessible-compatible | The invited entity Vault can be read without a personal anchor; address registration occurs only if an anchor exists and its separate write is confirmed. |
| Legacy bounded-read support | V2/V2.1 read remains operation support with version warning, never V3 profile adoption. |

Changes to an old case's expected result require an explicit new disposition,
not a silent fixture edit. These cross-checks are evaluated alongside the
positive and negative selection fixtures before accepting the Change Set.
