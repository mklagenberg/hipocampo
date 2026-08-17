# Mandatory personalization — repository router and identity

This generic skill (`hipocampo/skill/SKILL.md`) only knows one universal repository, the same for any user: `mklagenberg/hipocampo` (the methodology itself — spec, decisions, scaffold). It **does not** know any personal or corporate repository — hardcoding one would break the ability of any person or company to adopt the same skill.

Before real use, whoever adopts the methodology saves their own personalized copy (e.g., via `save_skill`), filling in the two tables below.

## Repository router

```
| Role                            | Repository                 |
|----------------------------------|----------------------------|
| Personal concepts (public*)      | [fill in: owner/repo]      |
| Personal vault                   | [fill in: owner/repo]      |
| Corporate content                | [fill in: owner/repo]      |
| Corporate vault                  | [fill in: owner/repo]      |
```

\* "public" here just means "least restricted within the personal scope" — no content repository is public to the internet (invariant 1, see `invariants.md`).

Not every instance has all four roles — fill in only what exists. Without this table filled in, the skill doesn't know where to read/write knowledge beyond the methodology itself.

## Multi-account author identity (fill in if applicable)

If the same person operates more than one git account that resolve to the same human `author` (e.g., a personal account and an account tied to an employer):

```
| Git account           | Role                       |
|------------------------|----------------------------|
| [fill in: @handle]     | Personal                    |
| [fill in: @handle]     | Professional/corporate      |
```

Never fill this in on the generic template copy — only on the personal copy. Invitation direction between personal and corporate instance: the personal account always invites the professional one into the **personal** second brain, never the reverse (`hipocampo/SPEC.md`, section 12; decision 0020).

## Example of using the router

> User: "save this decision about project X in my second brain"
>
> If "project X" is clearly work context, the personalized skill knows (from the table above) that "corporate content" is `owner-empresa/repo-corporativo`, not the personal vault. If the instance doesn't yet have the table filled in, the skill doesn't guess — it asks which repository the user wants to save to.