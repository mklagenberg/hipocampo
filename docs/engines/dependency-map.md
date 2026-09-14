# V3 logical engine dependency map

The map is logical, not a Python import mandate.

```text
Source / MCP request
        |
        v
Ingress -----> Governance -----> REM / Curation
   |                |                  |
   v                v                  v
Artifact -------> Record CRUD <---- semantic review
   |                |
   v                v
Package ------> Delivery / Transfer
   |                |
   v                v
Operational Audit <--- Migration / Compatibility
        ^
        |
Maintenance and Verification
        ^
        |
Learning & Evolution <--- events, audits, validator results and lessons
```

Rules:

- MCP is a transport adapter, not a persistence engine;
- Ingress, Artifact, REM, Package, Delivery, Governance and Migration produce
  proposals or decisions;
- Record CRUD is the only Record mutation boundary;
- Operational Audit records bounded events and checks circulation, but does not
  become a second knowledge store;
- Maintenance may write operational queues and deterministic corrections only
  through the applicable CRUD boundary;
- Verification runs across the graph and never authorizes migration or release
  by itself.
- Learning & Evolution reads bounded signals and reviewed lessons to propose
  cases; it does not activate behavior or write Records.

The graph deliberately leaves semantic review as a gate rather than making it a
hidden dependency inside deterministic code.
