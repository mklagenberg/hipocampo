# Change Set 0087 — V3 structural language and content language

## Intent

Implement D5.4's distinction between English structural vocabulary and the
locally declared language of knowledge content.

## Scope

Document the candidate policy and validate English structural markers plus
local content-language declaration. No existing vault is migrated.

## Acceptance criteria

- methodology structure is English;
- vault structure is English;
- content language is declared at instantiation;
- English is the default;
- ES-419 structural support is not falsely claimed.

## Compatibility and recovery

Existing v2 instances remain readable and unchanged. Removing the candidate
policy does not rewrite any content.
