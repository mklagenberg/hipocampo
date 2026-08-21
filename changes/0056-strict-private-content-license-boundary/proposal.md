# Change Set — 0056: Strict private content-license boundary

## Summary

Corrects a legacy template and specification contradiction that treated a
`visibility: public` classification as permission for copying and reproduction. The
root content-vault license becomes the sole external-use boundary: strictly private,
proprietary, and held by the declared entity.

## Class and SemVer

**normative; patch.** The private/proprietary boundary and private-vault invariant
already governed content repositories. This corrects an unsafe contradictory template
and projection; it adds no schema field or capability. Existing vaults replace their
root license structurally, without a content sweep or migration of historical memory.

## Acceptance criteria

- No canonical content-license template grants free copying, reproduction, or public
  redistribution from `visibility: public`.
- SPEC and scaffold distinguish handling classification from legal permission.
- The Apache-2.0 methodology license remains separate from content-vault licenses.
- The upgrade guide requires the root-license correction without authorizing a
  retrospective document inventory.
- Validators pass and the Change Set covers every protected changed surface.

## Recovery

If the corrected language proves unsuitable for a holder's external legal instrument,
the holder obtains legal review and replaces only that vault's root license through a
confirmed update. Do not restore a generic permission or alter historical documents
without a separate confirmed CRUD/REM plan.
