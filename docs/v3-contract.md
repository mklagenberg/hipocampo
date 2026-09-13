# Hipocampo V3 contract — unreleased candidate

This is the implementation contract for the unreleased `v3.0.0`/LTE work. The
active released specification remains v2.1.1 until a future release gate
promotes this candidate. Existing v2 instances remain readable and are not
migrated by merely reading this document.

The L4R closure adds logical authority resolution, bilateral local ledgers,
REM-pending local receipt, privacy-bounded transparency, and deterministic
backward/forward Package auditing. These additions remain an unreleased V3
candidate and do not activate V3 for existing instances.

## Record and Chunk metadata

The V3 Record or Chunk envelope may carry these independent fields:

```yaml
record_id: "stable-id"
record_version: 1
processing_state: "new | in_review | consolidated | discarded | superseded"
maturity: "new | provisional | curated"
staleness: "current | stale | revalidation_required | historical_exempt"
epistemic:
  base: "Fact | Account | Opinion | Memory"
  qualifiers: [] # Inference, Hypothesis, Recommendation
provisional_type: "question | hypothesis | observation | reference | project-candidate | decision-candidate"
provenance:
  source_ref: "non-secret reference"
  source_kind: "url | conversation | internal | artifact"
  captured_at: "YYYY-MM-DDThh:mm:ssZ"
  observed_at: "YYYY-MM-DDThh:mm:ssZ"
  source_hash: "optional sha256"
```

The unreleased V3 governance envelope may additionally carry:

```yaml
entity: "entity-id"
scope: "knowledge-scope"
vault:
  id: "vault-id"
  profile: "entity | team | personal"
  role: "anchor | additional"
governance:
  owner: "owner-id"
  authority: "authority-id-or-chain"
  curator: "curator-id-or-delegation"
source:
  source_id: "stable-source-id"
  source_kind: "person | conversation | observation | artifact | record | vault | external-system"
```

`Owner`, `Authority`, `Curator`, and `User` are distinct operational roles.
`Source` is provenance, not a role. A profile does not grant authority,
maturity, write access, or automatic access to an entity anchor. The existing
`entity`/`role` manifest model remains separate from the candidate vault
profile.

`confidence`, `attributed_to`, and `evidence` remain optional. A source hash
identifies a version; it does not prove truth, quality, or authorization.

`observation` is compatible with `Account` until confirmation. A
`decision-candidate` is not an approved decision. Unknown provisional types
are preserved with their original identifier and are not used as factual
knowledge automatically.

## Processing and response rules

| Condition | Permitted use |
|---|---|
| `curated` + authorized + non-stale | may support an answer, preserving epistemic label and provenance |
| `new`, `in_review`, or `provisional` | discussion/review only, explicitly labelled |
| `stale` or `revalidation_required` | not current guidance; disclose the limitation |
| `discarded` or `superseded` | historical trace only, unless explicitly requested |
| unknown provisional type | preserve and isolate; do not coerce silently |

No maturity transition changes epistemic nature. No date or retrieval rank
resolves a semantic conflict automatically.

## Entity-aware routing and governed split

Every relevant CRUD operation resolves actor role, Source, entity, scope, source
vault, profile, visibility, maturity, staleness, authority, and destination
contract before operating. A Source may produce separate entity-bound Records
or Chunks, but one mutable governed Chunk cannot span incompatible entity
contracts. A split preserves Source lineage and parent context; it is not a
silent copy, general projection, or automatic synchronization.

Intra-entity sending uses the shared entity contract while still validating
restrictions and authority. Inter-entity sending requires destination
compatibility, authorization, minimization, and acceptance, and never inherits
source authority. Personal, team, and entity profiles have different default
policies, but none is an authority hierarchy.

## Three maintenance queues

The queue files are:

- `meta/fila-frontmatter.yaml` — deterministic schema, vocabulary, alias, and
  mechanically detectable frontmatter findings;
- `meta/fila-staleness.yaml` — deterministic TTL, temporality, and anchor
  validity findings;
- `meta/fila-semantica.yaml` — semantic ambiguity, conflict, duplication,
  privacy, routing, and split/merge findings.

Every finding has this minimum envelope:

```yaml
- finding_id: "stable-hash"
  target_path: "records/example.md"
  target_id: "stable-id-or-empty"
  finding_kind: "rule-name"
  rule_revision: "v3.0.0-1"
  detected_at: "YYYY-MM-DDThh:mm:ssZ"
  description: "sanitized minimal description"
  status: "open | resolved | deferred | blocked"
```

The scanner can create or update queue findings. READ itself never writes. The
frontmatter normalizer runs independently, with an hourly cadence when an
instance schedules it, and consumes only deterministic frontmatter findings
marked as supported. It revalidates each correction and records resolution.
The staleness queue can be recalculated daily; its content disposition remains
with REM or the responsible human. The semantic queue has no automatic
normalizer.

## Migration boundary

V2 frontmatter remains valid for v2 operation. A V3 consumer treats absent V3
metadata as `legacy-unmapped` and preserves the original fields. A migration
must be a separate, explicit Change Set with a mapping table, rollback, and
vault-by-vault confirmation. This contract does not migrate any instance.

See `decisions/0071-v3-record-state-and-queue-contract.md` and
`docs/v3-crosswalk-v2-v3.yaml` for the compatibility boundary, plus
`scripts/scan_v3_queues.py` for the deterministic implementation. Selective
delivery, authority succession, conciliation and Package purpose gates are
defined in `docs/v3-package-delivery-contract.md`.

## D5 candidate contracts

The following documents record the unreleased MRL-0005 candidate boundary:

- `docs/v3-vocabulary-and-aliases.md` — canonical terms and didactic
  clarification for ambiguous conversational aliases;
- `docs/v3-documentation-architecture.md` — methodology SPEC authority,
  vault-local extensions and human README boundaries;
- `docs/v3-license-and-vault-privacy-contract.md` — methodology license versus
  vault privacy contract;
- `docs/v3-language-policy.md` — English structural vocabulary and locally
  declared content language;
- `docs/v3-surface-authority-contract.md` — canonical surface precedence and
  fail-closed offline behavior;
- `docs/v3-external-reference-policy.md` — comparison/inspiration boundary for
  external references.

These documents are candidate contracts only. They do not activate V3 for
existing instances, override the released v2.1.1 `SPEC.md`, or constitute a
migration plan.

## MRL-0006 candidate contracts

The unreleased MRL-0006 candidate adds bounded operational transparency:

- `docs/v3-operational-events-contract.md` — layered events, proof limits and
  redaction;
- `docs/v3-session-cache-contract.md` — transient context and explicit capture;
- `docs/v3-crud-events-contract.md` — governed CRUD audit without content
  mirroring;
- `docs/v3-correlation-contract.md` — IDs, fingerprints and inaccessible
  frontiers;
- `docs/v3-host-capability-matrix.yaml` — proven, observational, unavailable
  and authorization-required host capabilities;
- `docs/v3-revocation-contract.md` — revocation reach and proportional
  blocking;
- `docs/v3-x6-fixtures.yaml` and `scripts/validate_v3_x6.py` — deterministic
  and adversarial candidate validation.

These are candidate-only surfaces. They do not enable durable host logging,
remote cache invalidation, migration, publication or V3 activation.

## F0 candidate contracts

The unreleased F0 candidate reviews deterministic scripts after the V3
contracts are assembled:

- `docs/v3-f0-contract.md` — classification, phase gates, layered evidence and
  typed outcomes;
- `docs/v3-f0-script-classification.yaml` — script-level classifications and
  proof boundaries;
- `docs/v3-f0-verification-matrix.yaml` — checks for execution, review,
  publication, migration and retraction;
- `docs/v3-f0-hardcode-review.yaml` — reviewed, justified and resolved
  hardcode surfaces;
- `docs/v3-f0-fixtures.yaml` and `scripts/validate_v3_f0.py` — complete,
  partial, authorization-required and blocked proof scenarios.

These surfaces remain candidate-only. They do not activate V3, migrate vaults,
transport Packages remotely or publish a release.
