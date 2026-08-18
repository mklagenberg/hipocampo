# 0028 — Broadened trigger for remediation of a sensitive-data policy (2-A) violation

**Status:** Accepted

## Context

`decisions/0010` creates a narrow exception to invariant 3 (a document is never physically deleted), but the trigger, as written, is specific: "triggered by a legitimate deletion request from an identifiable data subject." This covers the case of someone exercising a right to erasure (LGPD Art. 16 / GDPR Art. 17). It doesn't cover a distinct, real case: content that already violates the sensitive-data policy (section 2-A) — a category unconditionally banned from a corporate instance, regardless of any request — is discovered by the weekly structural audit (section 5-C, function 3, which already exists specifically to find this) or by the instance operator directly, without the data subject having formally requested anything yet. Waiting for a formal request before correcting an already-confirmed violation of the instance's own declared policy doesn't seem to have been the original intent of `decisions/0010` — it's a scope gap in the text, not a deliberate choice.

## Decision

The mechanism from `decisions/0010` (physical deletion of the specific content, replaced by a tombstone, always an explicit human decision, never automatic, same caveat that git history isn't cleaned automatically) now has two triggers, not one:

1. A legitimate deletion request from an identifiable data subject (already existing, `decisions/0010`).
2. A confirmed violation of the sensitive-data policy by instance type (section 2-A), identified by the weekly structural audit (section 5-C) or by the instance operator directly — even without anyone's formal request.

In both cases, the legitimacy of the remediation is always assessed by the human responsible for the instance, never decided by the agent alone (same principle already established in `decisions/0010` and invariant 5).

This action is referenced operationally as "Redbutton" — see `SPEC.md`, section 13, and `decisions/0027`.

## Rationale

The 2-A policy already prohibits certain data categories unconditionally, "at no `visibility` level" — the prohibition is not conditioned on someone asking for removal. It makes sense for remediation not to depend on that either. Restricting the exception only to the data-subject-request trigger would leave the instance without a formal path for quick correction of an obvious leak that the methodology's own audit (5-C) was designed to find — the audit would have the power to detect but not to enable remediation, which defeats part of its purpose.

## Discarded alternatives

- **Edit `decisions/0010` directly, instead of creating a new decision.** Discarded: `0010` is already `Accepted` and was part of a published release (v1.4.0). Retroactively editing an accepted Decision Record breaks the very auditability principle the methodology advocates — the pattern already in use (`decisions/0016` refines `0008`, `decisions/0022` closes an asymmetry in `0019`) is always a new decision that extends, never rewriting the old one.
- **Let only the human operator identify the violation, without formally involving the structural audit.** Discarded: the structural audit (5-C, function 3) already exists specifically for this check — it doesn't make sense for the remediation mechanism to ignore the detection mechanism the methodology itself already built.
