> **Movido / Moved:** este documento foi traduzido e renomeado para `scaffold/skeleton/POST-INSTANTIATION.md`. Este arquivo é mantido como redirecionamento e nunca será apagado (ver invariante "documento nunca é apagado fisicamente", SPEC.md seção 8).
>
> This document was translated and renamed to `scaffold/skeleton/POST-INSTANTIATION.md`. This file is kept as a redirect and will never be deleted (see the "a document is never physically deleted" invariant, SPEC.md section 8).

## V3 activation gate

For stable, confirm the published immutable methodology release, the skill version and package hashes named by its canonical manifest, and the vault ^3.0.0 tuple. Verify the GitHub Release reports `immutable: true`, its tag resolves to the release target, pin that commit and check every package-lock hash. Verify the actor, authorized vault scope and canonical CRUD capability. Accept the first active Collection before creating any Record. The example is proposal documentation, not a Record; do not turn it into knowledge by direct editing. No inbox is generated. Block activation if any required declaration or capability is unknown.

For explicitly selected experimental execution, resolve the pinned source commit
or RC tag and distribution hashes instead; no GitHub Release or future stable is
required. Candidate/final-readiness state emits WARNING and valid canonical
operations continue. Authorization, compatibility and integrity remain required.
See the selected source's docs/v3-runtime-usage.md; this creates no Record or
permission. Template variables must be filled before instance activation.
