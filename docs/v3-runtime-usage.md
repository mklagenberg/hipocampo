# Install and run the V3 local runtime

The executable distribution composes the canonical CRUD and Search engines.
It is separate from the instructions-only skill; it is not an MCP server.
Python 3.12, Git and PyYAML 6.x are required. Use an isolated Python environment
and install `requirements-runtime.txt` there; never silently modify global tools.

## Installation

1. Confirm the canonical repository `https://github.com/mklagenberg/hipocampo`.
   Select stable by default, or explicitly choose experimental. For stable,
   verify the GitHub Release is published and immutable and resolve its tag.
   For experimental, use the approved commit or resolve the chosen RC tag.
2. Clone/check out that exact commit in a clean source directory. Preserve
   existing installations; never reset, overwrite or self-update them.
3. Create a separate virtual environment with `python -m venv <environment>`.
   Its Python installs dependencies with `-m pip install -r <source>/requirements-runtime.txt`.
4. Obtain the distribution inventory and compare its digest with the selected
   source/review artifact. The inventory tool is:
   `python <source>/scripts/v3_distribution.py --source <source> --inventory-only`.
   A digest derived from untrusted bytes alone does not establish source authenticity.
5. Install into a new version directory:

```text
python <source>/scripts/v3_distribution.py --source <source> --prefix <new-directory> --channel experimental --source-commit <exact-40-character-sha> --expected-payload <verified-64-character-digest>
```

For stable use `--channel stable`; the installer verifies the actual official
release API and tag-resolved commit. For experimental no GitHub Release is
required. Installation reports a WARNING, the callable runtime and fingerprint.
The directory is activated by `installation.json` written last. On failure,
leave the prior installation untouched and diagnose the incomplete directory.
Choose another version directory for retry; no recursive cleanup is automatic.

The skill files are in `<new-directory>/skill/`. Register that location through
the host's supported local skill mechanism (or load its SKILL.md explicitly for
an isolated test). Do not claim Claude Code, Copilot or another host actually
loaded it until that host's session confirms it. Keep the runtime source tree
and its operational docs together: copying only skill/ does not install Python.

## Instance authorization

An instance operator, under that instance's authority, supplies
`.hipocampo/runtime-policy.json`. The policy is local operational metadata,
protected by instance filesystem/repository ACLs; it is not a remote IAM service.
Show the current authenticated OS principal with:
`python <new-directory>/scripts/v3_runtime.py --principal`.
Do not derive governance ownership from that principal or repository ownership.

Example policy shape (illustrative identifiers, not an authorization):

```json
{
  "schema_version": 1,
  "principal": "the-confirmed-os-principal",
  "actor": "operator-confirmed-actor-id",
  "repository": "https://github.com/owner/private-instance",
  "entity": "confirmed-entity",
  "vault_id": "confirmed-vault",
  "scope": "confirmed-scope",
  "operations": ["read", "search"],
  "active_collections": {"collection-a": {"collection_id": "collection-a", "active": true}},
  "record_paths": {"record-a": "records/record-a.md"}
}
```

Repository/entity must match `hipocampo.yaml`; its compatibility range is checked.
Only explicitly mapped Record paths are eligible. Search requires one to 64
selected `record_ids`; the adapter checks headers before loading their bodies.
Requests cannot inject `actor`, `authorized_vault_ids`, entity or vault scope.
No policy means a precise authorization error, not a demand for an undefined
adapter. Configuring a real instance remains a separately authorized operation.

## First operation and new session

Put the request in a local JSON file:

```json
{"operation":"read","record_id":"record-a"}
```

Then invoke the installed runtime with the installation's pinned fingerprint:

```text
python <new-directory>/scripts/v3_runtime.py --instance <authorized-instance> --channel experimental --expected-payload <verified-digest> --request <request.json>
```

Search example:

```json
{"operation":"search","record_ids":["record-a"],"request_id":"query-1","query":"the question","requested_disclosure":"L2"}
```

Writes must be granted explicitly in policy and provide the canonical semantic
review, reason, idempotency and expected version fields as applicable. `delete`
archives through CRUD; it never physically removes a Record. Target identity,
path, entity and scope must stay within the policy. Every call reloads the
persisted Record, so a new process observes prior successful writes.

The result is one JSON object containing `result`, `diagnostics` and `source`.
Candidate WARNING is a diagnostic and does not change successful exit code 0.
Domain failures remain failures; wrappers must use the result/exit status rather
than treating diagnostic text as an exception. Do not copy returned private
content into public logs, release evidence or methodology commits.

## Reference self-test and preflight

`python scripts/validate_v3_preview_runtime.py --root .` performs real isolated
installation and CLI CRUD/Search against synthetic reference content. Its
metadata/tag/release fixtures are not an actual remote publication or host test.
`python scripts/v3_preflight.py --root . --channel experimental` runs product
checks with incomplete final review reported as warnings. Stable preflight
requires the external exact-payload receipt and host evidence; it never waits
for the future final tag. See [channel contract](v3-distribution-and-channels.md).


## Installable archive and isolated host workspaces

A frozen checkout can build the final asset before the final tag exists:

```text
python scripts/v3_distribution.py --source <clean-source> --archive <new-file.zip> --source-commit <selected-sha> --expected-payload <verified-digest>
```

The deterministic ZIP includes an external distribution.json envelope. After
verifying the selected artifact checksum, extract it to a new directory and
use that directory as --source; no Git checkout is needed for archive install.
Never extract untrusted/unverified archives. The expected payload digest comes
from the verified source/review artifact, not arbitrary downloaded metadata.

The installer also returns two isolated host workspace directories inside the
new install. Claude Code's workspace contains `.claude/skills/hipocampo/` and
Copilot's contains `.github/skills/hipocampo/`, with the exact skill bytes and a
local AGENTS.md carrying the runtime argument vector and pinned fingerprint.
Open the appropriate workspace in the host or use its supported additional-
directory mechanism, then confirm the skill actually loaded. No global skills
or existing project files are changed. Generated host workspaces are client-
local configuration; they contain no private router, credentials or Record.

Sources for host discovery: [Claude Code skills](https://code.claude.com/docs/en/skills)
and [GitHub Copilot agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills).
These document supported paths, not a claim that either host was run here.
The standalone engine check is `scripts/v3_runtime.py --channel experimental
--expected-payload <digest> --self-test-engines`, using the installed runtime.
