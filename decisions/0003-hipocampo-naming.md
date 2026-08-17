# 0003 — Naming: `hipocampo-*` prefix, "company" as a literal name

**Status:** Accepted

## Context

The previous naming convention used the prefix `second-brain-*`. It was also necessary to decide how to name the corporate content repository without tying the name to a specific company.

## Decision

Every repository in the methodology uses the `hipocampo-*` prefix. The word "company" is used literally (not as a placeholder to be substituted) in corporate repository names — `hipocampo-company` and `hipocampo-company-vault` — because the GitHub org the repository lives in already disambiguates which company it is. The `-vault` suffix is generic, used for sensitive/identifiable content, generalized from the original idea of a `-leadership` suffix (which described only the audience, not the content).

## Rationale

`second-brain-*` was discarded because the methodology's own name changed to Hipocampo — keeping the old prefix would create a branding inconsistency right out of the gate. Literal "company" avoids the trap of a placeholder that has to be remembered and substituted (risk of a forgotten or wrong name when instantiating); the GitHub org already resolves the "which company" ambiguity without needing to repeat it in the repository name. "-vault" generalizes better than "-leadership": the real separation criterion is content sensitivity/identifiability, not who has read permission — the audience can change (who counts as "leadership" varies by organization), but "sensitive content goes in the vault" is stable.

## Discarded alternatives

- **Keep `second-brain-*`** — discarded due to branding inconsistency with the methodology's new name.
- **`-leadership` as a suffix** — discarded because it describes only who accesses it, not what the content is; "vault" describes the content property that motivates the separation.
- **Generic placeholder like `hipocampo-{company}`** — discarded because it creates an unnecessary manual substitution step, since the GitHub org already disambiguates.
