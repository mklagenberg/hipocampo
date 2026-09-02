# Change Set 0065 — Ephemeral vault session view

## Intent

Define a per-vault, session-only context for heterogeneous operations without
persisting observations or inferring authority.

## Decision

Implements the accepted session-view boundary. Ambiguous or incompatible
targets are blocked before access.
