# 0121 — General compatibility and bounded operation support

**Status:** Accepted direction from the operator on 2026-10-21; public
implementation and host proof remain separate

## Context

The V3 compatibility matrix covers the general versioned skill, methodology
and vault contract. Its `^3.0.0` range and `migration_required` result for
known V2 vaults are correct. The operator also requires governed reading of
V2.0, V2.1, V2.2 and V3 with a version warning. Treating a V2 read adapter as
general compatibility would imply capabilities that do not exist; treating
general incompatibility as a universal prohibition would prevent the
requested bounded read.

## Decision

Keep `COMPATIBILITY.yaml` as the sole general compatibility matrix. Add a
separate, versioned `OPERATION-SUPPORT.yaml` for bounded operations. A
validated V2 `read` adapter may coexist with `migration_required`; it does
not change the vault range, authorize V3 writes, create GitHub permission or
override privacy. Actual reads require independently verified source, MCP
capability, GitHub permission, methodological authorization and stable ref.
Warnings state the old contract and permitted scope without alleging a
vulnerability. Catalog specification, synthetic validation and host
observation are distinct evidence levels.

The adapter consumes a versioned V2 document under its source schema and
preserves fields and provenance. It never emits a persisted V3 Record or
mutates source. A semantic MCP path follows the same gates when Python is
unavailable. If transport exposes an entire file before classification, the
pre-retrieval privacy limit must be proven separately or the body fetch
stops. Each vault remains an independent authority.

## Rationale

A single compatibility state cannot express both the overall V3 contract
transition and the limited behavior of one adapter. Separating the contracts
preserves the published V3 range, explains the allowed V2 read precisely and
keeps tool access and privacy as independent gates.

## Discarded alternatives

Adding `compatible_for_read` to the general matrix was rejected. Mandatory
migration before any V2 read was rejected. Applying the V3 parser to V2 was
rejected.

## Impact and compatibility

This is a compatible MINOR addition to the V3 distribution, subject
to tests and release gates. V2-to-V3 Record migration remains a separate
MAJOR transition. No V2 vault changes solely because the client updates.

## Evidence and limits

User directions on 2026-10-21, management FF-DEC-0089, FF-EVL-0201,
`SPEC.md` §2-E and historical V2.0.0/V2.1.0/V2.1.1/V2.2.0 tags. Change Set
0136 carries the implementation. This decision does not claim remote-host
operation or authorize a specific vault read, installation or publication.
