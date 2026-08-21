# 0024 — UPGRADE.md: cumulative and idempotent instance-upgrade checklist

**Status:** Accepted

## Context

A user with an instance stuck on an old version of the methodology had, until now, nowhere to check what to do to become conformant with the current version. The three documents that touch this subject don't solve it: `CHANGELOG.md` is chronological and requires manually digging through release by release, deciding alone what counts as a necessary action; `MIGRATIONS.md` only covers MAJOR jumps (none have occurred yet between v1.0.0 and v1.9.0, so the file is empty, which doesn't mean "nothing to do"); `POS-INSTANCIACAO.md` only covers new instantiation, not upgrading an existing instance.

Concretely exercised with a hypothetical case (4 repositories stuck on v1.3.0, methodology at v1.9.0 + unreleased) and confirmed against a real case: the `hipocampo-company-vault` (Acme, anonymized — `decisions/0050`) repository is in exactly this situation — skill still at the "stub" stage (prior to v1.7.0), `CLAUDE.md` never migrated to `AGENTS.md`, `LICENSE` not verified. No one had a checklist to apply against it.

## Decision

`hipocampo/UPGRADE.md` is created: a **cumulative and idempotent** checklist — "what an instance should have, today, no matter where it started from" — organized by area (canonical file and skill; licensing; maintenance rituals; privacy), with each item marked **Mandatory**, **Recommended**, or **Informational**, citing the version it appeared in and the originating Decision Record.

Updating `UPGRADE.md` becomes a mandatory step of the release routine (DR0014), in sequence: (1) classify scope (DR0023); (2) tag + GitHub Release always published together, in the same step — never one without the other (closes the real asymmetry found in v1.3.0, which has a tag but never had a published Release); (3) move `CHANGELOG.md`'s `[Unreleased]` to a numbered section; (4) sync `hipocampo-toolkit`; (5) update `UPGRADE.md` — every MINOR change that affects an existing instance gets a new line; a PATCH correction that reveals a real instance bug (e.g., improper `LICENSE` inheritance, skill never installed) does too.

The Hipocampo skill, when checking for a new release (start of session), now points to `UPGRADE.md` as the next step, instead of trying to summarize `CHANGELOG.md` on the fly — this avoids reconstructing that manual work every session.

## Rationale

A document organized by version delta ("what to do to go from 1.3 to 1.4," then "from 1.4 to 1.5"...) would require the user to know their exact starting version and navigate N concatenated sections — fragile, and it grows without bound as the methodology evolves. A cumulative and idempotent checklist solves this: it works for any starting point, including for someone who has already done part of the work manually (it just confirms what's missing), and it doesn't grow in reading complexity as more versions ship — it only grows in number of items, which the user can check off and never reread.

## Discarded alternatives

- **Document by version delta.** Discarded for the reason above — fragile and doesn't scale.
- **Let the skill's new-release check summarize `CHANGELOG.md` on the fly, via the agent reading it.** Discarded: it produces inconsistent results across different sessions (the agent can summarize differently each time) and redoes synthesis work that should be done once, at release time, not repeated every session for every user.
