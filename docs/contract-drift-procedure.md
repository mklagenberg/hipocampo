# Contract drift procedure

Before operating on a vault, reread its manifest and applicable instructions.
Classify the observed difference as content change, instruction change,
contract change, methodology-version change, or unavailable target. Content
changes may continue under the current contract. Instruction changes require a
fresh read. Contract changes block the affected operation until compatibility is
resolved. Version changes route through the compatibility contract. Unavailable
targets remain blocked. Unknown drift is never silently accepted.

For V3 migration preparation, `docs/v3-contract-drift-registry.yaml` maps the
methodology surfaces to their governing authorities, existing drift classes,
allowed actions, fixtures and validators. The registry is a traceability aid;
it does not replace those authorities or prove semantic truth.
