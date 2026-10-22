# V2 read-only support

Use this procedure only when the operator asks to read an identified V2
vault. It is an operation adapter, not general V2/V3 compatibility. Under
the current V3 distribution, a known V2 vault remains `migration_required`.
No V3 write, automatic migration or manifest rewrite follows from reading.

1. Select the exact remote repository, vault, entity, scope and requested
   item. Confirm the GitHub MCP's effective file/metadata read operations and
   actual repository read permission. A client installation, connected
   account, local clone or vault registration alone proves none of these.
2. Pin the remote ref/HEAD. Verify the source methodology version and commit
   from the vault's manifest plus versioned instructions or other trustworthy
   release evidence. A range is not an exact source version. Match an exact
   V2.0.0, V2.1.0, V2.1.1 or V2.2.0 entry in `OPERATION-SUPPORT.yaml`. Other
   versions are not yet a supported operation.
   Separately verify the current immutable published stable release and its
   resolved tag. An experimental candidate is not this stable reference.
3. Establish the candidate path and its classification before fetching its
   body. Repository read permission normally permits Hipocampo presentation
   up to proven `internal`; `confidential` and `restricted` require a specific
   methodological grant. Missing or conflicting labels fail closed. If the
   MCP can fetch only whole files and there is no trustworthy pre-retrieval
   classification, do not claim a privacy-safe body read or use a local cache
   to bypass that limit.
4. For an allowed path, use the GitHub MCP and recheck the ref. Interpret the
   original V2 frontmatter and body without projecting it into a V3 Record.
   Preserve source fields, Unicode, path, SHA and uncertainty. Use the
   deterministic `scripts/v2_legacy_reader.py` only in a trusted environment
   where the prior transport/authorization assertions were actually proved.
   Pass source-contract and stable-reference verification assertions only
   after observing their evidence; the parser cannot authenticate them.
   Without Python, perform the same checks semantically via MCP; if any gate
   cannot be met, stop with a typed cause.
5. Return the smallest permitted result with a visible WARNING: verified V2
   contract versus published stable version, bounded read-only scope and
   migration needed before V3 writes. Report compatibility, operation support
   and actual availability separately. Do not treat age as a vulnerability.

The full contract and failure outcomes are in
`docs/legacy-read-support.md` in the pinned methodology distribution.
Synthetic parser tests do not establish a real remote read or host support.
