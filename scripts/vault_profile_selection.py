#!/usr/bin/env python3
"""Pure declaration gate for V3 Vault creation and legacy-profile diagnosis.

This helper never creates a repository, authorizes a Record operation, or
changes GitHub permissions. Semantic review and the actual host gates remain
separate.
"""
from __future__ import annotations

import argparse
import json


VAULT_PROFILES = frozenset({"entity", "team", "personal"})
SUGGESTED_DEFAULT = "team"


def evaluate(
    *,
    source_state: str,
    profile: str | None = None,
    entity: str | None = None,
    explicit_selection: bool = False,
    plan_confirmed: bool = False,
    creator_authenticated: bool = False,
    representative_event_capable: bool = False,
    profile_dependent: bool = False,
    conflicting_profile: bool = False,
) -> dict[str, object]:
    """Return a declaration result, never a technical or CRUD authorization."""
    result: dict[str, object] = {
        "suggested_default": SUGGESTED_DEFAULT,
        "profile": profile,
        "declaration_complete": False,
        "profile_policy_ready": False,
    }
    if source_state not in {"new_v3", "incomplete_v3", "existing_v3", "v2_read"}:
        result["status"] = "invalid_source_state"
    elif source_state == "v2_read":
        result["status"] = "legacy_read_only"
        result["warning"] = "VERSION_OUTDATED"
    elif source_state == "incomplete_v3":
        result["status"] = "incomplete_creation"
        result["warning"] = "INCOMPLETE_CREATION"
    elif conflicting_profile:
        result["status"] = "conflicting_profile"
    elif profile is not None and profile not in VAULT_PROFILES:
        result["status"] = "invalid_profile"
    elif source_state == "existing_v3":
        if profile is None:
            result["status"] = "legacy_route_only"
            result["warning"] = "PROFILE_UNDECLARED"
        else:
            result["status"] = "declared_profile"
            result["profile_policy_ready"] = True
    elif profile is None or not explicit_selection:
        result["status"] = "needs_selection"
    elif not isinstance(entity, str) or not entity.strip():
        result["status"] = "needs_entity"
    elif not plan_confirmed:
        result["status"] = "needs_confirmation"
    elif not creator_authenticated or not representative_event_capable:
        result["status"] = "creation_capability_blocked"
    else:
        result["status"] = "selection_confirmed"
        result["declaration_complete"] = True
        result["profile_policy_ready"] = True
    if source_state == "existing_v3" and profile is None and profile_dependent:
        result["blocked_operation"] = "new_profile_dependent_policy"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-state", required=True, choices=["new_v3", "incomplete_v3", "existing_v3", "v2_read"])
    parser.add_argument("--profile", choices=sorted(VAULT_PROFILES))
    parser.add_argument("--entity")
    parser.add_argument("--explicit-selection", action="store_true")
    parser.add_argument("--plan-confirmed", action="store_true")
    parser.add_argument("--creator-authenticated", action="store_true")
    parser.add_argument("--representative-event-capable", action="store_true")
    parser.add_argument("--profile-dependent", action="store_true")
    parser.add_argument("--conflicting-profile", action="store_true")
    args = parser.parse_args()
    result = evaluate(**vars(args))
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] in {"selection_confirmed", "legacy_route_only", "declared_profile", "legacy_read_only"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
