# V3 candidate — revocation and reach matrix

**Status:** unreleased V3 candidate; derived from D6.5.

Revocation is an operational event with requester, approver, target, scope,
reason class, mechanism, result and a reach matrix. Each surface is marked
`invalidated`, `not_reached`, `unavailable` or `not_applicable`.

The host invalidates what it can deterministically reach. **TTL is not proof**
of revocation. A surface outside
the proven reach is disclosed and future use is blocked when privacy,
authority, staleness or integrity would otherwise be compromised. TTL is not
proof of revocation. Projections remain deferred and never become authority.
