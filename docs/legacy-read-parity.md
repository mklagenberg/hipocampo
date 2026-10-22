# V2 read: semantic and deterministic parity review

This review applies only to the shared subset of the semantic MCP procedure
in `skill/references/legacy-read.md` and the pure parser in
`scripts/v2_legacy_reader.py`. The parser receives already-fetched bytes and
caller assertions; it cannot authenticate an MCP session, GitHub permission,
source-version evidence or pre-retrieval privacy. The semantic route must
establish those facts before supplying bytes. A matching parser result alone
does not prove an end-to-end remote read.

| Shared case | Semantic instruction | Parser/test result | Disposition |
|---|---|---|---|
| Exact V2.0.0, 2.1.0, 2.1.1 or 2.2.0 source contract | Pin and verify the historical contract; keep V2 `migration_required` overall. | Exact catalog version and commit required; four synthetic positive cases. | Aligned for the tested releases; vault source proof remains caller evidence. |
| Unknown source or mismatched contract commit | Withhold body and report an unresolved source. | `source_contract_unsupported` or `source_contract_mismatch`. | Aligned. |
| No MCP read or repository permission | Withhold body; do not use a cache as a silent bypass. | `mcp_read_unavailable` or `repository_access_unavailable` on caller assertions. | Aligned in outcome; real permission evidence remains untested. |
| Ref changes between discovery and read | Revalidate before presentation. | `ref_changed`. | Aligned for the asserted heads; remote compare-and-recheck remains caller work. |
| `internal` without nominal vault registration | Present when repository read and trusted class proof exist. | Positive fixture requires read assertions and matching pre-retrieval/header class, not a nominal member entry. | Aligned within the fixture. |
| Unknown or conflicting class | Withhold body. | `privacy_class_unknown` or `privacy_class_mismatch`. | Aligned after bytes reach parser; pre-retrieval proof cannot be supplied by the parser. |
| `confidential` or `restricted` | Require specific grant before body retrieval/presentation. | `privacy_grant_required`; restricted positive fixture requires asserted grant. | Aligned for the shared decision, with host transport limitation explicit. |
| Invalid path/header or missing required source fields | Withhold body and identify the failed boundary. | `path_invalid`, `header_invalid` or `legacy_header_incomplete`. | Aligned. |
| Successful read | Preserve original source fields/body, ref and hash; warn about older V2 and prohibit V3 write. | Original frontmatter/body, source ref/SHA, `read_only`, `mutation: none` and WARNING. | Aligned for one document, including UTF-8 and CRLF fixtures. |

## Retroactive case disposition

Existing V3 compatibility fixtures remain authoritative for the general
contract; the new reader does not alter `COMPATIBILITY.yaml`. A V2 case that
previously stopped at `migration_required` may now proceed only through the
bounded `read` route after the separate support and effective-operation gates.
Existing V3 Record CRUD and Search paths retain their own privacy and tool
gates. A compatible V3 vault with absent MCP read is still operationally
unavailable. The V3 engine suite and compatibility validator are regression
checks, not evidence that V2 Search, a real remote V2 vault, or any host was
exercised.

## Open coverage

The parser validates a selected document. A remote V2 Search discovery and
metadata index have not been implemented or observed. A GitHub Contents-style
full-file fetch may expose a protected body to the host before this parser
checks its header. The semantic procedure therefore requires trusted class
metadata before fetch and returns metadata-only/unavailable when it is absent.
Claude, Copilot/VS Code and Codex/ChatGPT each need a new-session observation.
Keep these gaps visible in the work item and do not promote the catalog's
synthetic evidence to host or remote support.
