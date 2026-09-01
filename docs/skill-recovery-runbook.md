# Bounded skill recovery runbook

Classify the failure surface first: release availability, manifest or lock,
installed files, discovery, permission, or anchor. Preserve the last known-good
installation, verify source and version before replacement, and keep rollback
available. Never promote an unverified package to the active skill, request or
persist credentials, or overwrite the known-good installation. This runbook
does not test remote release access; the current result is local and procedural.
