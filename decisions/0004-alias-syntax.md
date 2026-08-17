# 0004 — Cross-repository alias syntax: `$name`, not `{{name}}`

**Status:** Accepted

## Context

The `related` field (and `context_anchor`) needs a syntax to distinguish a reference to the same repository from a reference to a different repository (SPEC.md, section 6).

## Decision

Use the `$alias:` prefix (example: `$concepts:path.md`) for cross-repository references, resolved by a `registry.md` file.

## Rationale

The more obvious alternative, `{{name}}`, is the standard syntax of template engines like Jinja and Mustache. If a Hipocampo file ever passes through a pipeline that uses one of these engines (static site generation, batch processing), `{{name}}` runs a real risk of being interpreted as a template variable to be substituted, silently corrupting the reference. `$` has no special meaning in plain YAML nor in the most common template engines in this context — syntax with no known ambiguity.

## Discarded alternatives

- **`{{name}}`** — discarded due to the risk of collision with template engine syntax, described above.
- **Full GitHub URL** — discarded for verbosity and for coupling the reference to the repository's current name; renaming a repository would break every existing reference, instead of just one line in `registry.md`.
