# V3 skill and distribution conformance gate

The case suite preserves raw V3.0.0 behavior. Portable skill 2.2.0 remains
instructions-only; its separately installed runtime has its own executable tests.
The current routing envelope uses schema 2.0 and declares `external-receipt`;
it does not freeze a pending human verdict into the operational payload.
Historical 2.0.0/2.0.1 review evidence remains in docs/releases/ and Git history.

Run `python scripts/validate_v3_skill_conformance.py --root . --mode workflow`
for structural development validation. Experimental mode reports missing final
reviews as WARNING and never authorizes a private action or hides byte errors.
For final handoff, run release mode with `--receipt <external-file>` and the
aggregate `scripts/v3_preflight.py --channel stable --receipt <external-file>`.

The receipt binds the full payload digest. AI review covers every semantic
case, a distinct independent session challenges those cases after the primary
review, then a human explicitly approves the exact payload. Host observations
cover each required mode declared by the runtime manifest. Identity, evidence,
payload binding and ordered timestamps are mandatory. A receipt template or
agent-created pending file is not approval. Evidence-only changes must preserve
the reviewed operational digest; no pre-tag gate waits for publication.

The final external receipt is assembled before publication and may be attached
to the final draft. Installing stable separately verifies the actual immutable
published release and tag/source identity. Installing experimental needs only
the explicitly selected verified snapshot; an optional RC may be tag-only.
