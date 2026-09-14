# V3 processed ingress and declassification

X4.5 requires content to enter the destination already processed for that
destination: minimized, redacted and anonymized as authorized. The repository
does not become a raw inbox. REM is a local double check, not a replacement for
the processing boundary.

READ only identifies findings. CREATE/UPDATE may prepare a Record proposal, but
the Record is persisted only through the canonical CRUD gateway. The processed
ingress contract must prove minimization, anonymization, redaction completeness
and destination authorization before it can return `processed`.
Frontmatter, semantic and staleness findings remain separate, because only the
first class is mechanically normalizable. A queue normalizer therefore invokes
the CRUD write boundary for a Record document; it does not write the document
directly.
