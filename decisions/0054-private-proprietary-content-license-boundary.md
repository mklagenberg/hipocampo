# 0054 — Strict private proprietary boundary for content-vault licenses

**Status:** Accepted

## Context

Hipocampo has always required knowledge vaults to remain private and their root
licenses to be proprietary. However, the legacy personal and corporate templates,
and matching `visibility: public` prose, incorrectly stated that copying and
reproduction were free. That wording created an external-use permission that
contradicted the private-vault invariant and could be replicated by every new
instantiation.

## Decision

Every content-vault root `LICENSE` is strictly private and proprietary for its
declared holder. `visibility` and mechanically derived `LicenseRef` identifiers are
handling classifications for people already authorized to access the private
repository; they never grant an open license, external publication, copying,
redistribution, sublicensing, external indexing, or model training.

The canonical templates, scaffold guidance, specification, and upgrade guide express
the same boundary. Existing vaults correct their root license structurally. This does
not authorize a repository-wide content inspection or rewrite: a legacy frontmatter
reference is governed by the corrected root contract and any document-level finding is
handled progressively through ordinary CRUD or REM.

## Rationale

The root license is the correct place to establish ownership and the external-use
boundary. Treating a visibility label as a license is both legally ambiguous and a
privacy risk. Correcting the root artifact fixes the unsafe permission immediately
without copying content-license language into the public methodology's own Apache
license, a client-side skill, or local adapter state.

## Discarded alternatives

- **Preserve free copying for `visibility: public`.** Rejected: it contradicts the
  private/proprietary contract and makes a repository-access label look like public
  distribution consent.
- **Rename or rewrite every historical `LicenseRef` immediately.** Rejected: the root
  contract resolves the unsafe interpretation without a content sweep; progressive
  CRUD/REM remains the remediation mechanism for document-level normalization.
- **Copy a content license into every methodology or client artifact.** Rejected:
  methodology Apache-2.0 and content-vault proprietary licensing have different
  owners and purposes.
