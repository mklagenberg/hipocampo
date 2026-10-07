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

SPEC.md prepares the V3.0.0 authority; existing V2 instances remain unchanged until their explicit migration gate. The published baseline remains v2.2.0 until actual publication. This candidate records the
future separation so that implementation, migration and publication cannot
silently conflate license and privacy.

## Release-preparation projection

This adjacency is included by the prepared V3 SPEC. Unreleased/candidate wording above records development state, not proof of publication. Its normative scope is subordinate to SPEC and accepted decisions; existing vault adoption remains separately governed.
