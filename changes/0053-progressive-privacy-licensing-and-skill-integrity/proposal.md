# Change Set — 0053: Progressive privacy, licensing, routing, and skill integrity

## Summary

Makes privacy a core, progressive operating criterion; separates methodology and content licensing; requires terminology governance; routes methodology requests by intent; and makes client-side skill updates independently versioned and integrity-verifiable.

## Class and SemVer

**normative and operational; minor.** New and touched content gains requirements immediately, while existing vaults remain compatible and are remediated only through ordinary CRUD or REM. No MAJOR migration or full-repository inspection is required.

## Acceptance criteria

- SPEC, audit, CRUD, REM, scaffold, upgrade, documentation, and skill agree on progressive privacy remediation.
- Contribution and agent entry points route terminology and user intents deterministically.
- The skill manifest and package lock have independent version/integrity semantics and do not self-update.
- Repository validators pass, including package-lock verification and diff coverage.

## Recovery

If a new privacy rule produces an ambiguous historical finding, report it without copying the sensitive value and await a confirmed Update or Redbutton decision. Revert the methodology change through a new Decision Record and Change Set; never weaken a local vault silently.
