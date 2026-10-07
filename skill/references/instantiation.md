# V3 Bootstrap and instantiation

Use the canonical scaffold profile and V3 contracts from the verified version-matched immutable release for a new vault. Pin its actual commit, profile path and hashes; HEAD of main is availability context, never the scaffold provenance source. This
procedure creates a plan first; a repository name, invitation, tool or available
account does not itself authorize repository creation or governed writes.

## Bootstrap

When no personal anchor pointer exists, guide the operator through selection,
orientation, profile inputs and the generated skeleton. An invitation to
another vault does not remove the personal-anchor decision. If a configured
anchor exists but is unavailable or invalid, report that condition rather
than treating it as absent.

## Inputs and plan

Collect every profile-required value from the operator: repository address or
requested name, entity, anchor/additional role, `policy_profile`,
`curation_level`, owner, language, scope and applicable privacy constraints.
Do not infer required values or copy another vault's identity and metadata.

Present the complete plan before creating anything:

- target repository and visibility;
- entity, role and scope boundary;
- manifest and scaffold outputs with proposed values;
- source profile and template versions;
- authorization, privacy and owner/authority checks;
- tool capability for repository creation and canonical CRUD;
- validation, rollback/recovery path and remaining limitations.

Wait for explicit operator approval for the exact target and scope. If required
authority or capability is missing, stop with a plan and a blocked result.

## Creation and validation

Create a private repository only when the host exposes an authorized create
capability. Populate approved operational manifests and registries through the separately authorized structure capability; they are not Records and are not persisted by RecordCrud. Persist every knowledge Record only through canonical CRUD; never use direct filesystem or GitHub contents writes as a substitute. Use
the selected scaffold profile as the source of generated structure and
preserve its declared ownership classes.

If the target already contains files, stop and present the conflict; never
overwrite silently. After creation, validate manifest fields, compatibility,
entity/vault boundaries, links, provenance, privacy, generated outputs and
CRUD state. Provide the operator with the post-instantiation review checklist.

Successful structure checks do not prove remote authorization, content truth,
publication or ongoing compatibility. Record those limits separately.
