# Maintenance rituals — frontmatter audit, REM, structural audit

Three rituals, different cadences, always scoped to **one repository at a time** — each Hipocampo repository has its own `inbox/` and its own queue. Full reference: `hipocampo/SPEC.md`, sections 5-A, 5-B, 5-C.

## Execution order in a daily cycle

1. **Frontmatter audit** (deterministic, first)
2. **REM ritual** (consolidation + update, reads the output of step 1)

The structural audit runs separately, on a weekly cadence.

## 1. Frontmatter audit — daily, deterministic

Mechanical scan of the frontmatter (never the body) of every document in a repository: expired `ttl` (per `temporality`), missing required field, a deprecated pt-BR controlled-vocabulary value still in use (e.g. `source: conversa` instead of `source: conversation`) — matched literally against `hipocampo/docs/vocabulary-dictionary.md`, no judgment involved — other mechanically detectable violation. Produces/updates `meta/fila-de-manutencao.md`. **Never decides disposition** — only reports. This is not AI agent judgment: it's a fixed-rule, reproducible scan. See decision 0017 and decision 0035.

## 2. REM ritual — daily, two functions

**Consolidate:** read `inbox/` (short-term memory — already passed through an attention gate, e.g. a session dump/check-in, but not yet atomic nor in the right place; it's a sanitization stage, not raw capture). Decide per item: becomes a new document, merges with an existing one, or is discarded.

**Update old memories:** read `meta/fila-de-manutencao.md` (output of the frontmatter audit) and decide the disposition of each pending item: revalidate (including via external research when `source: url` — the same trigger as the `deep-research` skill), archive, supersede, or fix a field — normalizing a flagged deprecated vocabulary value (per `hipocampo/docs/vocabulary-dictionary.md`) to its current English form is a routine "fix a field," presented the same way as any other field fix, not skipped or auto-applied.

**Always present the full plan for either of the two functions before any write** — the same explicit-request invariant (see `invariants.md`, item 5), applied to this ritual specifically. See decision 0008, decision 0016.

### Example of a cycle

> `meta/fila-de-manutencao.md` (produced by the frontmatter audit) lists: `projetos/case-acme.md` with `ttl` expired 40 days ago, `temporality: ephemeral`.
>
> REM ritual, "update old memories" function: since it's `ephemeral` and has passed its deadline without renewal, the section 5 rule already pre-flags it as "suggestion: archive/supersede". The agent presents: "`case-acme.md` has a `ttl` expired 40 days ago, `ephemeral` — I suggest marking `status: archived`. Confirm?" — never applies it on its own.

## 3. Structural audit — weekly, three functions

1. **Atomicity** — do recently consolidated documents (or ones flagged by the queue) still represent a single concept, or should they be split?
2. **Positioning** — does the `category`/folder structure still make sense? Is any document outside the scope declared in the repository's `AGENTS.md` (section "Scope of this repository")?
3. **Sensitive data leakage** — does any document contain something the sensitive-data policy (SPEC section 2-A) prohibits for the **instance type** declared in `AGENTS.md` (field "Instance type": `corporate`/`personal` — deprecated pt-BR values `corporativa`/`pessoal` remain valid and equivalent, see `hipocampo/docs/vocabulary-dictionary.md`) — never inferred by the agent from the repository name. See decision 0022.

4. **Controlled-vocabulary check on repository-level fields** — `AGENTS.md`'s "Instance type" and `hipocampo.yaml`'s `instance.domain`/`instance.tier` aren't scanned by the daily frontmatter audit (that one only covers document frontmatter). Whenever the structural audit reads either file, it checks their values against `hipocampo/docs/vocabulary-dictionary.md` too, and flags a deprecated pt-BR value the same way as any other finding below — never rewritten on its own. See decision 0035.

Any finding from the four functions is always presented to the responsible human before any action — moving, splitting, or removing a document never happens on its own. See decision 0019 and decision 0035.

### Example

> Weekly audit of the corporate repository (`AGENTS.md` declares "Instance type: corporativa" — the deprecated pt-BR value, still valid). It finds `trabalho/negociacao-fornecedor-y.md` citing a contract value in R$. This is exactly what the sensitive-data policy prohibits for a corporate instance (vendor value). The agent flags it: "I found a vendor contract value in `negociacao-fornecedor-y.md` — the corporate instance policy does not allow this, not even under `restricted`. Do you want me to remove the absolute value (keeping the rest of the document), or would you rather review it yourself?" — it never edits on its own. Separately, since `AGENTS.md` still declares the deprecated `corporativa` value, the agent also notes it as a normalization candidate for this same audit cycle: "Also, unrelated to the finding above: this repository's `AGENTS.md` still uses the older 'Instance type: corporativa' — want me to update it to 'corporate' (`hipocampo/docs/vocabulary-dictionary.md`)? Purely cosmetic, doesn't change behavior."

## Automation (scheduled tasks)

A recurring cadence is a good candidate for an agentic `scheduled task` (daily frontmatter audit + REM in sequence; weekly structural audit separately). Automation is an implementation decision per instance, not part of the methodology itself — configuring it (or not) is up to whoever operates that instance.