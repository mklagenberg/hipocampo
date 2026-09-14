# V3 transfer and retraction

X4.3 separates delivery, receipt, REM, current use and retraction. Delivery
does not publish or promote. A received Package remains local `new` and
`pending_rem` until REM and semantic acceptance complete.

Retraction is an additive control event. It blocks current use according to the
destination contract and preserves the Package and ledger history.
