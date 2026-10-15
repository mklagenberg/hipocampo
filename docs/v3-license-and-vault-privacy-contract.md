# V3.0.0 contract — methodology license and vault privacy

**Status:** published in V3.0.0. Existing V2.2.0 instances are not migrated or
silently changed by this document.

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

SPEC.md defines the published V3.0.0 authority; existing V2 instances remain unchanged until their explicit migration gate. This contract records the
future separation so that implementation, migration and publication cannot
silently conflate license and privacy.

## Release-preparation projection

This adjacency is included by the published V3 SPEC. Existing vault adoption remains separately governed.
