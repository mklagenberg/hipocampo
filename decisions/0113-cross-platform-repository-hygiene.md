# 0113 — Cross-platform repository hygiene

**Status:** Accepted

**Date:** 2026-09-30

## Context

The canonical methodology repository had no versioned `.gitignore` or
`.gitattributes`. Its current tracked files happen to use LF, but that state was
not declared for contributors on Windows, macOS and Linux. The management
repository already normalizes ordinary text to LF and deliberately disables
text conversion for archived and source material that must remain byte-stable.
Its `.gitignore` covered Python bytecode and a few OS artifacts, but omitted
common JavaScript caches and Excel lock/recovery files.

The repositories are independent. Repository rules belong in each repository;
the workspace root is not a Git repository and cannot supply shared Git
configuration to clones.

## Decision

1. In the canonical `deliverable`, normalize recognized text to LF both in Git
   and in working trees through a versioned `.gitattributes` rule.
2. Preserve CRLF in working trees only for Windows `.bat` and `.cmd` scripts;
   their repository representation remains normalized LF.
3. Declare common image, PDF, archive and Office workbook/document formats as
   binary so line-ending conversion and text diffs do not alter or misrepresent
   them.
4. Share `.gitignore` rules in both repositories for generated Python and
   JavaScript caches, Excel temporary lock/backup files, and operating-system
   metadata from Windows and macOS.
5. Do not ignore real `.py` or `.js` source, dependency lockfiles, or actual
   Excel workbooks. `.gitignore` prevents new untracked files from being added;
   it does not untrack files already in Git.
6. Preserve the management repository's existing `-text` exceptions for
   `archive/`, `assets/`, `backlog/source/` and `research/source/`. Those paths
   include source material whose bytes are intentionally retained. Do not
   renormalize them under this change.

This is an operational repository policy only. It changes no methodology
contract, vault content, migration, skill package, release version or runtime
behavior.

## Rationale

The repository-level `text=auto` and `eol` attributes make line endings
consistent regardless of each contributor's local `core.autocrlf` setting.
The `.bat`/`.cmd` exception accommodates Windows command interpreters without
changing the canonical LF representation. Explicit binary attributes protect
formats whose bytes must not be treated as text. Narrow ignore patterns block
generated clutter while keeping intentional source and data files versionable.

The existing management exceptions are preserved because normalizing those
source paths would change archived source bytes without improving the active
product repository's EOL consistency.

## Discarded alternatives

- **Rely only on each contributor's `core.autocrlf` setting:** rejected because
  local configuration is not shared or authoritative across clones.
- **Ignore every Excel workbook or every file with `.py`/`.js` extensions:**
  rejected because legitimate source and project data must remain versionable.
- **Normalize every file in `management`, including protected source paths:**
  rejected because those paths explicitly preserve historical material and
  already opt out of text conversion.
- **Ignore broad directories such as `dist/`, `build/` or `.yarn/`:** rejected
  because their contents can be intentional project outputs or dependencies
  committed by a repository's chosen workflow.

## Validation and limits

- Inspect `.gitignore` behavior with `git check-ignore` for representative
  generated and operating-system files and confirm that real source, workbook
  and lockfile examples remain eligible for versioning.
- Inspect `.gitattributes` behavior with `git check-attr` and `git ls-files
  --eol`; renormalize the `deliverable` index and review the full diff before
  committing.
- Run the canonical repository, Change Set, management SDD and link validators.
- Confirm protected management source files are unchanged and retain their
  existing `-text` attributes.

These checks prove repository configuration and current file-state consistency;
they do not guarantee that future contributors never force-add ignored files.

## Approval

The project operator explicitly requested these repository hygiene changes and
authorized planning, validation, implementation and correction on 2026-09-30.
