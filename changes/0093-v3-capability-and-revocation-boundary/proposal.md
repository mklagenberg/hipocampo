# Change Set 0093 — V3 host capabilities and revocation reach

## Intent

Implement X6.5's capability classification, redaction boundary and explicit
revocation reach matrix.

## Scope

Add host capability fixtures, revocation primitives, contract documentation and
the final X6 integration checks.

## Acceptance criteria

- host capabilities are classified without presumption;
- revocation reach is explicit per surface;
- unreachable use can be blocked;
- TTL is not treated as proof;
- external backups are not claimed to be removed.
