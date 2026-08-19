# Step classification

`SPEC.md` section 5-D already names a step-behavior scheme, in passing, as "orthogonal to" the Dispatcher/Routine/Mechanic/Action taxonomy: **deterministic**, **discretionary**, **gated**. Section 14 uses the same distinction implicitly, describing how an agent behaves under six failure modes. Neither section enumerates every step the methodology actually defines against this scheme in one place — each addition classified only itself, at the point it was introduced. This document is that single place. See `decisions/0048-step-classification-scheme.md` for why this exists as its own reference rather than folded into `SPEC.md` directly.

**Not a mapping onto MODA's own agency vocabulary.** MODA's `distribution_of_agency` control (`conformance/moda.yaml`) uses a five-value scheme — deterministic / agent-reasoned / tool-executed / human-decided / hybrid. This document formalizes Hipocampo's own three-value scheme instead, the one `SPEC.md` already uses. The two vocabularies are related but not identical, and no translation table between them is attempted here — see the note in `conformance/moda.yaml`'s `distribution_of_agency` control for what this document does and doesn't close.

## The three categories

- **Deterministic.** A fixed procedure — a script, or a mechanical lookup — with no agent judgment involved in *whether* or *how* it runs. Example: the frontmatter audit (`SPEC.md` §5-B) is a script, not an AI agent's judgment; it scans and reports, nothing more.
- **Discretionary.** The agent applies judgment or reasoning, but the step itself doesn't durably change repository state — either because it only reads/decides/flags, or because any resulting write is a separate, later, gated step. Example: reading and caching a vault's manifest during discovery (`SPEC.md` §12-A) is agent-executed but produces no durable write — the cache is ephemeral sensory memory, never committed.
- **Gated.** The step durably changes repository state and therefore requires the explicit-confirmation gate Invariant 5 (`SPEC.md` §8) already establishes: the agent presents the plan, and only proceeds on explicit request. Every durable write in this methodology is gated — "gated" names *which* steps carry that requirement, it doesn't add a new one.

These three aren't a strict pipeline (discretionary always before gated, deterministic always standalone) — a single mechanic action can itself be discretionary-then-gated in sequence (see Bootstrap's Interview action below), and this document classifies at that granularity rather than only at the mechanic/routine level.

## Routines (`SPEC.md`, section 5-D)

| Routine | Step | Category | Note |
|---|---|---|---|
| Frontmatter audit (§5-B) | Scan and produce `meta/fila-de-manutencao.md` | Deterministic | Script, never AI judgment. |
| REM ritual (§5-A) | Consolidate — decide disposition of an `inbox/` item | Discretionary | Judgment on classification/destination. |
| REM ritual (§5-A) | Consolidate — commit the resulting document | Gated | Invariant 5, same as any write. |
| REM ritual (§5-A) | Update old memories — decide disposition of a flagged item | Discretionary | Revalidate/archive/supersede/fix-field is a judgment call. |
| REM ritual (§5-A) | Update old memories — commit the disposition | Gated | Invariant 5. |
| Weekly structural audit (§5-C) | Review atomicity/placement/sensitive-data-leak, produce findings | Discretionary | Judgment call on each of the three functions. |
| Weekly structural audit (§5-C) | Act on a finding (move/split/remove/Redbutton) | Gated | "Any finding is always presented to the responsible human before any action" (§5-C). |
| Dispatcher (§5-D) | Trigger a routine on schedule | Deterministic | Fixed order today; dynamic scheduling from per-routine metadata is an open question, not yet built (`decisions/0042`). |

## Mechanics and their actions

| Mechanic | Action | Category | Note |
|---|---|---|---|
| CRUD (§2-B) | Read | Discretionary | Frontmatter-first triage is judgment; the light read-time validation (§2-B) is deterministic-lookup within an otherwise discretionary step. |
| CRUD (§2-B) | Create / Update / Delete | Gated | Invariant 5; Delete additionally requires the narrow §8 exception (`decisions/0010`/`0028`) even when gated. |
| Publication — Promote (§13) | Deciding elegant vs. literal path, drafting the destination document | Discretionary | Both variants always presented together before any write. |
| Publication — Promote (§13) | Committing either path | Gated | Invariant 5; literal path additionally requires the explicit ownership-transfer warning before proceeding. |
| Publication — Depromote (§13) | Deciding the move | Discretionary | — |
| Publication — Depromote (§13) | Committing the move | Gated | Invariant 5. |
| Sequenced-removal — Redbutton (§13) | Identifying a policy violation | Discretionary | Structural audit or operator-identified, per the broadened trigger (`decisions/0028`). |
| Sequenced-removal — Redbutton (§13) | Executing the tombstone | Gated | "The decision is always explicitly human, never automatic" (§13) — the strictest gate in the methodology, on top of Invariant 5. |
| Bootstrap — Select (§12-B) | Choosing which repository, for which entity | Discretionary | Fixed choice on a user's first vault; ordinary judgment afterward. |
| Bootstrap — Orient (§12-B) | Conversational walkthrough | Discretionary | Conditional trigger judgment (only first vault, only if the user seems unfamiliar); no durable write. |
| Bootstrap — Instantiate, skeleton (§12-B) | Running the scaffold, creating the repository and `hipocampo.yaml` | Gated | Invariant 5 — a durable write, same as any instantiation. |
| Bootstrap — Interview (§12-B) | Conversational capture of `profile.md` fields | Discretionary | Capture method, not a write. |
| Bootstrap — Interview (§12-B) | Committing `profile.md` | Gated | "The result always passes through the same explicit-confirmation gate" (§12-B). |
| Vault and entity discovery (§12-A) | Reading and caching the anchor manifest | Discretionary, ungated | Ephemeral sensory-memory cache — never a durable write, so no gate applies; matches the classification already validated against this real case in the taxonomy revision's planning discussion. |
| Vault and entity discovery (§12-A) | Registering a newly-discovered or newly-granted vault | Gated | "Per invariant 5, like any other durable write" (§12-A). |

## Failure and recovery behavior (`SPEC.md`, section 14)

Every one of the six modes section 14 defines follows the same two-step shape: a discretionary detection/judgment step, followed — only if a corrective action is actually taken — by a gated write.

| Mode | Detection step | Category | Corrective write, if any | Category |
|---|---|---|---|---|
| Insufficient evidence | Recognizing the claim isn't supported at the implied confidence | Discretionary | Proposing/executing a check | Discretionary (a search or read is not itself a durable write) |
| Frontmatter↔body contradiction | Recognizing the disagreement | Discretionary | Editing either side to resolve it | Gated — "never edits either side... without an explicit instruction" |
| Unavailable tool | Recognizing the tool is down/restricted | Discretionary | Any fallback mechanism used instead | Gated — "without flagging that it's a fallback" implies explicit surfacing before proceeding |
| Interruption mid-ritual | Re-deriving ritual state from the repository on resume | Discretionary | Resuming the write | Gated — Invariant 5 "applies again at resumption" |
| Unsafe request | Recognizing the invariant/policy conflict | Discretionary | Offering a compliant alternative | Gated, if the alternative itself is a write |
| Incompatible migration | Recognizing the version gap | Discretionary | Applying the migration | Gated — "as an explicit, separate, confirmed step" |

## Known limitation

This table's coverage is the methodology's currently-named routines, mechanics, and actions as of Lote E1 (v2.0.0-unreleased) — it is not re-derived automatically from `SPEC.md` and there is no mechanism keeping the two in sync. A future addition to the methodology needs its own row added here explicitly, the same way `decisions/0044`/`0045` classified vault discovery and Bootstrap at the point they were introduced, rather than this document being regenerated. Flagged as a real, acknowledged gap, not silently assumed to stay current on its own.
