#!/usr/bin/env python3
"""Integrated adversarial validation for V3 X4.1-X4.6."""
from __future__ import annotations

import argparse
from copy import deepcopy

from v3_ingress_engine import IngressError, process_ingress, read_findings, rem_double_check
from v3_multivault_engine import detect_authority_collisions, detect_successor_cycles, resolve_visible_graph
from v3_policy_engine import evaluate_passage, evaluate_policy
from v3_privacy_gate import evaluate_pipeline, evaluate_privacy_gate
from v3_profile_engine import ProfileError, accept_profile, append_correction, evaluate_profile, record_violation, revoke_profile
from v3_transfer_engine import TransferError, accept_received, deliver_package, retract_delivery


def expect(condition: bool, label: str, errors: list[str]) -> None:
    if not condition:
        errors.append(label)


def run_x41(errors: list[str]) -> None:
    source = {"entity": "entity-personal", "vault_id": "vault-personal", "can_send": True, "allowed_purposes": ["review", "current_use"]}
    destination = {"entity": "entity-company", "vault_id": "vault-company", "can_receive": True, "allowed_purposes": ["review", "current_use"], "maximum_visibility": "internal", "accepts_redaction": True, "accepts_provisional": True}
    allowed = evaluate_policy(source, destination, {"purpose": "current_use", "visibility": "internal"})
    expect(allowed["outcome"] == "permitido", "X4.1 allowed intersection failed", errors)
    redacted = evaluate_policy(source, destination, {"purpose": "review", "visibility": "restricted", "redactions": ["private-opinion"]})
    expect(redacted["outcome"] == "redigido", "X4.1 redaction result failed", errors)
    provisional = evaluate_policy(source, destination, {"purpose": "review", "visibility": "internal", "semantic_status": "conflict"})
    expect(provisional["outcome"] == "provisório", "X4.1 semantic uncertainty was not kept provisional", errors)
    blocked = evaluate_policy(source, {**destination, "can_receive": False}, {"purpose": "current_use", "visibility": "internal"})
    expect(blocked["outcome"] == "bloqueado", "X4.1 destination denial did not block", errors)
    opaque = evaluate_policy(source, destination, {"purpose": "current_use", "visibility": "internal", "boundary_evaluable": False})
    expect("source_vault_id" not in opaque["explanation"], "X4.1 blocked explanation leaked boundary identifiers", errors)


def run_x42(errors: list[str]) -> None:
    vaults = [
        {"vault_id": "vault-personal", "entity": "entity-personal", "authorities": [{"authority_id": "m1", "entity": "entity-personal", "scope": "liferay"}]},
        {"vault_id": "vault-company", "entity": "entity-company", "authorities": [{"authority_id": "g1", "entity": "entity-company", "scope": "liferay"}]},
        {"vault_id": "vault-client", "entity": "entity-client", "authorities": [{"authority_id": "p1", "entity": "entity-client", "scope": "liferay"}]},
    ]
    relations = [
        {"relation_id": "r1", "kind": "cross_entity_delivery", "from_vault_id": "vault-personal", "to_vault_id": "vault-company", "scope": "liferay"},
        {"relation_id": "r2", "kind": "cross_entity_delivery", "from_vault_id": "vault-company", "to_vault_id": "vault-client", "scope": "liferay"},
        {"relation_id": "r3", "kind": "successor", "from_vault_id": "vault-company", "to_vault_id": "vault-personal", "scope": "liferay"},
    ]
    partial = resolve_visible_graph(start_vault_id="vault-company", vaults=vaults, relations=relations, accessible_vault_ids={"vault-client", "vault-company"})
    expect(partial["coverage"] == "partial", "X4.2 inaccessible frontier was not partial", errors)
    expect("vault-personal" not in partial["visible_vault_ids"], "X4.2 inaccessible vault leaked", errors)
    cycle_relations = relations + [{"relation_id": "r4", "kind": "successor", "from_vault_id": "vault-personal", "to_vault_id": "vault-company", "scope": "liferay"}]
    expect(detect_successor_cycles(cycle_relations), "X4.2 successor cycle was not detected", errors)
    collision = detect_authority_collisions(vaults[1]["authorities"] + [{"authority_id": "g2", "entity": "entity-company", "scope": "liferay"}])
    expect(collision, "X4.2 authority collision was not detected", errors)


def run_x43(errors: list[str]) -> None:
    package = {"package": {"package_id": "pkg-1"}, "delivery": {"delivery_id": "del-1"}}
    source = {"entity": "entity-personal", "vault_id": "vault-personal", "can_send": True, "allowed_purposes": ["review"]}
    destination = {"entity": "entity-company", "vault_id": "vault-company", "can_receive": True, "allowed_purposes": ["review"], "maximum_visibility": "internal", "accepts_redaction": True}
    delivered = deliver_package(package, source_policy=source, destination_policy=destination, context={"purpose": "review", "visibility": "internal"})
    expect(delivered["status"] == "delivered" and delivered["publication"] == "not_performed", "X4.3 delivery was conflated with publication", errors)
    pending = accept_received({"acceptance": "accepted", "local_record": {"processing_state": "new"}}, rem_status="pending")
    expect(pending["status"] == "pending_rem" and not pending["current_use"], "X4.3 receipt bypassed REM", errors)
    current = accept_received({"acceptance": "accepted", "local_record": {"processing_state": "new"}}, rem_status="passed")
    expect(current["status"] == "pending_crud" and not current["current_use"], "X4.3 receipt bypassed canonical CRUD", errors)
    tombstone = retract_delivery(delivery_id="del-1", package_id="pkg-1", reason="source correction", recorded_by="owner", recorded_at="2026-09-09T12:00:00Z")
    expect(tombstone["tombstone"] and tombstone["preserve_history"] and not tombstone["current_use"], "X4.3 retraction lost history or current-use block", errors)


def run_x44(errors: list[str]) -> None:
    base = {"identity": "user-1", "destination": "entity-agent", "purpose": "review", "minimized": True}
    pipeline = evaluate_pipeline(base, ["retrieval", "compilation", "injection", "export", "cache", "embedding", "telemetry"])
    expect(pipeline["allowed"], "X4.4 normal passage pipeline was blocked", errors)
    secret = evaluate_privacy_gate({**base, "passage": "injection", "contains_secret": True})
    expect(not secret["allowed"] and secret["rule"] == "secret_not_authorized", "X4.4 secret bypassed injection gate", errors)
    external = evaluate_privacy_gate({**base, "passage": "external_processing", "environment_authorized": False})
    expect(not external["allowed"] and external["rule"] == "external_environment_unauthorized", "X4.4 external environment bypassed gate", errors)
    missing = evaluate_privacy_gate({"passage": "cache", "minimized": True})
    expect(not missing["allowed"], "X4.4 missing boundary context did not fail closed", errors)


def run_x45(errors: list[str]) -> None:
    record = {"record_id": "r1", "destination_vault_id": "vault-company", "source_ref": "pkg-1", "content": "guide\napi_key: SECRET", "minimized": True, "anonymized": True, "redaction_complete": True, "destination_authorized": True, "frontmatter_findings": ["missing_tag"], "semantic_findings": ["needs_review"], "staleness_findings": []}
    destination = {"vault_id": "vault-company", "entity": "entity-company"}
    result = process_ingress(record=record, destination_vault=destination, operation="create", environment_authorized=True)
    local = result["local_record"]
    expect(result["raw_inbox"] is False and "SECRET" not in local["content"], "X4.5 raw content entered destination", errors)
    expect(local["processing_state"] == "new" and local["curation_status"] == "pending_rem", "X4.5 receipt state was not REM-pending", errors)
    expect(not read_findings(record=record)["write_performed"], "X4.5 READ wrote findings", errors)
    expect(rem_double_check(local, destination)["status"] == "passed", "X4.5 REM double check failed", errors)
    try:
        process_ingress(record=record, destination_vault=destination, operation="read", environment_authorized=True)
    except IngressError:
        pass
    else:
        errors.append("X4.5 READ was allowed to persist ingress")
    try:
        process_ingress(record={**record, "declassification_requested": True}, destination_vault=destination, operation="create", environment_authorized=True)
    except IngressError:
        pass
    else:
        errors.append("X4.5 declassification bypassed human approval")


def run_x46(errors: list[str]) -> None:
    link = accept_profile(user_id="user-1", entity="entity-company", vault_id="vault-company", role="curator", scope="liferay", version=1, recorded_at="2026-09-09T12:00:00Z")
    expect(evaluate_profile(link, at="2026-09-09T12:01:00Z", required_role="curator")["valid"], "X4.6 accepted profile was rejected", errors)
    revoked = revoke_profile(link, recorded_by="owner-1", recorded_at="2026-09-09T13:00:00Z", reason="membership ended")
    expect(not evaluate_profile(revoked, at="2026-09-09T13:01:00Z")["valid"], "X4.6 revoked profile remained valid", errors)
    actor = {"user_id": "user-1", "vault_id": "vault-company", "can_write_audit": True}
    event = record_violation(vault_id="vault-company", actor=actor, event={"what": "unauthorized export", "destination": "external", "result": "blocked"}, recorded_at="2026-09-09T13:02:00Z")
    audit = append_correction([event], original_audit_id=event["audit_id"], correction={"what": "unauthorized export corrected", "destination": "external", "result": "closed"}, actor=actor, recorded_at="2026-09-09T13:03:00Z")
    expect(len(audit) == 2 and audit[1]["correction_of"] == event["audit_id"], "X4.6 correction was not additive", errors)
    try:
        record_violation(vault_id="vault-company", actor={"user_id": "other", "vault_id": "other-vault", "can_write_audit": True}, event={"what": "x", "destination": "y", "result": "blocked"}, recorded_at="2026-09-09T13:04:00Z")
    except ProfileError:
        pass
    else:
        errors.append("X4.6 unauthorized audit write was accepted")


def run(section: str = "all") -> list[str]:
    errors: list[str] = []
    runners = {"x41": run_x41, "x42": run_x42, "x43": run_x43, "x44": run_x44, "x45": run_x45, "x46": run_x46}
    for key, runner in runners.items():
        if section in {"all", key}:
            runner(errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--section", choices=["all", "x41", "x42", "x43", "x44", "x45", "x46"], default="all")
    args = parser.parse_args()
    errors = run(args.section)
    if errors:
        print(f"validate_v3_x4: FAILED — {len(errors)} error(s)")
        for error in errors:
            print(f"  [FAIL] {error}")
        return 1
    print(f"validate_v3_x4: OK — {args.section} policy, graph, transfer, privacy, ingress and profile checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
