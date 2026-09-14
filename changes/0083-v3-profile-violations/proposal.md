# Change Set 0083 — V3 profile acceptance and local violation audit

## Problem

Profile membership, acceptance and revocation need a scoped, versioned
contract. Each vault also needs a local, Git-versioned audit directory for
violations and attempted violations concerning that vault.

## Proposed contract

Define expirable user/vault/entity links, acceptance and revocation, distinct
Owner/Authority/Curator/User/Source roles, and an audit index plus detailed
records visible and writable only within the authorized vault boundary. Audit
corrections are additive and never erase evidence.

## Risks and compatibility

Local transparency can itself disclose sensitive information. The contract
therefore scopes audit visibility to authorized vault users and avoids using
the audit log as a second source of truth.

## Acceptance criteria

- profile links are versioned, scoped and expirable;
- revocation preserves history and stops applicable current use;
- audit records include who, when, what, destination and result;
- corrections are versioned and additive;
- unauthorized audit reads/writes are rejected by fixtures.
