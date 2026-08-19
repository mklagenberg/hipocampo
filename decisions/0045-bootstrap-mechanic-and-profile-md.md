# 0045 — Bootstrap mechanic: Select, Orient, Instantiate, Interview, and profile.md

**Status:** Accepted

## Context

First-time instantiation already happens in practice — `skill/references/instantiation.md` already describes choosing a scaffold profile, collecting inputs, and generating outputs — but nothing in `SPEC.md` names this as a distinct, classified piece of behavior under the Dispatcher/Routine/Mechanic/Action taxonomy (`decisions/0042`, `decisions/0043`). `decisions/0043`'s own rationale anticipated this: "a forthcoming Bootstrap capability... would otherwise need to invent its own category from scratch" — this Decision Record is that capability, fit into the taxonomy `decisions/0043` established rather than retrofitted after the fact.

Two things First-time instantiation does not yet have: a recognized trigger condition (today, an agent either infers "this looks like a new user" informally, or waits to be told outright), and a place to record the identity/contact facts a returning user shouldn't have to repeat every time (today, nothing distinguishes a document written *by* a person from a durable record *about* that person's own identity — the closest thing, `AGENTS.md`'s free-text scope block, was never meant to hold structured, machine-read personal facts).

`decisions/0044` also leaves one item genuinely open: a single, irreducibly local pointer to which repository is the user's own anchor vault — needed before any manifest-based discovery can start at all. Bootstrap is the mechanic that exists to create that anchor vault in the first place, so this Decision Record inherits, rather than resolves, that open item.

## Decision

**Classification.** Bootstrap is a **mechanic** (`SPEC.md` section 5-D), not a routine — it fires on an event, not a schedule, and does not enter the Dispatcher's process registry alongside REM, frontmatter audit, or the weekly structural audit.

**Trigger.** "Discovery attempted, nothing found" — the agent tries to read the user's own anchor-vault manifest (`decisions/0044`) at session start and finds none — is the recognized, purpose-built condition that launches Bootstrap. This is a positive signal, not a generic error state or a fallback path; it exists specifically to be checked for and acted on.

**Personal bootstrap is a prerequisite, not one option among others.** Before any third-party entity, the very first vault any new user instantiates is their own personal anchor — `decisions/0040`'s premise 3 already requires this (the fallback-with-tag mechanism has nowhere to land for a user with no personal anchor yet); this Decision Record makes it the explicit first step of the mechanic that would otherwise let a user's first vault be someone else's entity.

**Four actions, in order:**

1. **Select** — which repository, for which entity. For a user's very first vault this is fixed (their own personal entity, anchor role); for any later vault it is the normal profile/entity choice already described in `skill/references/instantiation.md`.
2. **Orient** — a conversational walkthrough (not a link to go read alone) covering what Hipocampo is, why it needs a repository, and platform-specific installation variations (Claude, ChatGPT/Cursor, and others as they come up) — content and full rationale in `docs/getting-started-non-technical.md`. Conditional, not run on every instantiation: only on a user's very first (personal) vault, and only when there is a signal the user doesn't already know what Hipocampo is — a returning user instantiating a second or third vault skips this step entirely.
3. **Instantiate (skeleton)** — runs the existing scaffolding mechanism (`decisions/0032`, `skill/references/instantiation.md`), creating the repository and its `hipocampo.yaml`. Ordered before Interview, not after, because there is nothing for Interview's confirmed answers to be written into until the skeleton exists.
4. **Interview** — collects the facts `profile.md` (below) needs. Full depth on a user's first instantiation ever; a lighter pass on every later one, because `profile.md` already answers the identity questions from the second vault onward. Kept as its own step, separate from Orient's conversation — "what is a repository" is onboarding content, not a `profile.md` field, and conflating the two risks capturing throwaway conversational context as if it were a durable fact. The result closes the loop with **Instantiate (content)**: the same gate every other durable write already goes through (invariant 5, `SPEC.md` section 8) — presented before written, never written first and confirmed after.

**`profile.md`.** A structured, fixed-schema file, not a `type: person` content document — closer in kind to `hipocampo.yaml` (`decisions/0033`) than to anything covered by frontmatter, staleness, or the structural audit. Fields: `name` (full name), `preferred_name` (optional, how the user prefers to be addressed), `emails` (list), `github_handles` (list — the same field discovery, `decisions/0044`, resolves per entity, replacing the multi-account table `personalization.md` used to hold), `updated` (date of last confirmed edit). A fixed, small schema by design, not an open bucket for "whatever comes up" — a new field is only added the same way any other schema field is, through its own Decision Record, not through ad hoc capture. Capture happens conversationally during the Interview action, but the result is written only after the same explicit-confirmation gate as any other durable write — discovery-by-conversation is a capture method, not an exemption from that gate.

**Where `profile.md` lives, and what it doesn't do yet.** `profile.md` lives at the root of the user's personal anchor vault, alongside `hipocampo.yaml` — it is not generated by the scaffold's declarative profile system (`scaffold/profiles/`) in this Decision Record; the Interview action writes it directly. Wiring `profile.md` into the scaffold's own `outputs` mechanism is not done here.

## Rationale

Naming Bootstrap as a fourth mechanic, alongside CRUD, publication, and sequenced-removal, follows `decisions/0043`'s own stated reason for introducing the taxonomy before Bootstrap shipped: fitting a new capability into an existing category costs less than retrofitting one later. Making personal-anchor-first an explicit step of the mechanic (rather than leaving it as a premise stated only in `decisions/0040`) closes the gap between "the rule exists" and "the rule is actually enforced by the one piece of behavior that could violate it." Treating `profile.md` as fixed-schema config, not narrative content, keeps it out of rituals whose behavior assumes ordinary knowledge documents (staleness, atomicity review) — the same reasoning `decisions/0033` already applied to `hipocampo.yaml`.

## Discarded alternatives

- **Run Orient on every instantiation, unconditionally.** Discarded — repetitive and mildly patronizing for a user who has already instantiated one or more vaults; the conditional trigger (first vault, and only with a signal of unfamiliarity) keeps the onboarding content useful instead of routine noise.
- **Treat "discovery attempted, nothing found" as a generic error, handled by section 14's failure-and-recovery behavior rather than a named trigger.** Discarded — section 14's modes are about an agent recognizing something is *wrong*; a brand-new user with no anchor vault yet is not a failure state, it is the expected condition for a purpose-built mechanic to recognize and act on.
- **`profile.md` as an ordinary `type: person` document, subject to the normal frontmatter/staleness/structural-audit cycle.** Discarded — identity config that changes only when the user's own contact details change doesn't benefit from staleness review or atomicity checks designed for knowledge content, and forcing it through that cycle would be audit noise with no corresponding benefit.
- **Keep a separate identity-routing file (`personalization.md`'s multi-account table) alongside `profile.md`.** Already discarded in `decisions/0044`; restated here because `profile.md`'s `github_handles` field is the concrete replacement for what that table used to hold.
