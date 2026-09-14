# V3 candidate — surface authority and offline behavior

**Status:** unreleased V3 candidate.

The methodology `SPEC.md` and accepted Decision Records are the **normative sources**.
The skill is a procedural adapter that locates and applies those
sources. A vault manifest and local extension may specialize or restrict the
operation within the vault boundary, but cannot weaken methodology invariants.

Offline operation is fail-closed for normative uncertainty. The agent may
continue only when the required version, authority and criteria are proven in
the local material. Missing, stale or conflicting sources are disclosed to the
user and block the operation that depends on them. Mechanical operations that
are independently proven may continue with the limitation recorded.

Recency alone does not establish authority. A newer README or skill copy does
not silently defeat the canonical SPEC or an accepted Decision Record.
