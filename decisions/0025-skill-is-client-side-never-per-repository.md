# 0025 — The skill runs client-side, per person/AI environment — never per repository

**Status:** Accepted

## Context

Every content instance carried its own `skill/` folder, automatically copied by GitHub's "Use this template" mechanism from `hipocampo-toolkit` — not by a deliberate architecture decision. This copy never had any functional effect: a skill only exists operationally when installed in the AI environment of the person operating it (via `save_skill` or an equivalent tool mechanism) — no agent scans GitHub repositories looking for a `SKILL.md` to activate automatically. The copy inside the repository was always an inert markdown file.

This duplication generated real confusion, raised by Mau when he asked directly: "isn't this going to cause confusion? If I install the skill here in Cowork, will it also use the skill from the repo?" The answer is no — but `POS-INSTANCIACAO.md` itself already had to explicitly warn not to edit the file inside the repository "as if that already activated it," a symptom that the previous design invited error. Auditing the 4 real content repositories (see fixes via `UPGRADE.md`), none of them ever had a skill actually installed — all of them carried only the original `SKILL-STUB.md` from the template, never replaced.

## Decision

The Hipocampo skill has exactly **one** place where it exists in operative form: the AI environment of the person operating the instance, installed (personalized, with the repository router filled in) from the canonical template at `hipocampo-toolkit/skill/SKILL.md` + `references/`. A content repository **never** carries its own copy of the skill — the `skill/` folder is no longer part of the expected scope of a content instance.

`hipocampo-toolkit/POS-INSTANCIACAO.md`, step 3, now instructs: delete the `skill/` folder inherited from the template right after instantiating (it's a residue of "Use this template," never functional), and install the personalized skill directly from `hipocampo-toolkit`, referencing the new repository in the repository router.

`hipocampo-toolkit` continues carrying `skill/SKILL.md` + `references/` at its own root — there it makes sense, because it's the canonical distribution source, not a content instance.

## Rationale

Keeping a "decorative" copy of the skill in every content repository has only costs, no real benefit: (1) it suggests a wrong mental model — "each repo has its own skill" — when the correct model is "one skill per person/environment, operating over N repositories via the router"; (2) it creates additional drift surface (copy in the toolkit, copy in each repo, copy installed on the client — three places instead of two); (3) in practice, it led to the same result across the 4 real audited repositories: the copy was never updated beyond the original stub, because no one had a real reason to touch it.

## Discarded alternatives

- **Keep the copy in the repository as a "read-only reference" documenting which skill version was in use when the repo was synced.** Discarded: this information is already captured by the Hipocampo version declaration in `AGENTS.md` — no need for an entire copy of `SKILL.md` just for that.
- **Add a stronger warning inside the file, instead of removing the folder.** Discarded: the warning already existed (`POS-INSTANCIACAO.md`) and did not prevent the 4 real repositories from never having the skill installed — the problem is structural, not communicational.
