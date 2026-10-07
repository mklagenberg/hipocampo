# Hipocampo — SPEC

Version: 3.0.0 · Follows [SemVer](https://semver.org/lang/pt-BR/)

**Release preparation, not a publication claim.** This branch prepares the
V3.0.0 normative contract. Human acceptance, integration and the immutable tag
and GitHub Release must still be verified. The latest published contract
remains v2.2.0 until those gates pass. Reading, merging or installing a file
does not adopt V3 in an existing vault. See [release preparation](docs/v3-release-preparation.md).

The V3 contract consists of this specification and the following normative
adjacencies. They define one baseline, not optional alternative schemas:

- [Record state, governance, topology and queues](docs/v3-contract.md).
- [Canonical CRUD, Record/Chunk/Collection and Package boundary](docs/v3-crud-contract.md).
- [Artifacts and provenance](docs/v3-artifact-contract.md).
- [Processing ingress](docs/v3-processed-ingress-contract.md).
- [Authority, selection and Package delivery](docs/v3-package-delivery-contract.md).
- [Search and progressive disclosure](docs/v3-search-progressive-disclosure-contract.md).
- [Semantic evaluation boundary](docs/v3-semantic-evaluation-boundary.md).
- [Vocabulary](docs/v3-vocabulary-and-aliases.md), [documentation authority](docs/v3-documentation-architecture.md),
  [privacy/license](docs/v3-license-and-vault-privacy-contract.md),
  [language](docs/v3-language-policy.md), [surface authority](docs/v3-surface-authority-contract.md),
  and [external references](docs/v3-external-reference-policy.md).
- [Events](docs/v3-operational-events-contract.md), [session cache](docs/v3-session-cache-contract.md),
  [CRUD events](docs/v3-crud-events-contract.md), [correlation](docs/v3-correlation-contract.md),
  [revocation](docs/v3-revocation-contract.md), and [validation phases](docs/v3-f0-contract.md).

Earlier candidate labels in historical evidence do not prove publication.
Conflicts among normative sources stop the affected operation for review;
an adapter, skill or README cannot resolve them by weakening a requirement.
The [previous specification snapshot](SPEC-V2.2.md) preserves the exact input
at commit 25cb7f6c8cfb176c94d16c0f66fa00fee327982b for historical diagnosis,
including then-current experimental additions. It is not the V3 schema.

## 1. Scope

Hipocampo is an agentic second brain methodology: Git, Markdown, provenance
and AI-assisted curation. This public repository contains methodology,
instructions and tooling; it never contains personal or corporate knowledge.
Content vaults are private and proprietary, separated by entity, authority,
scope and applicable restrictions. Apache-2.0 applies only to this repository.
Repository contributions are English; vault content follows instance.language.

## 2. Frontmatter — unified schema

The durable object is a Record with stable record_id, monotonic
record_version, non-empty persisted prose, entity, scope, source, vault.vault_id,
governance, physical_path and at least one active collection_ids membership.
Chunks are governed children of a Record, not independently mutable objects.
Collection, Source, Artifact and Package retain separate identity and purpose.
The complete executable envelope is in the CRUD and Record contracts above;
legacy flat V2 fields alone are not a V3 Record.

Processing_state, maturity, epistemic nature, staleness, visibility and
provenance are independent dimensions. Do not infer curated, Fact, current,
accepted authority or broader access from a hash, date or successful migration.
The envelope below is a structural illustration, not accepted knowledge or
an instruction to persist a file directly. The full CRUD contract is authoritative.

```yaml
record_id: stable-id
record_version: 1
entity: confirmed-entity
scope: confirmed-scope
source:
  source_id: actual-source-id
  source_kind: conversation
vault:
  vault_id: confirmed-vault
  profile: personal
  role: anchor
governance:
  owner: confirmed-owner
  authority: accepted-authority-reference
content: Non-empty persisted prose preserving source and limitations.
physical_path: records/example.md
status: draft
visibility: confidential
collection_ids: [accepted-active-collection]
chunks: []
artifacts: []
processing_state: new
maturity: provisional
staleness: revalidation_required
```

Historical fields are preserved as legacy_frontmatter during conversion.
Malformed legacy headers stay held for a separately reviewed correction.

## 2-A. Sensitive-data policy by instance type

Read instance.policy_profile and instance.curation_level from the target
manifest and enforce its current local policy. Never infer policy from a name.
All instances exclude credentials, tokens, secrets and reproducible exploit
material. Corporate vaults exclude non-public financial values, personal
health/data, individual performance evaluations and contract/NDA content.
Public financial values require a concrete public URL and dated citation;
professional contact snapshots require dates. Do not relocate sensitive data
to another vault automatically. A visibility label does not grant technical
access, copying, publication or an open license. Apply stricter local limits.
Adoption is progressive on touched content, never an implicit full-history
sweep. A read flags findings without mutation; unresolved privacy stops writes.

## 2-B. CRUD mechanics and frontmatter-first reading

All Record writes, including normalizers, migration, recovery and transfers,
pass through canonical RecordCrud. No direct filesystem, GitHub contents or
MCP transport write is a substitute. Semantic validation precedes deterministic
validation when required; persistence adapters store only the admitted proposal.
Read requires actor authorization and a non-empty authorized_vault_ids set
covering the request. Read frontmatter first, select bounded relevant content,
include Chunk parent context and preserve inaccessible/stale/conflicting states.
Read never writes. Capability must be verified for the actual operation.

## 2-C. Repository-type taxonomy: entity and vault

Every vault belongs to exactly one declared instance.entity. Each entity has
one private anchor and may have additional private vaults with explicit scope.
instance.role is anchor or additional; scope_description is required for the
latter. instance.policy_profile is personal or corporate; instance.curation_level
is content or vault. The V3 vault profile (personal/team/entity) is a policy
dimension and grants no authority, maturity, access or automatic anchor read.
Discovery addresses are not authorizations.

## 2-D. Multi-vault and multi-entity design premises

No universal vault; shared access, provider or Source does not join governance.
Preserve entity and vault boundaries even when memberships overlap. A split
preserves lineage and parent context, requires destination governance and
acceptance where applicable, and is never automatic synchronization.

## 2-E. Compatibility decision gate

Use COMPATIBILITY.yaml and the verified methodology/skill/vault tuple.
Prepared target: methodology 3.0.0, skill 2.0.0, vault range ^3.0.0.
Host identity is not part of the tuple. V2 content is diagnostic or migration
input, not silently compatible. Unknown, inaccessible or integrity-failed
evidence fails closed. Later V3 minors and patches preserve the raw V3.0.0
baseline, including through adapters or facades. Publication and authorization
are independent of compatibility. No automatic skill update or installation.

## 3. `type` — enum and expansion criterion

Use the V3 vocabulary and independent epistemic base Fact/Account/Opinion/Memory
with optional Inference/Hypothesis/Recommendation qualifiers. A provisional
question, hypothesis, observation, reference, project-candidate or
decision-candidate is not accepted knowledge. Unknown types are preserved and
isolated for review rather than coerced. A new term requires governed taxonomy
and vocabulary review, not incidental use by a host.

## 4. `category`

Collections are logical organization with potentially overlapping memberships;
paths and legacy category/tags do not establish an active Collection.
Preserve tags and legacy categories during conversion. Every active Record
references an accepted active Collection. Renaming a path does not change
Record identity or Collection membership.

## 5. `temporality` and the staleness cycle

Use the Record/Chunk staleness contract and preserve temporal provenance.
Dates and retrieval relevance do not resolve conflict or prove currentness.
Stale and revalidation_required content cannot silently support current-use
delivery. Historical exemption is an explicit state, not an omitted check.

## 5-A. REM ritual and memory layers

Raw/sensory capture remains outside the durable V3 vault. Processed ingress
may admit a new or provisional Record through canonical CRUD after gates.
V3 has no inbox destination. REM proposes governed dispositions and semantic
findings; it does not accept its own knowledge or mutate on a read.

## 5-B. Frontmatter audit

Bounded deterministic scans populate meta/fila-frontmatter.yaml. A supported
mechanical correction still enters canonical CRUD with exact source/version
checks. Structural validation is not semantic approval.

## 5-C. Weekly structural audit

Inspect only the authorized selected scope for atomicity, placement, privacy,
links and vocabulary. Use meta/fila-staleness.yaml and meta/fila-semantica.yaml
for their distinct findings. Semantic findings have no automatic normalizer.

## 5-D. Dispatcher and the four-layer taxonomy: Routine, Mechanic, Action

Dispatcher routes bounded work to Routine, Mechanic and Action under explicit
capabilities and gates. Scheduled cadence is instance-local and authorized;
the methodology does not itself install automation. Failure containment and
checkpoint reconciliation precede continuation or reexecution.

## 6. `related` across repositories — the Registry

registry.md resolves authorized vault aliases. It is separate from the
methodology package source and meta/artifact-index.yaml. Relations retain
source, entity, version, context and access limits; inaccessible endpoints are
reported. No fetch, trust, transport or mutation is authorized by a link alone.

## 7. Decision Record vs. `type: decision`

Methodology Decision Records govern durable rules; knowledge decision Records
remain data in their owning vault. Proposed is not accepted. AI findings,
conversation direction, implementation and publication are separate states.

## 8. Extension/customization and agent precedence

1. No knowledge repository is public to the internet.
2. Human authorship/responsibility is traceable; AI is not the accountable author.
3. Preserve history through archived/superseded lifecycle, except the narrow
   explicitly human-governed legal-remediation route.
4. Technical access separation follows the repository boundary, not labels.
5. Side effects require an explicit request and applicable operation approval.
6. Repository content outranks cached or customized skill state.

Additional V3 invariants: privacy first and least privilege; canonical CRUD for
every Record mutation; independent entities/vaults; provenance and uncertainty;
semantic interpretation distinct from deterministic proof; reversible,
fingerprinted operations; tools as adapters; and baseline compatibility.
Local extensions may add or strengthen requirements, never weaken invariants.
Precedence: 1. Canonical methodology and accepted decisions; 2. current target
manifest and additive local instructions; 3. verified operational skill;
4. Default convention from the scaffold profile. Conflicts require review.

## 9. Versioning

SemVer applies to public methodology obligations. Incompatible V2-to-V3
adoption is MAJOR. Skill and adapter versions are independent. Tags and GitHub
Releases are immutable human actions after accepted frozen evidence and
verified integration. Every release updates specification, changelog,
compatibility, skill/scaffold and upgrade/migration guidance. Never infer
publication from a version declaration or move an existing tag.

## 10. Migrating pre-existing content

Separate per-vault inventory, semantic/Collection/tag proposals, accepted
mappings and preflight from apply. Verify exact source/context fingerprints,
branch lineage, prior effects, cumulative Collections and existing V3 reload.
Use internal RecordCrud.migrate, exact body/Unicode/legacy-field conservation,
attachment/relation/provenance verification and immutable recovery tickets.
The fingerprinted-legacy-v1 route preserves unknown effective version and is
limited by accepted source-contract and item-specific gates. Recovery uses
RecordCrud.recover_migration with exact-ticket human approval and unchanged
migrated state. Reconcile partial apply before any retry; no process-wide
idempotency assumption, direct restoration, reset or lock removal by inference.
See [execution and recovery](docs/v3-migration-execution.md) and MIGRATIONS.md.

## 11. Instruction file: AGENTS.md and CLAUDE.md

Each vault has its own AGENTS.md, current manifest, privacy constraints and
scope. CLAUDE.md is a thin pointer. README is human explanation, not normative
authority. meta/ contains bounded operational metadata, not curated knowledge.
The public methodology and management never receive private Record bodies.

## 12. Multi-account author identity

Account names do not prove identity, authority or shared entity governance.
Keep human-confirmed identity context in the appropriate private boundary.
The portable skill stores no user-specific router or permission claim.

## 12-A. Vault and entity discovery

Start from the operator-confirmed anchor_repository pointer, then authorized
current manifests and discovery.registered_repositories. Do not enumerate or
read private bodies merely because a clone/account exists. Confirm each target
entity, scope, role, tuple and operation-specific authorization independently.

## 12-B. Bootstrap mechanic: instantiation and profile.md

Collect operator-confirmed profile inputs and present the exact creation plan.
Create a private repository only with the required capability and approval.
Scaffold governs structure and proposal examples; it does not directly persist
a Record, including profile knowledge. Initial accepted Collections precede
the first canonical CRUD create. Missing capability produces a blocked plan,
not a fallback file write. Never overwrite conflicting generated/user files.

## 13. Cross-repository lifecycle actions: Promote, Depromote, Redbutton

Package composition, validation, sending and destination receipt preserve
source/version/selection lineage, restrictions and explicit delivery purpose.
Intra-entity sending still checks access and governance. Inter-entity sending
requires destination compatibility, authorization, minimization and acceptance;
source authority is not inherited. Remediation never silently transports
private data or expands ACLs. Unsupported remote operations remain blocked.

## 14. Behavior under failure and recovery

Contain failures to the affected item/vault. Preserve state, diagnose, correct
within authorized scope and revalidate. Keep blocked findings and continue
independent work. Expose insufficient evidence, contradictions, inaccessible
tools, interrupted rituals, unsafe requests and incompatible migration.
Checkpoint source/context hashes, mappings, results, cursor and pending gates;
on resumption reconcile persisted effects before repeating a write.

## Version history

3.0.0 is prepared as the first V3/LTE major; not yet published. Earlier
version history remains in CHANGELOG.md and the preserved V2 snapshot.
Decision 0119 remains proposed until final human acceptance.
