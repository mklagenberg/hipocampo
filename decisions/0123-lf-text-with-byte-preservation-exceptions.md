# 0123 — LF for authored text with byte-preservation exceptions

**Status:** Accepted

**Date:** 2026-10-22

## Context

Decision 0113 already sets LF for recognized text in the methodology
repository. Four existing V3 vaults force LF for Markdown, YAML and JSON, but
the scaffold does not emit `.gitattributes`, and contributors lack a concise
cross-platform procedure. Another existing vault preserves all files without
Git text conversion because its historical sources have an exact-byte
conservation requirement. Windows checkout conversion has caused misleading
hashes and apparent missing Records in earlier work.

## Decision

1. Recommend LF for authored text in methodology and Hipocampo vault
   repositories, declared with a versioned `.gitattributes` file. New scaffold
   instances receive `* text=auto eol=lf`, common binary declarations and a
   Windows command-script working-tree exception.
2. Existing vaults adopt the recommendation individually after reviewing
   their source-preservation rules. Retain narrow `-text` exceptions when exact
   historical bytes matter. Do not renormalize existing blobs implicitly.
3. Treat `.gitattributes` as repository transport metadata. It grants no
   permission, does not bypass RecordCrud, and does not amend the V3 Record,
   Chunk or frontmatter contract.
4. The methodology repository's current `.gitattributes` already satisfies
   the recommendation; document its behavior without rewriting it.

## Rationale

Shared attributes are more reproducible than each operator's Git settings.
The selected default avoids CRLF materialization in ordinary text. Explicit
exceptions preserve binaries, Windows command usability and historical
sources whose exact bytes are part of the evidence. The change extends the
existing Decision 0113 without creating a new compatibility requirement.

## Discarded alternatives

- Require each contributor to set `core.autocrlf`: local configuration is not
  versioned and does not provide the same result across machines.
- Renormalize every existing vault at once: that can change unrelated evidence
  and conflicts with local byte-preservation rules.
- Make LF a V3 schema-conformance gate: line endings are repository transport
  guidance; compatible vaults should not become incompatible for this reason.

## Scope and review

Change Set 0139 adds guidance and scaffold output. Each real vault keeps its
own review, branch and publication boundary. Constitution and taxonomy review
found no new constitutional premise or named methodological concept: existing
privacy, provenance and reversible-change clauses already govern this work.
