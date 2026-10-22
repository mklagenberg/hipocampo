# V3 Bootstrap and instantiation

Use the canonical scaffold profile and V3 contracts from the verified, version-matched source for a new vault. Stable uses the immutable published release; explicit experimental use pins its commit/RC tag and hashes, emits WARNING and requires no GitHub Release or future stable. When a tag is selected, confirm it resolves to the intended source; otherwise pin the selected commit directly. Verify profile/package hashes; HEAD of main is availability context, never the scaffold provenance source. This
procedure creates a plan first; a repository name, invitation, tool or available
account does not itself authorize repository creation or governed writes.

## Bootstrap

When no personal anchor pointer exists, an authorized invitation or exact
Vault address can still lead to a bounded entity read after target, permission
and MCP checks. A personal anchor is optional. Offer its creation when a
personal write needs an authorized destination; if declined, do not persist
personal material elsewhere. Discovery without an anchor uses only bounded
candidate addresses or temporary private project hints and revalidates each
remote target. If a configured anchor exists but is unavailable or invalid,
report that condition rather than treating it as absent.
No personal anchor is required to join an existing vault for read. An explicit
invitation or target address can start with remote diagnosis and manifest
verification. Run Bootstrap only when the operator chooses to create a vault.
If a configured anchor exists but is unavailable or invalid, report that
condition rather than treating it as absent. A direct target may still be
diagnosed independently.

## Inputs and plan

Collect every profile-required value from the operator: repository address or
requested name, explicitly selected V3 `vault_profile`, separately confirmed entity,
anchor/additional role, `policy_profile`,
`curation_level`, owner, language, scope and applicable privacy constraints.
Do not infer required values or copy another vault's identity and metadata.
Ask the profile question using `docs/v3-vault-profile-selection.md`: `team`
is suggested for a collaborative single-entity Vault, `personal` is private
personal knowledge, and `entity` has stricter entry and representative-gated
writing. Explain the practical consequences and ask the user to choose.
`team` is never accepted from silence. The scaffold profile `pessoal` or
`empresa`, older policy profile and curation level do not determine it.

Present the complete plan before creating anything:

- target repository and visibility;
- entity, role and scope boundary;
- the selected V3 Vault profile and its read/write consequences;
- manifest and scaffold outputs with proposed values;
- source profile and template versions;
- authorization, privacy and owner/authority checks;
- the authenticated creator and scoped initial Vault-representative event;
- tool capability for repository creation and canonical CRUD;
- validation, rollback/recovery path and remaining limitations.

Wait for explicit operator approval for the exact target and scope. If required
authority or capability is missing, stop with a plan and a blocked result.

## Creation and validation

Create a private repository only after explicit profile choice and exact plan
confirmation, and when the GitHub MCP exposes an authorized create capability.
If it does not, remote creation is unavailable; an
explicitly requested local proto-vault has no remote truth or GitHub receipt.
Populate approved operational manifests and registries through the separately
authorized structure capability; they are not Records and are not persisted
by RecordCrud. Record the authenticated human creator as initial
representative in `governance.authorized_representatives` for **this new
vault only**, with stable account ID, entity, actions, scope and validity;
record the grant event in `meta/representative-events.yaml`. A typed login,
GitHub admin role or the agent's own account cannot establish that human
binding or authority over an existing entity vault. Persist every knowledge
Record only through canonical CRUD; never use direct filesystem or GitHub
contents writes as a substitute. Use
the selected scaffold profile as the source of generated structure and
preserve its declared ownership classes.

If the target already contains files, stop and present the conflict; never
overwrite silently. After creation, validate the selected profile, manifest fields, compatibility,
entity/vault boundaries, links, provenance, privacy, generated outputs and
CRUD state. Provide the operator with the post-instantiation review checklist.

Successful structure checks do not prove remote authorization, content truth,
publication or ongoing compatibility. Record those limits separately.
