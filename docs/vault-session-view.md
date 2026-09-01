# Ephemeral vault session view

The session view is a transient record maintained separately for each vault
selected during an operation. It contains the vault address, entity, role,
scope, methodology version, compatibility state, observed access, verification
time and source. The target manifest remains the source of truth.

The view exists only for the active session. It is not a Git file, is discarded
when the session ends, and must not be used to infer authority. The anchor may
retain addresses, but not the transient observations. Target selection happens
before reading or writing; stale or ambiguous context blocks the operation.
