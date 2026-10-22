# Change Set 0136 — Bounded V2 read support

## Problem and current contract

The V3 distribution has a general `^3.0.0` vault range. Under that contract,
known V2 vaults are `migration_required`, and current V3 instructions stop
before content read. The operator requires version-aware, warning-bearing
reading of V2.0, V2.1, V2.2 and V3, while preserving the distinction between
general compatibility and adaptation for one operation. Skill/plugin and
vault updates are independent. Existing local runtime/host evidence does not
prove remote V2 reads.

## Proposed contract

`SPEC.md` §2-E remains authoritative for general compatibility and adds a
separate operation-support concept. `COMPATIBILITY.yaml` keeps its
`^3.0.0` range and existing states. `OPERATION-SUPPORT.yaml` lists exact
V2 source releases and their `read_only` adapter and evidence level. The
V2 reader preserves the source frontmatter/body and cannot mutate vaults.
Remote operation uses a verified GitHub MCP and keeps host capability,
repository permission, methodological authorization and privacy independent.

Claude, Copilot/VS Code and Codex/ChatGPT use host-specific installation and
new-session verification. Installation never upgrades a vault. `UPGRADE.md`
explains bounded reads; `MIGRATIONS.md` keeps V2-to-V3 conversion required for
V3 writes. The skill projects the semantic MCP path and deterministic parser
boundary. No real vault, host installation or GitHub ACL is changed here.

## Acceptance criteria

- V2.0.0, V2.1.0, V2.1.1 and V2.2.0 exact-source synthetic documents retain
  original fields, Unicode and line endings; the adapter reports
  `migration_required` general compatibility and a version WARNING.
- Missing source proof, MCP read, repository read, pre-retrieval class,
  specific high-class grant, stable ref or valid frontmatter denies body
  output with a typed cause. No parser path writes or creates a V3 Record.
- Taxonomy, vocabulary, SPEC, skill, upgrade/migration and catalog use
  compatibility and support consistently. Existing V3 compatibility cases
  continue to pass. Host observation remains `not_assessed` until tested.
- Change Set, package lock and repository validators pass on the exact diff.
  Human review judges whether semantic instructions match the deterministic
  subset and whether any pre-retrieval privacy issue remains open.

## Alternatives, risks and recovery

Reject widening the compatibility matrix to V2, applying the V3 parser to
V2, or requiring migration before all V2 reads. A full-file GitHub MCP fetch
can expose the body to the host before a local parser checks `visibility`.
The procedure therefore requires trusted classification before fetch; when
that cannot be proved, the read remains unavailable. A synthetic parser test
is not remote or host proof. Recovery preserves previous client installs and
leaves every vault unchanged; revert this candidate branch if rejected.

## Compatibility, SemVer and publication

This adds a bounded optional V2 read route without changing the V3.0.0
Record/CRUD baseline or `^3.0.0` general vault range: MINOR scope. It may
join the unpublished 3.1.0 candidate only after the required review and
payload/host gates; no immutable release identity is changed now. V2 client
writing under its own contract is unaffected. Publication and installation
are separate human-controlled gates.

## Evidence and status

Management FF-DEC-0089/FF-EVL-0201/FF-WRK-0080, historical V2 release tags,
Decision 0121 and `scripts/validate_v2_legacy_reader.py`. Proposed for
methodology review; synthetic checks do not certify a real-vault read.
