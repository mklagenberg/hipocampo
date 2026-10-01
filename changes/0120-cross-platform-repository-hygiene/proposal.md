# Change Set 0120 — Cross-platform repository hygiene

## Intent

Prevent generated Python/JavaScript caches, Excel lock/recovery files and
Windows/macOS filesystem metadata from cluttering either repository, while
making text line endings deterministic across contributor platforms.

## Scope

Add `.gitignore` and `.gitattributes` to the canonical methodology repository;
extend the existing `.gitignore` and `.gitattributes` in the independent
management repository; record the durable policy in Decision Record 0113; and
validate ignore behavior, EOL attributes, renormalization, links and repository
contracts.

Ignore only generated artifacts and temporary Excel lock/backup files. Real
Python/JavaScript source, dependency lockfiles and Excel workbooks remain
eligible for versioning. Preserve the management repository's existing
`-text` exceptions for archived and source paths.

## Authority and compatibility

Operational repository configuration, not a methodology contract. No released
behavior, SemVer, skill, scaffold, vault, migration, runtime or release surface
changes. The workspace root is not a Git repository, so each independent repo
receives only its own configuration.

## Acceptance criteria

- recognized text in `deliverable` is normalized to LF in the index and
  checkout; `.bat` and `.cmd` use CRLF only in working trees;
- binary formats, including Excel and Office files, are not normalized as text;
- shared ignore rules cover Python and JavaScript caches, Excel lock/backup
  files, and Windows/macOS metadata;
- `.py`, `.js`, dependency lockfiles and actual `.xlsx` files are not ignored;
- protected management source paths retain their current bytes and `-text`
  attributes;
- repository validators and an exact diff-coverage check pass, with any
  pre-existing global management validation findings clearly separated.

## Recovery

Revert this Change Set and Decision Record to restore the prior ignore and
attribute behavior. No tracked source file should require recovery; management
source paths are excluded from renormalization, and the `deliverable` baseline
currently contains no tracked CRLF files.
