# Line endings in methodology and vault repositories

Hipocampo recommends LF for authored text in Git and in working trees on
Linux, macOS and Windows. A repository-level `.gitattributes` file makes the
rule reproducible across clients, regardless of `core.autocrlf`. The
methodology repository already uses `* text=auto eol=lf`; its Windows `.bat`
and `.cmd` working-tree exception retains LF in Git. Binary files are never
normalized as text.

New vaults generated from the scaffold receive the same default. An existing
vault adopts it through its own reviewed branch and local policy. The
recommendation is about transport and materialization of bytes; it does not
change Record schema, authorize a write, or replace canonical CRUD. For an
existing vault with byte-preserved historical material, retain narrow `-text`
exceptions and document why. A blanket `git add --renormalize .` can rewrite
unrelated blobs and must be separately scoped, reviewed and authorized.

## Before editing an existing repository

1. Read that repository's `AGENTS.md`, manifest, constitution if present, and
   current `.gitattributes` at a fixed remote commit. Identify protected source
   paths and any binary or exact-byte package files.
2. Inspect the current attributes with `git check-attr text eol -- <path>` and
   tracked line endings with `git ls-files --eol`. On Windows, compare a
   worktree file with `git show HEAD:<path>` before using its bytes for a hash.
3. Add or narrow attributes on a dedicated branch. Review the diff and check
   that the change includes no incidental content or Record conversion.
4. For a byte-sensitive file, validate the Git blob itself. A clean worktree,
   normalized view, or local hash does not prove the remote blob's bytes.
5. After publication, inspect the target branch/ref and the `.gitattributes`
   blob remotely. Existing historical `verified_against` and source hashes
   remain historical evidence; do not update them merely for this policy.

`* text=auto eol=lf` detects binary data, but a vault may still require
explicit `binary` patterns for known assets and `-text` for preserved sources.
The Windows command-script exception is for execution in a Windows worktree,
not a different repository format. Do not claim that adding attributes alone
renormalized old blobs; it governs checkout and future staging.
