# Hipocampo — Migrations

Migration guide for each MAJOR version jump (SemVer — see SPEC.md, section 9, and DISCLAIMER.md).

MINOR and PATCH migration requires no action — see DISCLAIMER.md, section "Versioning and what it means for you". This file only documents MAJOR jumps, which require active migration by definition.

## How to use this document

Each instance declares, in its own `CLAUDE.md`/README, the version or compatibility range it implements. When a new MAJOR version is released, find here the section corresponding to the jump you need to make (for example, "1.x → 2.0") before updating your instance's version declaration.

## History of MAJOR jumps

No MAJOR jump has occurred yet. The initial version is 1.0.0 — there is no migration to document until the first incompatible change.

When the first MAJOR jump happens, the corresponding section here will follow this format:

```markdown
## 1.x → 2.0

**What broke:** [direct summary]
**Why:** [link to the Decision Record in decisions/ that motivated the change]
**Step by step:**
1. ...
2. ...
**How to know if your instance can migrate already:** [checklist]
```