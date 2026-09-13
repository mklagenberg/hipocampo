# Change Set 0091 — V3 CRUD operational events

## Intent

Implement X6.3's bounded operational audit for defined CRUD and exceptional
actions without copying knowledge content.

## Scope

Add the CRUD event contract, candidate Decision Record and integrated fixtures.

## Acceptance criteria

- governed action metadata is separated from content history;
- reads are not automatically durable events;
- failures and unavailable targets remain auditable;
- sensitive content is excluded or redacted.
