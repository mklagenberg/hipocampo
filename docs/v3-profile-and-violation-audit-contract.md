# V3 profile and local violation audit

X4.6 defines versioned, scoped and expirable user–vault–entity links. Owner,
Authority, Curator and User remain distinct. Acceptance and revocation affect
the operation context; they do not rewrite source authority.

Each vault may maintain a Git-versioned audit index and detailed records for
violations or attempted violations concerning that vault under
`meta/audits/`. Authorized users may read and write within the vault boundary.
Corrections are additive and retain the original event.
