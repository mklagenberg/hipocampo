# V3.0.0 contract — revocation and reach matrix

**Status:** published in V3.0.0; derived from D6.5. Runtime reach remains bounded by the declared surface evidence.

Revocation is an operational event with requester, approver, target, scope,
reason class, mechanism, result and a reach matrix. Each surface is marked
`invalidated`, `not_reached`, `unavailable` or `not_applicable`.

The host invalidates what it can deterministically reach. **TTL is not proof**
of revocation. A surface outside
the proven reach is disclosed and future use is blocked when privacy,
authority, staleness or integrity would otherwise be compromised. TTL is not
proof of revocation. Projections remain deferred and never become authority.
