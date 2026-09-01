# Bootstrap and invited-vault registration

Run connector preflight before Bootstrap or invitation handling. Establish the
personal anchor first, obtain explicit confirmation, then read the target
manifest before registering its address. Registration stores an address and
declared relationship only; it does not copy content. No write occurs before
confirmation. Missing capability, inaccessible targets and incompatibility
block the operation or require a separately authorized manual path.
