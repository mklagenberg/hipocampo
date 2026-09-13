# Change Set 0086 — V3 methodology license and vault privacy boundary

## Intent

Implement D5.2's distinction between legal methodology licensing and
vault-local privacy governance.

## Scope

Document and validate the candidate boundary. No real vault license or
frontmatter field is changed, and no content is reclassified.

## Acceptance criteria

- methodology license and vault privacy are separated;
- license text is not treated as access permission;
- no generic content-license field is required by the candidate;
- applicable notices remain possible without becoming access grants;
- v2.1.1 behavior remains unchanged.

## Compatibility and recovery

Candidate documentation can be removed without modifying a vault or changing
the released contract.
