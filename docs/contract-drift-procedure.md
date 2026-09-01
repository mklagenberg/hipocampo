# Contract drift procedure

Before operating on a vault, reread its manifest and applicable instructions.
Classify the observed difference as content change, instruction change,
contract change, methodology-version change, or unavailable target. Content
changes may continue under the current contract. Instruction changes require a
fresh read. Contract changes block the affected operation until compatibility is
resolved. Version changes route through the compatibility contract. Unavailable
targets remain blocked. Unknown drift is never silently accepted.
