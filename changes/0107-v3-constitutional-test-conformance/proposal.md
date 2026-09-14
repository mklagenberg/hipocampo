# Change Set 0107 — V3 constitutional test conformance

## Intent

Make the V3 deterministic and semantic test package explicitly traceable to
the project Constitution and accepted Decision Records.

## Scope

This operational Change Set adds case-level normative basis, deterministic
case bindings, constitutional edge cases, and validators for the V3 candidate.
It also records the rejudgment status of project rules after adoption of
`FF-CON-0001`.

It does not publish V3, change V2.2, migrate a vault, write to a vault cache,
or authorize a Record mutation.

## Governing interpretation

The Constitution is the general rule. A specific rule may contradict it only
through an accepted, explicit and scoped Decision Record. Constitutional
amendments require rejudgment of active specific rules before new use.

## Acceptance criteria

- every matrix deterministic case has an explicit binding and assertion;
- every semantic case has constitutional and Decision Record references;
- constitutional exception and rejudgment scenarios are represented;
- validators reject missing, malformed or out-of-scope normative references;
- existing semantic dispositions remain unchanged unless a documented conflict
  is found;
- deterministic and semantic validators pass twice;
- the four local vault caches and V2.2 remain unchanged.

## Recovery

Revert only this Change Set's test metadata, validators, fixtures and reports.
The historical 0106 evidence remains intact and no vault state is affected.
