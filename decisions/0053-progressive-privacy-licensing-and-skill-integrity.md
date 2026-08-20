# 0053 — Progressive privacy remediation, licensing boundaries, and skill-package integrity

**Status:** Accepted

## Context

The existing privacy rule was corporate-only, allowed one absolute-value exception, and did not state how a methodology update should affect historical content. Contribution guidance also lacked a mandatory terminology gate, the public methodology entry point did not route common user intents, and the skill had a version but no package-integrity contract for a confirmed update.

## Decision

Credentials and non-public financial values are prohibited prospectively in every content vault. A public financial value requires an explicit public URL and date citation. Existing content is not swept merely because the methodology changes: it is flagged on READ and remediated only when updated or processed by REM, with the existing confirmation gate.

The structural audit's privacy function includes credentials, financial provenance, and anonymization of public methodology material. Methodology Apache-2.0 licensing and proprietary content-vault licensing remain separate; content governance artifacts are never copied into non-content repositories or client-local skill state.

The canonical skill has independent SemVer and a package lock containing hashes of the distributable files. Update availability is read from the canonical manifest; installation verification uses the immutable release tag and lock, never a self-referential commit hash or unverified `main` content. The skill only notifies and waits for confirmation.

## Rationale

Prospective enforcement protects new material without treating every methodology upgrade as authorization to inspect or alter a person's whole historical knowledge base. A release tag plus a lock avoids the structural impossibility of a manifest accurately self-referencing the commit that contains its own new value.

## Discarded alternatives

- **Repository-wide privacy migration at update time.** Rejected: it exceeds the requested operation and conflicts with the explicit CRUD/REM progressive-remediation model.
- **Keep absolute financial case values as an exception.** Rejected: public verifiability is a clearer boundary than purpose.
- **Use `source_commit` as the skill's update identity.** Rejected: it cannot self-reference; the release tag and package lock provide immutable verification instead.

## Status

Accepted.
