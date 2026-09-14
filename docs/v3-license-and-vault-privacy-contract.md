# V3 candidate — methodology license and vault privacy

**Status:** unreleased V3 candidate. The released v2.2.0 license behavior is
not migrated or silently changed by this document.

## Boundary

The legal license belongs to the methodology when it has its own repository
(`LICENSE`, such as Apache-2.0). That license governs use of the methodology
repository and its tooling. It does not grant access to knowledge stored in a
vault.

Once methodology material is installed or operated inside a vault, the local
vault contract governs access, purpose, audience, retention, circulation and
processing within that vault. Records, Chunks, Artifacts, Packages and
references do not receive a generic `content_license` field by default.

Third-party notices remain possible when a particular methodology artifact
has an applicable attribution or notice obligation. A notice is not an access
permission and does not override the vault contract.

## Compatibility boundary

The active v2.2.0 `SPEC.md` and existing instances remain unchanged until a
future V3 release and explicit migration gate. This candidate records the
future separation so that implementation, migration and publication cannot
silently conflate license and privacy.
