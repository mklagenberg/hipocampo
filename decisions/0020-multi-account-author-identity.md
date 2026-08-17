# 0020 — Multi-account author identity and invitation direction between personal and corporate instance

**Status:** Accepted

## Context

Hipocampo is designed as a second brain for both personal and team/company use (multiple repositories, see DR0002). In practice, someone who operates a personal instance and also contributes to a corporate instance frequently has two different git accounts — one personal, one tied to the employing organization — that need to resolve to the same human `author` (section 2, invariant 2: `author` is always a person). Without a formal mechanism, the authorship scheme (and the access invitation between personal and corporate repositories) ends up ambiguous, or resolved differently by each person who adopts the methodology.

## Decision

Two new rules:

1. **Multi-account identity registration:** when a person operates more than one git account representing the same human `author`, this relationship (which accounts are the same person) is recorded in the instance — in the `AGENTS.md` of the least-restricted personal repository (see DR0015), never in the public `hipocampo`/`hipocampo-toolkit`. The skill's repository router (`hipocampo-toolkit/skill/SKILL.md`, personalization section) gains a new field for this relationship, filled in only in each user's personal copy, never in the generic copy.
2. **Invitation direction:** between a personal instance and a corporate instance of the same person, the access invitation (repository collaborator) always originates from the personal account inviting the professional account into the **personal** second brain — never the reverse (the professional account never invites the personal account into anything). This keeps personal identity as the anchor of trust: the person decides to bring their professional side into their personal knowledge; the employer never has standing to grant or deny access to someone's personal knowledge.

## Rationale

The invitation direction mirrors the real relationship between the two spheres: personal knowledge is always broader in ownership than corporate knowledge (the person owns their personal second brain; the company owns the corporate one, but not the person). Letting the professional account invite the personal one would subtly invert this ownership relationship — it would give the employing organization a gatekeeper role over knowledge that is not theirs. Recording the multi-account identity relationship only on the personal side, never publicly, follows the same principle already applied to all instance-specific data: the (public) methodology never carries anyone's real identity.

## Discarded alternatives

- **Register the multi-account identity relationship in the public `hipocampo`, as an example:** discarded — even anonymized, there would be no real need for a real example in the public repository; the generic mechanism is already sufficient without exposing anyone's identity.
- **Leave invitation direction open, at each person's discretion:** discarded because it would create ownership inconsistency between different instances, and the specific risk (an organization controlling access to personal knowledge) is serious enough to warrant an explicit rule, not a suggestion.
